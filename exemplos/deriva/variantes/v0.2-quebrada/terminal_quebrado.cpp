// Deriva v0.2-quebrada · Aula 08 (RAII)
//
// ┌─ AVISO ────────────────────────────────────────────────────────────────┐
// │ Este programa deixa o SEU terminal sem eco e sem Enter depois de sair. │
// │ É o ponto dele. Rode num terminal descartável, ou saiba que o conserto │
// │ é digitar  reset  e apertar Enter - às cegas.                          │
// │                                                                        │
// │ Em pipe, em teste ou em CI ele não mexe em nada: sem tty, não há modo  │
// │ bruto a alterar. Nesse caso a evidência é o contador, que fecha em 1.   │
// └────────────────────────────────────────────────────────────────────────┘
//
// g++ -std=c++17 -Wall -Wextra -Wpedantic terminal_quebrado.cpp -o quebrado
#include <termios.h>
#include <unistd.h>

#include <cstdio>

namespace deriva_quebrada {

struct contador_terminal {
  inline static int vivos = 0;
};

/// O terminal_bruto da v0.2, sem o destrutor.
class terminal_bruto {
 public:
  terminal_bruto() {
    ++contador_terminal::vivos;
    if (::isatty(STDIN_FILENO) == 0) return;
    if (::tcgetattr(STDIN_FILENO, &salvo_) != 0) return;
    termios bruto = salvo_;
    const tcflag_t cru = static_cast<tcflag_t>(ICANON) | static_cast<tcflag_t>(ECHO);
    bruto.c_lflag &= ~cru;
    if (::tcsetattr(STDIN_FILENO, TCSAFLUSH, &bruto) == 0) ativo_ = true;
  }

  // FALTA: ~terminal_bruto() { if (ativo_) tcsetattr(..., &salvo_); }
  //
  // O recurso adquirido no construtor não é memória: é um estado do sistema
  // operacional, e ele sobrevive ao processo. Nenhum sanitizer, nenhum
  // coletor de lixo e nenhum sistema operacional vai desfazer isto por você.

  [[nodiscard]] bool ativo() const noexcept { return ativo_; }

 private:
  termios salvo_{};
  bool ativo_ = false;
};

}  // namespace deriva_quebrada

int main() {
  using deriva_quebrada::contador_terminal;
  using deriva_quebrada::terminal_bruto;

  bool era_tty = false;
  {
    const terminal_bruto t;
    era_tty = t.ativo();
    std::printf("terminal em modo bruto: %s\n", era_tty ? "sim" : "nao (sem tty)");
    std::printf("vivos dentro do escopo: %d\n", contador_terminal::vivos);
  }  // o escopo fecha, o objeto morre, e NADA é restaurado

  std::printf("vivos depois do escopo: %d   <-- devia ser 0\n",
              contador_terminal::vivos);
  if (era_tty) {
    std::puts("");
    std::puts("Se voce esta num terminal de verdade, ele esta quebrado agora.");
    std::puts("Digite  reset  e Enter. Voce nao vera o que digita.");
  } else {
    std::puts("");
    std::puts("Sem tty nada foi alterado - mas o contador acusa: um objeto");
    std::puts("nasceu e nenhum destrutor rodou. Era esse o recurso.");
  }
  return contador_terminal::vivos == 0 ? 0 : 1;
}
