// LAB-09 · esqueleto · prepara a Aula 16
// Portão: escrever o teste que TRAVA a refatoração antes de refatorar.
//
// A ordem é cobrada, e é o conteúdo do laboratório: quem refatora e depois
// escreve o teste escreve o teste que passa.
#include <cstdio>
#include <string>
#include <vector>

namespace {

/// Um gerador congruente linear. Determinístico dada a semente, e é essa
/// propriedade que torna o replay possível.
class sorteio {
 public:
  explicit sorteio(unsigned semente) noexcept : estado_(semente) {}
  [[nodiscard]] int ate(int limite) noexcept {
    estado_ = estado_ * 1664525u + 1013904223u;
    return limite <= 0 ? 0 : static_cast<int>(estado_ % static_cast<unsigned>(limite));
  }

 private:
  unsigned estado_;
};

/// A função a refatorar. Versão ANTES: um laço só, fazendo três coisas.
[[nodiscard]] std::string percurso_antes(unsigned semente, int passos, int largura) {
  sorteio s(semente);
  std::string saida;
  int x = largura / 2, colhidos = 0;
  for (int k = 0; k < passos; ++k) {
    const int d = s.ate(3) - 1;
    const int alvo = x + d;
    if (alvo >= 0 && alvo < largura) x = alvo;
    if (s.ate(4) == 0) ++colhidos;
    saida.append(std::to_string(x)).push_back(colhidos > 0 ? '*' : '.');
  }
  return saida + " colhidos=" + std::to_string(colhidos);
}

/// Versão DEPOIS: três responsabilidades separadas. Tem de produzir o MESMO
/// despejo, byte a byte - e é o roteiro gravado que prova.
[[nodiscard]] int mover(int x, int d, int largura) noexcept {
  const int alvo = x + d;
  return (alvo >= 0 && alvo < largura) ? alvo : x;
}

[[nodiscard]] std::string percurso_depois(unsigned semente, int passos, int largura) {
  sorteio s(semente);
  std::string saida;
  int x = largura / 2, colhidos = 0;
  for (int k = 0; k < passos; ++k) {
    // A ordem das chamadas ao sorteio é parte do comportamento observável:
    // trocar as duas linhas abaixo muda o despejo sem mudar a lógica, e é o
    // erro que a caça ao bug 3 procura.
    const int d = s.ate(3) - 1;
    x = mover(x, d, largura);
    if (s.ate(4) == 0) ++colhidos;
    saida.append(std::to_string(x)).push_back(colhidos > 0 ? '*' : '.');
  }
  return saida + " colhidos=" + std::to_string(colhidos);
}

}  // namespace

int main() {
  int falhas = 0;
  auto checar = [&falhas](const char* o_que, bool ok) {
    std::printf("  %-52s %s\n", o_que, ok ? "OK" : "FALHA");
    if (!ok) ++falhas;
  };

  // (1) O roteiro gravado: várias sementes, e não uma. Uma semente só é um
  //     teste que passa por acaso.
  // TODO 1: uma semente so e um teste que passa por acaso. Quantas, e quais?
  const unsigned sementes[] = {7u};
  bool todas_iguais = true;
  for (const unsigned sem : sementes) {
    if (percurso_antes(sem, 40, 20) != percurso_depois(sem, 40, 20)) {
      todas_iguais = false;
      std::printf("    divergiu na semente %u\n", sem);
    }
  }
  checar("o despejo e identico em cinco sementes", todas_iguais);

  // (2) Determinismo: a mesma semente sempre dá o mesmo despejo.
  checar("a mesma semente da o mesmo despejo",
         percurso_depois(7u, 40, 20) == percurso_depois(7u, 40, 20));

  // (3) E sementes diferentes dão despejos diferentes - senão o teste passaria
  //     comparando duas funções que ignoram a entrada.
  checar("sementes diferentes dao despejos diferentes",
         percurso_depois(1u, 40, 20) != percurso_depois(2u, 40, 20));

  // (4) O roteiro exercita o limite, e não só o meio. Sem isto, a refatoração
  //     poderia quebrar a borda sem ninguem notar.
  // TODO 2: o roteiro exercita o MEIO. Acrescente os casos de borda - sem
  // eles, a refatoracao pode quebrar o limite sem que ninguem note.
  checar("o roteiro exercita a borda esquerda", true);

  std::printf("\nportao LAB-09: %s\n", falhas == 0 ? "OK" : "FALHA");
  if (falhas == 0) {
    std::printf("\nAgora TROQUE a ordem das duas chamadas a `s.ate` em\n"
                "`percurso_depois` e rode de novo. A logica nao mudou, o\n"
                "despejo mudou, e o portao acusa. E o erro da caca ao bug 3.\n");
  }
  return falhas == 0 ? 0 : 1;
}
