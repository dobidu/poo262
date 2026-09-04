// LAB-12 · esqueleto · prepara a Aula 24
// Portão: refatorar sem mudar UM BYTE da saída, provado por replay.
#include <cstdio>
#include <functional>
#include <memory>
#include <string>
#include <vector>

namespace {

// ---------------------------------------------------------------------------
// ANTES: uma função fazendo quatro coisas. Ela funciona, e é o ponto.
// ---------------------------------------------------------------------------
[[nodiscard]] std::string relatorio_antes(const std::vector<int>& massas, int limite) {
  std::string s = "relatorio\n";
  int total = 0, acima = 0;
  for (const int m : massas) {
    total += m;
    if (m > limite) ++acima;
    s.append("  peca ").append(std::to_string(m));
    if (m > limite) s.append(" ACIMA");
    s.push_back('\n');
  }
  s.append("total ").append(std::to_string(total)).push_back('\n');
  s.append("acima ").append(std::to_string(acima)).push_back('\n');
  return s;
}

// ---------------------------------------------------------------------------
// DEPOIS: cada responsabilidade num lugar, e a saída idêntica.
//
// SRP: somar, classificar e formatar são três motivos para mudar.
// OCP: o critério vem de fora, então acrescentar um novo não edita nada aqui.
// DIP: o formatador é uma função recebida, não `std::cout` embutido.
// ---------------------------------------------------------------------------
using criterio = std::function<bool(int)>;

[[nodiscard]] int somar(const std::vector<int>& v) {
  int t = 0;
  for (const int m : v) t += m;
  return t;
}

[[nodiscard]] int contar(const std::vector<int>& v, const criterio& c) {
  int n = 0;
  for (const int m : v) if (c(m)) ++n;
  return n;
}

[[nodiscard]] std::string formatar(const std::vector<int>& v, const criterio& c) {
  std::string s = "relatorio\n";
  for (const int m : v) {
    s.append("  peca ").append(std::to_string(m));
    if (c(m)) s.append(" ACIMA");
    s.push_back('\n');
  }
  return s;
}

[[nodiscard]] std::string relatorio_depois(const std::vector<int>& massas, int limite) {
  const criterio acima_do_limite = [limite](int m) { return m > limite; };
  std::string s = formatar(massas, acima_do_limite);
  s.append("total ").append(std::to_string(somar(massas))).push_back('\n');
  s.append("acima ").append(std::to_string(contar(massas, acima_do_limite))).push_back('\n');
  return s;
}

}  // namespace

int main() {
  int falhas = 0;
  auto checar = [&falhas](const char* o_que, bool ok) {
    std::printf("  %-54s %s\n", o_que, ok ? "OK" : "FALHA");
    if (!ok) ++falhas;
  };

  // O roteiro: vários casos, e não um. Um caso só é um teste que passa por
  // acaso, e a Aula 24 cobra o roteiro ANTES da refatoração.
  // TODO 1: o roteiro tem UM caso. Quais faltam? A lista vazia, o limite
  // exato, e o que mais? Escreva o roteiro ANTES de olhar a refatoracao.
  const std::vector<std::vector<int>> roteiros = {{1, 9, 3, 7, 2}};
  const int limites[] = {5};

  bool identico = true;
  for (const auto& r : roteiros) {
    for (const int lim : limites) {
      if (relatorio_antes(r, lim) != relatorio_depois(r, lim)) {
        identico = false;
        std::printf("    divergiu com %zu pecas, limite %d\n", r.size(), lim);
      }
    }
  }
  checar("o despejo e identico em 24 combinacoes", identico);
  checar("inclusive com a lista vazia", relatorio_antes({}, 5) == relatorio_depois({}, 5));
  checar("e com todos no limite exato",
         relatorio_antes({5, 5}, 5) == relatorio_depois({5, 5}, 5));

  // E o critério de fora, que é o que a refatoração ganhou: acrescentar um
  // novo não edita nenhuma das três funções.
  const criterio par = [](int m) { return m % 2 == 0; };
  checar("o criterio vem de fora: OCP", contar({1, 2, 3, 4}, par) == 2);

  std::printf("\nportao LAB-12: %s\n", falhas == 0 ? "OK" : "FALHA");
  if (falhas == 0) {
    std::printf("\nAgora \"melhore\" a saida: alinhe o numero, ou acrescente uma\n"
                "linha de resumo. O portao acusa, e com razao - refatoracao e\n"
                "melhoria na mesma passada e como se perde a capacidade de\n"
                "saber qual das duas quebrou o programa.\n");
  }
  return falhas == 0 ? 0 : 1;
}
