// Anexo A · v2.1 - Concepts e Ranges, FORA do padrão-alvo
#ifndef DERIVA_C20_RESTRICOES_HPP
#define DERIVA_C20_RESTRICOES_HPP

// Este arquivo é C++20 e não entra no build padrão. Compila com
//     cmake -S . -B build -DDERIVA_COM_CPP20=ON
// num alvo separado, e nada do material obrigatório depende dele.
//
// A razão de existir é a do Anexo A: mostrar para onde a linguagem foi, sem
// que nenhum exemplo da disciplina passe a exigir C++20. O padrão-alvo é
// C++17, e o laboratório tem g++ 13 - que suporta os dois; a restrição é
// pedagógica, e não técnica.
#if __cplusplus < 202002L
#error "restricoes.hpp e C++20: compile o alvo deriva_c20"
#endif

#include <concepts>
#include <ranges>
#include <string>
#include <type_traits>
#include <vector>

#include "deriva/celula.hpp"
#include "deriva/vetor2.hpp"

namespace deriva::c20 {

/// O que `grade_de<T>` exige de `T`, dito como CONCEPT em vez de como
/// `static_assert`.
///
/// A diferença que se vê: a mensagem de erro. Com `static_assert`, o
/// compilador aponta a linha do assert e o estudante lê a nossa frase. Com
/// `concept`, ele aponta a CHAMADA e diz qual restrição falhou - o que é
/// melhor, e é a razão de o C++20 ter os concepts.
template <class T>
concept guardavel = std::default_initializable<T> && !std::is_reference_v<T> &&
                    !std::same_as<T, bool>;

/// A mesma grade da v2.0, agora restrita. `requires` na declaração, e não
/// `enable_if` no tipo de retorno.
template <guardavel T>
class grade_restrita {
 public:
  grade_restrita(int largura, int altura)
      : largura_(largura), celulas_(static_cast<std::size_t>(largura * altura)) {}

  [[nodiscard]] T& em(vetor2 p) {
    return celulas_[static_cast<std::size_t>(p.y * largura_ + p.x)];
  }
  [[nodiscard]] const T& em(vetor2 p) const {
    return celulas_[static_cast<std::size_t>(p.y * largura_ + p.x)];
  }
  [[nodiscard]] auto todas() const { return std::views::all(celulas_); }
  [[nodiscard]] std::size_t tamanho() const noexcept { return celulas_.size(); }

 private:
  int largura_;
  std::vector<T> celulas_;
};

/// Ranges no lugar do laço, sobre as células da grade.
///
/// O que se ganha é composição sem contêiner intermediário: `filter` e
/// `transform` são vistas preguiçosas, e nada é copiado até alguém iterar. Em
/// C++17 o equivalente seria um `copy_if` para um vetor temporário e um
/// `transform` depois - dois laços e uma alocação.
[[nodiscard]] inline std::string glifos_de_parede(const grade_restrita<celula>& g) {
  std::string s;
  for (const celula& c : g.todas()
                             | std::views::filter([](const celula& x) {
                                 return x.glifo == '#';
                               })
                             | std::views::take(10)) {
    s.push_back(c.glifo);
  }
  return s;
}

/// A restrição que o `concept` recusa, e a mensagem que ele produz.
/// `grade_restrita<bool>` não compila, e o erro nomeia `guardavel`.
static_assert(guardavel<celula>);
static_assert(guardavel<int>);
static_assert(!guardavel<bool>);
static_assert(!guardavel<int&>);

}  // namespace deriva::c20

#endif
