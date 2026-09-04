// Deriva v1.1-quebrada · CAÇA AO BUG 2 - semana 9 · Aula 11
//
// A base tem função virtual e destrutor NÃO virtual. Deletar por
// `entidade*` não roda o destrutor da derivada, e o contador de instâncias
// vivas é o que acusa.
//
// O ponto desta variante não é o defeito, que é conhecido. É QUANDO o
// compilador avisa, e as três medições abaixo dão respostas diferentes:
//
//   A  delete textual, com -Wall -Wextra -Wpedantic        1 aviso
//   B  o mesmo delete dentro de unique_ptr                  0 avisos
//   C  qualquer um dos dois, com -Wnon-virtual-dtor         3 avisos
//
// O caso B é o que interessa. O `delete` passou a morar num cabeçalho do
// sistema, dentro de `std::default_delete`, e o -Wdelete-non-virtual-dtor não
// aponta para código que não é seu. C++ moderno, feito certo em tudo o mais,
// silenciou o único aviso que existia.
//
// O portão do Deriva liga -Wnon-virtual-dtor de propósito, e por isso esta
// variante falha na condição 1 de 4 e não na 2. Também é uma lição: o aviso
// existia, e bastava pedir.
//
//   g++ -std=c++17 -Wall -Wextra -Wpedantic destrutor_quebrado.cpp -o quebrado
//   ./quebrado
//   g++ -std=c++17 -Wall -Wextra -Wpedantic -Wnon-virtual-dtor -fsyntax-only destrutor_quebrado.cpp
#include <cstdio>
#include <memory>
#include <vector>

namespace deriva_quebrada {

struct contador {
  inline static int vivos = 0;
  inline static int criados = 0;
  inline static int destrutores_de_base = 0;
  inline static int destrutores_de_derivada = 0;
};

/// A base da hierarquia da v1.0. Tem função virtual, então é polimórfica -
/// e é para ser usada por ponteiro de base.
struct entidade {
  explicit entidade(char glifo) : glifo_(glifo) {
    ++contador::vivos;
    ++contador::criados;
  }

  // FALTA a palavra `virtual` aqui. É a única diferença entre esta variante e
  // a v1.1 boa.
  ~entidade() {
    ++contador::destrutores_de_base;
    --contador::vivos;
  }

  virtual void desenhar() const { std::putchar(glifo_); }

 protected:
  char glifo_;
};

/// A derivada adquire recurso próprio: um vetor de leituras da inspeção.
/// Sem destrutor virtual na base, este destrutor nunca roda.
struct sonda : entidade {
  sonda() : entidade('@'), leituras_(1024, 0) {}

  ~sonda() { ++contador::destrutores_de_derivada; }

  void desenhar() const override { std::putchar('@'); }

 private:
  std::vector<int> leituras_;   // 4 KB que ninguém libera
};

}  // namespace deriva_quebrada

int main() {
  using namespace deriva_quebrada;

  std::puts("== caso A: delete textual, por ponteiro da base");
  {
    entidade* e = new sonda();
    e->desenhar();
    std::putchar('\n');
    delete e;   // -Wall aponta AQUI: -Wdelete-non-virtual-dtor
  }
  std::printf("   ~entidade() rodou %d vez  ~sonda() rodou %d vez\n",
              contador::destrutores_de_base, contador::destrutores_de_derivada);

  std::puts("\n== caso B: o MESMO delete, dentro de unique_ptr");
  {
    std::unique_ptr<entidade> e = std::make_unique<sonda>();
    e->desenhar();
    std::putchar('\n');
  }  // o delete acontece em <bits/unique_ptr.h>, e o aviso desaparece
  std::printf("   ~entidade() rodou %d vezes  ~sonda() rodou %d vez\n",
              contador::destrutores_de_base, contador::destrutores_de_derivada);

  std::puts("");
  std::printf("criados                 %d\n", contador::criados);
  std::printf("vivos                   %d   <-- e ele fecha em zero\n", contador::vivos);
  std::printf("~sonda() executado      %d   <-- e este e o vazamento\n",
              contador::destrutores_de_derivada);
  std::puts("");
  std::puts("O contador de instancias fecha em ZERO e mente: ele conta objetos,");
  std::puts("e o destrutor da base decrementa por todos. Para acusar este defeito");
  std::puts("o contador tem de morar na DERIVADA - e e assim que a v1.1 boa faz.");

  // Falha de propósito: os dois destrutores de derivada deviam ter rodado.
  return contador::destrutores_de_derivada == 2 ? 0 : 1;
}
