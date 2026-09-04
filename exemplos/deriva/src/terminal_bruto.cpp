#include "deriva/terminal_bruto.hpp"

#include <termios.h>
#include <unistd.h>

namespace deriva {
namespace {
termios& salvo() {
  static termios t{};
  return t;
}
}  // namespace

terminal_bruto::terminal_bruto() {
  ++contador_terminal::vivos;
  ++contador_terminal::criados;

  if (::isatty(STDIN_FILENO) == 0) return;  // pipe, teste, CI: não há o que mexer
  if (::tcgetattr(STDIN_FILENO, &salvo()) != 0) return;

  termios bruto = salvo();

  // ICANON e ECHO são macros de `int`. `~(ICANON | ECHO)` é um int NEGATIVO,
  // e atribuí-lo a `c_lflag`, que é `unsigned`, muda o valor de -11 para
  // 4294967285. O resultado funciona por acidente do complemento de dois, e
  // -Wsign-conversion está certo em reclamar. Converter primeiro, complementar
  // depois: aí a operação toda acontece em `tcflag_t`.
  const tcflag_t cru = static_cast<tcflag_t>(ICANON) | static_cast<tcflag_t>(ECHO);
  bruto.c_lflag &= ~cru;
  bruto.c_cc[VMIN] = 1;
  bruto.c_cc[VTIME] = 0;
  if (::tcsetattr(STDIN_FILENO, TCSAFLUSH, &bruto) == 0) ativo_ = true;
}

// É esta linha que separa "o terminal do estudante volta ao normal" de "ele
// digita `reset` às cegas". A variante quebrada não a tem.
terminal_bruto::~terminal_bruto() {
  if (ativo_) ::tcsetattr(STDIN_FILENO, TCSAFLUSH, &salvo());
  --contador_terminal::vivos;
}

}  // namespace deriva
