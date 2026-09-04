// v0.2 · Aula 08 - RAII com consequência física
#ifndef DERIVA_TERMINAL_BRUTO_HPP
#define DERIVA_TERMINAL_BRUTO_HPP

#include "deriva/contador.hpp"

namespace deriva {

/// Põe o terminal em modo bruto no construtor e o restaura no destrutor.
///
/// É a melhor demonstração de RAII que existe, e não é metáfora: se o
/// destrutor não rodar, o terminal do estudante fica sem eco e sem Enter
/// **depois** que o programa sai. Ele descobre RAII digitando `reset` às
/// cegas.
///
/// A variante `variantes/v0.2-quebrada/` omite o destrutor de propósito.
///
/// Não é copiável nem movível: há exatamente um terminal, e posse de recurso
/// único não se duplica. Declarar as duas apagadas é a **regra do três**
/// (Aula 09) na sua forma mais curta.
class terminal_bruto {
 public:
  terminal_bruto();
  ~terminal_bruto();

  terminal_bruto(const terminal_bruto&) = delete;
  terminal_bruto& operator=(const terminal_bruto&) = delete;

  /// Verdadeiro quando havia um terminal de verdade para alterar. Em teste,
  /// em pipe ou em CI a saída não é tty: o objeto se constrói, conta como
  /// vivo, e não mexe em nada. Sem isso, `ctest` deixaria o terminal de quem
  /// roda os testes em estado imprevisível.
  [[nodiscard]] bool ativo() const noexcept { return ativo_; }

 private:
  bool ativo_ = false;
};

}  // namespace deriva

#endif
