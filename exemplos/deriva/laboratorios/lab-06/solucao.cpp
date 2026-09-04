// LAB-06 · solução de referência · prepara a Aula 11
// Portão: provar o vazamento SEM ferramenta externa, e provar a correção.
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

namespace {

/// O contador mora na DERIVADA, e é essa a decisão que faz este laboratório
/// funcionar. Na base, o destrutor da base decrementaria por todos, e o
/// contador fecharia em zero mesmo com o defeito presente - foi o que a
/// variante `v1.1-quebrada` mostrou.
struct base_quebrada {
  virtual ~base_quebrada() = default;   // corrigido: era não-virtual
  virtual char glifo() const = 0;
};

struct derivada final : base_quebrada {
  inline static int vivos = 0;
  inline static int criados = 0;

  derivada() : leituras_(256, 0) {
    ++vivos;
    ++criados;
  }
  ~derivada() override { --vivos; }

  char glifo() const override { return 'd'; }

 private:
  std::vector<int> leituras_;   // 1 KB que só o destrutor da derivada libera
};

}  // namespace

int main() {
  int falhas = 0;
  auto checar = [&falhas](const char* o_que, bool ok) {
    std::printf("  %-50s %s\n", o_que, ok ? "OK" : "FALHA");
    if (!ok) ++falhas;
  };

  // (1) Deletar por ponteiro da base, com destrutor virtual: fecha.
  {
    std::unique_ptr<base_quebrada> e = std::make_unique<derivada>();
    checar("um objeto vivo dentro do escopo", derivada::vivos == 1);
    checar("e o despacho virtual funciona", e->glifo() == 'd');
  }
  checar("o destrutor da derivada rodou: vivos fecha em zero", derivada::vivos == 0);

  // (2) Muitos objetos, num vetor de ponteiros da base. É a forma do `mundo`.
  {
    std::vector<std::unique_ptr<base_quebrada>> muitos;
    for (int k = 0; k < 10; ++k) muitos.push_back(std::make_unique<derivada>());
    checar("dez vivos", derivada::vivos == 10);
  }
  checar("dez destruidos ao sair do escopo", derivada::vivos == 0);
  checar("e criados contou os onze", derivada::criados == 11);

  // (3) O que o contador NÃO acusaria se ele morasse na base.
  //     Este é o item que o laboratório cobra por escrito, e não por código.
  checar("o contador mora na derivada, e e por isso que ele acusa",
         derivada::vivos == 0 && derivada::criados == 11);

  std::printf("\nportao LAB-06: %s\n", falhas == 0 ? "OK" : "FALHA");
  if (falhas == 0) {
    std::printf("\nAgora rode ../../variantes/v1.1-quebrada/ e responda:\n"
                "  a) por que `vivos` fecha em ZERO lá, com o defeito presente?\n"
                "  b) quantos avisos o compilador da com -Wall -Wextra -Wpedantic\n"
                "     quando o delete esta dentro de um unique_ptr?\n");
  }
  return falhas == 0 ? 0 : 1;
}
