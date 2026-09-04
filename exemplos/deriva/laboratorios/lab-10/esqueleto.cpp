// LAB-10 · esqueleto · prepara a Aula 19
// Portão: as três classes usando `contador_de_instancias<T>`, com
// comportamento idêntico ao contador escrito à mão.
#include <cstdio>
#include <string>

namespace {

/// O contador, generalizado por CRTP. Cada instanciação é um TIPO diferente,
/// logo tem os seus próprios contadores - e é isso que herança comum não faz.
// TODO 1: falta o parametro de template, e sem ele os tres tipos passam a
// compartilhar UM contador so. Rode antes de acrescentar.
class contador_de_instancias {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;
  static void zerar() noexcept { vivos = criados = 0; }
  [[nodiscard]] static bool fechou() noexcept { return vivos == 0; }

 protected:
  contador_de_instancias() noexcept { ++vivos; ++criados; }
  // TODO 2: a copia tambem e um nascimento. O que falta?
  contador_de_instancias(const contador_de_instancias&) noexcept {}
  ~contador_de_instancias() noexcept { --vivos; }
};

/// A versão manual, escrita à mão desde a Aula 7. Fica aqui para ser
/// comparada - é a repetição dela, seis vezes no Deriva, que motivou o
/// template.
struct manual {
  inline static int vivos = 0;
  inline static int criados = 0;
  manual() { ++vivos; ++criados; }
  manual(const manual&) { ++vivos; ++criados; }
  ~manual() { --vivos; }
};

// TODO 3: passe cada tipo a si mesmo. E o que da a cada um o seu contador.
struct sonda : contador_de_instancias { int energia = 100; };
struct drone : contador_de_instancias { int carga = 0; };
struct item : contador_de_instancias { std::string nome = "sucata"; };

}  // namespace

int main() {
  int falhas = 0;
  auto checar = [&falhas](const char* o_que, bool ok) {
    std::printf("  %-54s %s\n", o_que, ok ? "OK" : "FALHA");
    if (!ok) ++falhas;
  };

  contador_de_instancias<sonda>::zerar();
  contador_de_instancias<drone>::zerar();
  contador_de_instancias<item>::zerar();
  manual::vivos = manual::criados = 0;

  {
    const sonda s1, s2;
    const drone d;
    const item i;
    checar("cada tipo tem o SEU contador", contador_de_instancias<sonda>::vivos == 2);
    checar("e o do drone nao foi afetado", contador_de_instancias<drone>::vivos == 1);
    checar("nem o do item", contador_de_instancias<item>::vivos == 1);
  }
  checar("os tres fecham em zero",
         contador_de_instancias<sonda>::fechou() &&
         contador_de_instancias<drone>::fechou() &&
         contador_de_instancias<item>::fechou());

  // A comparação que justifica o template: comportamento idêntico.
  contador_de_instancias<sonda>::zerar();
  {
    const sonda a;
    const sonda copia = a;
    const manual m;
    const manual m_copia = m;
    checar("o CRTP conta a copia, como o manual contava",
           contador_de_instancias<sonda>::vivos == manual::vivos);
    checar("e `criados` tambem bate",
           contador_de_instancias<sonda>::criados == manual::criados);
  }
  checar("os dois fecham em zero", contador_de_instancias<sonda>::vivos == 0 && manual::vivos == 0);

  // O que o template ganha e o manual não tinha: custo zero declarado.
  checar("a base do CRTP e vazia: nao ha estado por objeto",
         sizeof(contador_de_instancias<sonda>) == 1);
  checar("e a derivada nao cresce por causa dela",
         sizeof(sonda) == sizeof(int));

  std::printf("\nportao LAB-10: %s\n", falhas == 0 ? "OK" : "FALHA");
  if (falhas == 0) {
    std::printf("\nAgora tente trocar o CRTP por uma base NAO-template comum e\n"
                "rode de novo. Os tres tipos passam a compartilhar um contador\n"
                "so, e nenhum deles acusa mais nada.\n");
  }
  return falhas == 0 ? 0 : 1;
}
