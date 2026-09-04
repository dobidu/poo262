// Deriva v0.3-quebrada · CAÇA AO BUG 1 - semana 5 · Aula 09
//
// Esta variante NÃO compila errado e NÃO falha nos testes que a acompanham.
// Ela declara destrutor e esquece a cópia - a violação mais barata da regra
// do três, e a que mais sobrevive à revisão de código.
//
// Compile e rode:
//     g++ -std=c++17 -Wall -Wextra -Wpedantic grade_quebrada.cpp -o quebrada
//     ./quebrada                       # a evidência, sem ferramenta nenhuma
//     g++ -std=c++17 -g -fsanitize=address,undefined grade_quebrada.cpp -o q-asan
//     ./q-asan                         # o ASan nomeando o crime
//
// Repare no que -Wall -Wextra -Wpedantic diz sobre isto: nada.
#include <cstddef>
#include <cstdio>

namespace deriva_quebrada {

struct celula {
  int energia = 0;
  int massa = 0;
  char glifo = '.';
  char sigla = ' ';
};

/// A grade da v0.3, com uma diferença: o buffer é um ponteiro cru, e a posse
/// dele é do destrutor.
class grade {
 public:
  grade(int largura, int altura)
      : largura_(largura),
        altura_(altura),
        dados_(new celula[static_cast<std::size_t>(largura) *
                          static_cast<std::size_t>(altura)]) {}

  // Destrutor declarado. A partir daqui, a cópia gerada pelo compilador
  // passou a ser um erro - e o compilador não avisa, porque gerar cópia
  // membro a membro é exatamente o que a linguagem manda fazer.
  ~grade() { delete[] dados_; }

  // FALTA: grade(const grade&)
  // FALTA: grade& operator=(const grade&)
  // (é a regra do três, e ela está pela metade)

  [[nodiscard]] celula& em(int x, int y) {
    return dados_[static_cast<std::size_t>(y) * static_cast<std::size_t>(largura_) +
                  static_cast<std::size_t>(x)];
  }
  [[nodiscard]] const celula* buffer() const noexcept { return dados_; }

 private:
  int largura_;
  int altura_;
  celula* dados_;
};

}  // namespace deriva_quebrada

int main() {
  using deriva_quebrada::grade;

  std::puts("== evidencia 1: as duas grades compartilham o mesmo buffer");
  int compartilham = 0;
  {
    grade a(4, 3);
    a.em(0, 0).glifo = '@';

    grade b = a;                   // parece uma cópia. é um apelido.
    b.em(0, 0).glifo = '#';

    std::printf("   a[0,0] = '%c'   (o esperado era '@')\n", a.em(0, 0).glifo);
    std::printf("   b[0,0] = '%c'\n", b.em(0, 0).glifo);
    std::printf("   buffer de a = %p\n   buffer de b = %p\n",
                static_cast<const void*>(a.buffer()),
                static_cast<const void*>(b.buffer()));
    compartilham = (a.buffer() == b.buffer()) ? 1 : 0;

    std::puts("\n== evidencia 2: ao sair deste escopo, os DOIS destrutores rodam");
    std::puts("   e os dois chamam delete[] no mesmo endereco.");
    std::fflush(stdout);
  }  // <-- aqui. com ASan, o programa morre nesta linha.

  // Nesta maquina a propria glibc aborta aqui, com
  //     free(): double free detected in tcache 2
  // Nao conte com isso: o tcache detecta ESTE padrao, e um double free
  // separado por outras alocacoes costuma passar. A deteccao do alocador e
  // sorte de arranjo; o ASan e que da a garantia.
  std::puts("\n(se o programa chegou aqui, o alocador nao reclamou HOJE,");
  std::puts(" nesta maquina, com esta libc - o que e pior que abortar.)");

  // Falha de propósito: esta variante existe para acusar, não para passar.
  return compartilham ? 1 : 0;
}
