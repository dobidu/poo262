// Aula 02 - o que o sanitizer pega, e o portão não
//
// Duas coisas que o Deriva NÃO tem, e não é acidente: `-Wconversion`,
// `-Wsign-conversion` e o par `dentro()`/`em()` as impedem. Elas moram aqui
// porque o capítulo precisa mostrar o ASan e o UBSan fazendo o trabalho deles,
// e no núcleo ou na suíte elas abortariam as condições 1 e 2 do portão.
//
// Não é variante da trilha: é artefato de aula, como `comparativo/`,
// `revisao_ia/` e `tipos/`.
//
// Nenhum dos dois defeitos produz aviso de compilação. Os dois produzem
// comportamento indefinido, e o programa **parece funcionar** - o que é o pior
// resultado possível.
//
//   g++ -std=c++17 -Wall -Wextra -Wpedantic -Wconversion defeitos_de_memoria.cpp -o quebrado
//   ./quebrado                       # roda, e mente
//
//   g++ -std=c++17 -g -fsanitize=address defeitos_de_memoria.cpp -o q-asan
//   ./q-asan                         # ASan aponta a linha e a alocação
//
//   g++ -std=c++17 -g -fsanitize=undefined defeitos_de_memoria.cpp -o q-ubsan
//   ./q-ubsan                        # UBSan nomeia o estouro com sinal
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

namespace deriva_quebrada {

struct celula {
  int energia = 0;
  int massa = 0;
  char glifo = '.';
  char sigla = ' ';
};

/// A grade da v0.2, com uma diferença: `em()` não tem par com `dentro()`, e
/// ninguém confere o limite. A versão boa deixa a escolha do custo com quem
/// chama, e é isso que este arquivo remove.
class grade {
 public:
  grade(int largura, int altura)
      : largura_(largura),
        altura_(altura),
        // DEFEITO 2 · estouro de `int` com sinal.
        //
        // Com largura e altura grandes, `largura * altura` estoura ANTES de
        // virar `size_t`, e o resultado é negativo. Convertido para `size_t`,
        // ele vira um número enorme, e o `vector` lança `length_error` - ou,
        // com valores diferentes, aloca um vetor pequeno demais e o defeito
        // 1 passa a acontecer sem ninguém ter indexado fora.
        //
        // A versão boa converte CADA fator antes de multiplicar, e é por isso
        // que ela tem dois `static_cast` que parecem redundantes e não são.
        celulas_(static_cast<std::size_t>(largura * altura)) {}

  // DEFEITO 1 · acesso fora de limite.
  //
  // Sem `dentro()` ao lado, esta função aceita qualquer posição. O
  // `operator[]` do vector não confere - `at()` conferiria, e é a escolha que
  // a versão boa deixa explícita.
  [[nodiscard]] celula& em(int x, int y) {
    return celulas_[static_cast<std::size_t>(y) * static_cast<std::size_t>(largura_) +
                    static_cast<std::size_t>(x)];
  }

  [[nodiscard]] int largura() const noexcept { return largura_; }
  [[nodiscard]] int altura() const noexcept { return altura_; }
  [[nodiscard]] std::size_t celulas() const noexcept { return celulas_.size(); }

 private:
  int largura_;
  int altura_;
  std::vector<celula> celulas_;
};

}  // namespace deriva_quebrada

int main() {
  using deriva_quebrada::grade;

  std::puts("== defeito 1: acesso fora de limite, sem um aviso de compilacao");
  {
    grade g(4, 3);              // 12 células, índices válidos de 0 a 11
    g.em(0, 0).glifo = '@';

    // Linha 3 numa grade de 3 fileiras: o índice calculado é 12 + 2 = 14.
    // Fora dos 12. O `operator[]` não confere, e a escrita acontece.
    g.em(2, 3).glifo = '#';

    std::printf("   celulas alocadas ... %zu\n", g.celulas());
    std::printf("   escrevi em (2,3), que exigiria %d celulas\n", 3 * 4 + 3);
    std::printf("   li de volta ........ '%c'  <-- e ele responde\n", g.em(2, 3).glifo);
    std::puts("   nenhum aviso, nenhuma excecao, e o programa continua.");
  }

  std::puts("\n== defeito 2: estouro de int com sinal na conta do tamanho");
  {
    // As dimensões vêm de FORA - de linha de comando, como vêm de um arquivo
    // de mapa no Deriva de verdade. E é essa a diferença que importa.
    //
    // Escrito com literais - `const int p = 50000 * 50000;` - o g++ dobra a
    // conta em tempo de compilação, vê o estouro e avisa: `-Woverflow`,
    // "integer overflow in expression of type 'int' results in
    // '-1794967296'". O defeito não embarca.
    //
    // Com os valores vindo de fora, o compilador não tem o que dobrar, o aviso
    // desaparece, e o estouro passa a acontecer em execução. É assim que ele
    // chega em produção: não com número escrito no código, mas com número
    // lido de um arquivo que alguém editou.
    const int largura = std::atoi("50000");
    const int altura = std::atoi("50000");
    const int produto = largura * altura;       // <-- o estouro, sem aviso
    std::printf("   largura x altura ... %d  <-- deveria ser 2500000000\n", produto);
    std::printf("   como size_t ........ %zu\n", static_cast<std::size_t>(produto));
    std::puts("   a conta acontece em int, e nenhum static_cast depois a conserta.");
    std::puts("   a versao boa converte CADA fator ANTES de multiplicar.");
  }

  std::puts("\nCompilam com -Wall -Wextra -Wpedantic -Wconversion sem uma palavra,");
  std::puts("porque os valores vem de fora. Com literais, o -Woverflow pegaria o");
  std::puts("segundo - e e por isso que o defeito real nunca vem com literal.");
  std::puts("Rode com -fsanitize=address e -fsanitize=undefined.");

  // Falha de propósito: esta variante existe para acusar.
  return 1;
}
