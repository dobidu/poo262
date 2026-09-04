// LAB-01 · esqueleto · prepara a Aula 2
//
// Portão: compilar sem um warning sob -Wall -Wextra -Wpedantic, e reportar o
// ambiente que a disciplina fixou.
//
//   g++ -std=c++17 -Wall -Wextra -Wpedantic -Wconversion esqueleto.cpp -o meu
//
// Este arquivo compila E emite avisos de propósito. Sua tarefa é fazer os
// avisos desaparecerem sem desligar nenhum deles, e completar o portão.
#include <cstdio>
#include <string>

namespace {

struct ambiente {
  std::string padrao;
  int avisos_tolerados;
  bool extensoes_gnu;
};

[[nodiscard]] ambiente da_disciplina() {
  // TODO 1: descubra o padrão em uso. `__cplusplus` vale 201703L para C++17.
  const bool eh_17 = false;

  // TODO 2: descubra se as extensões GNU estão ligadas. A macro é
  // `__STRICT_ANSI__`, e ela é definida quando elas estão DESLIGADAS.
  const bool gnu = true;

  return {eh_17 ? "c++17" : "outro", 0, gnu};
}

// TODO 3: esta função emite um aviso de -Wconversion. Conserte sem mudar a
// assinatura e sem desligar o aviso.
[[nodiscard]] char digito(int n) { return '0' + (n % 10); }

}  // namespace

int main() {
  const ambiente a = da_disciplina();

  std::printf("padrao ................ %s\n", a.padrao.c_str());
  std::printf("avisos tolerados ...... %d\n", a.avisos_tolerados);
  std::printf("extensoes GNU ......... %s\n", a.extensoes_gnu ? "SIM" : "nao");
  std::printf("digito de 47 .......... %c\n", digito(47));

  const bool ok = a.padrao == "c++17" && !a.extensoes_gnu;
  std::printf("\nportao LAB-01: %s\n", ok ? "OK" : "FALHA");
  if (!ok) std::printf("  resolva os TODO deste arquivo\n");
  return ok ? 0 : 1;
}
