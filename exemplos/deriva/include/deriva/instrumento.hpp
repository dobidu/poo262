// v0.2 · Aula 08 - instrumentação de ciclo de vida
#ifndef DERIVA_INSTRUMENTO_HPP
#define DERIVA_INSTRUMENTO_HPP

#include <string>
#include <string_view>
#include <vector>

namespace deriva {

/// Construtores e destrutores imprimindo a própria execução.
///
/// Substitui o sanitizer que o laboratório não tem: em vez de confiar que a
/// ordem de destruição é a inversa da de construção, o estudante LÊ o traço e
/// compara com o roteiro esperado.
///
/// O traço é gravado num vetor, não em `std::cout`, por dois motivos: teste
/// pode afirmar sobre ele, e a saída do programa não fica poluída. Quem quer
/// ver ao vivo liga `instrumento::ecoar(true)`.
class instrumento {
 public:
  /// Registra um evento. `o_que` é "+" para construção, "-" para destruição,
  /// "!" para exceção lançada.
  static void anotar(std::string_view o_que, std::string_view quem);

  /// Ecoar em stderr, além de gravar. Desligado por padrão.
  static void ecoar(bool ligado) noexcept;

  [[nodiscard]] static const std::vector<std::string>& traco() noexcept;
  static void limpar();

  /// Uma linha por evento, na ordem. É isto que o teste compara.
  [[nodiscard]] static std::string despejo();
};

/// Anota "+nome" ao nascer e "-nome" ao morrer. Membro de quem quiser ser
/// rastreado; é RAII aplicado ao próprio rastreamento.
class marca_de_vida {
 public:
  explicit marca_de_vida(std::string nome);
  ~marca_de_vida();

  marca_de_vida(const marca_de_vida& o);
  marca_de_vida& operator=(const marca_de_vida& o);

  // O movimento anota com sufixo próprio, para que o traço distinga cópia de
  // movimento sem que ninguém precise adivinhar (v1.4 · Aula 14).
  marca_de_vida(marca_de_vida&& o) noexcept;
  marca_de_vida& operator=(marca_de_vida&& o) noexcept;

 private:
  std::string nome_;
};

}  // namespace deriva

#endif
