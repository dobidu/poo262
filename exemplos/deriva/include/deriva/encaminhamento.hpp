// v1.4 · Aula 14 - encaminhamento perfeito, como panorama
#ifndef DERIVA_ENCAMINHAMENTO_HPP
#define DERIVA_ENCAMINHAMENTO_HPP

#include <memory>
#include <string>
#include <type_traits>
#include <utility>
#include <vector>

namespace deriva {

/// Registro do que aconteceu com cada argumento. É o que torna o
/// encaminhamento observável em vez de afirmado.
struct como_chegou {
  inline static std::vector<std::string> traco;
  static void limpar() { traco.clear(); }
};

/// Um tipo que anota se foi copiado ou movido.
class carga_marcada {
 public:
  explicit carga_marcada(std::string rotulo) : rotulo_(std::move(rotulo)) {
    como_chegou::traco.push_back("construida " + rotulo_);
  }
  carga_marcada(const carga_marcada& o) : rotulo_(o.rotulo_) {
    como_chegou::traco.push_back("COPIADA " + rotulo_);
  }
  carga_marcada(carga_marcada&& o) noexcept : rotulo_(std::move(o.rotulo_)) {
    como_chegou::traco.push_back("MOVIDA " + rotulo_);
  }
  [[nodiscard]] const std::string& rotulo() const noexcept { return rotulo_; }

 private:
  std::string rotulo_;
};

/// Fábrica **sem** encaminhamento: recebe por `const&` e copia sempre.
///
/// É o que se escreve por primeiro, e funciona - ao custo de uma cópia que o
/// chamador não pediu e não vê.
template <class T>
[[nodiscard]] std::unique_ptr<T> criar_copiando(const T& original) {
  return std::make_unique<T>(original);
}

/// Fábrica **com** encaminhamento perfeito.
///
/// `T&&` num parâmetro de template dedutível NÃO é referência a rvalue: é
/// referência universal, e ela deduz `T` como `X&` para lvalue e como `X` para
/// rvalue. O colapso de referências faz `X& &&` virar `X&`, e é por isso que a
/// mesma assinatura serve para os dois casos.
///
/// `std::forward<T>(x)` devolve `x` na categoria de valor com que ele chegou.
/// Trocá-lo por `std::move(x)` moveria SEMPRE - inclusive de um lvalue que o
/// chamador ainda vai usar, e esse é o defeito clássico deste idioma.
template <class T, class... Args>
[[nodiscard]] std::unique_ptr<T> criar_encaminhando(Args&&... args) {
  return std::make_unique<T>(std::forward<Args>(args)...);
}

/// A prova de que a dedução é a que se diz. `constexpr`, então o compilador
/// responde sem executar.
template <class T>
[[nodiscard]] constexpr bool deduziu_lvalue(T&&) {
  return std::is_lvalue_reference_v<T>;
}

}  // namespace deriva

#endif
