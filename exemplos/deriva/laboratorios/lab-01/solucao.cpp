// LAB-01 · solução de referência · prepara a Aula 2
//
// Portão: compilar sem um warning sob -Wall -Wextra -Wpedantic, e o programa
// reportar o ambiente que a disciplina fixou.
#include <cstdio>
#include <string>

namespace {

/// O portão não é "compila": é "compila sem aviso". A diferença aparece aqui.
/// Cada linha abaixo já foi um aviso num semestre anterior.
struct ambiente {
  std::string padrao;
  int avisos_tolerados;
  bool extensoes_gnu;
};

[[nodiscard]] ambiente da_disciplina() {
  // `__cplusplus` vale 201703L para C++17. Comparar com o número, e não com uma
  // macro do compilador, é o que torna a checagem portável.
  const bool eh_17 = __cplusplus == 201703L;

  // `__STRICT_ANSI__` é definida quando as extensões GNU estão DESLIGADAS,
  // isto é, com -std=c++17 e não -std=gnu++17. É o que `CXX_EXTENSIONS OFF`
  // garante no CMake.
#ifdef __STRICT_ANSI__
  const bool gnu = false;
#else
  const bool gnu = true;
#endif

  return {eh_17 ? "c++17" : "outro", 0, gnu};
}

/// Conversão explícita porque `-Wconversion` está ligado: `int` para `char`
/// perde informação, e o compilador exige que se diga que isso é intencional.
[[nodiscard]] char digito(int n) { return static_cast<char>('0' + (n % 10)); }

}  // namespace

int main() {
  const ambiente a = da_disciplina();

  std::printf("padrao ................ %s\n", a.padrao.c_str());
  std::printf("avisos tolerados ...... %d\n", a.avisos_tolerados);
  std::printf("extensoes GNU ......... %s\n", a.extensoes_gnu ? "SIM" : "nao");
  std::printf("digito de 47 .......... %c\n", digito(47));

  const bool ok = a.padrao == "c++17" && !a.extensoes_gnu;
  std::printf("\nportao LAB-01: %s\n", ok ? "OK" : "FALHA");
  if (!ok) {
    std::printf("  compile com -std=c++17 (e nao -std=gnu++17)\n");
  }
  return ok ? 0 : 1;
}
