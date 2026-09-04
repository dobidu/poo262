// v2.0 · Aula 19 - grade<T>, if constexpr e static_assert
#ifndef DERIVA_GRADE_GENERICA_HPP
#define DERIVA_GRADE_GENERICA_HPP

#include <cstddef>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <vector>

#include "deriva/celula.hpp"
#include "deriva/contador_crtp.hpp"
#include "deriva/vetor2.hpp"

namespace deriva {

/// A `grade` da v0.2, agora genérica no que cada posição guarda.
///
/// O que motivou generalizar não foi elegância: a v2.3 precisa de uma grade de
/// `int` para o mapa de distâncias do campo de visão, e a v2.5 de uma grade de
/// `bool` para o que já foi visitado. Copiar a classe três vezes seria a
/// alternativa, e é ela que o template evita.
///
/// `static_assert` na definição, e não no uso: a mensagem que o estudante lê
/// quando erra é a nossa, e não seiscentas linhas de instanciação.
template <class T>
class grade_de : public contador_de_instancias<grade_de<T>> {
  static_assert(std::is_default_constructible_v<T>,
                "grade_de<T> precisa saber criar celula vazia: T sem construtor "
                "padrao nao serve");
  static_assert(!std::is_reference_v<T>, "grade de referencias nao existe");
  // `std::vector<bool>` é a especialização mais famosa da biblioteca padrão, e
  // a mais lamentada: ela empacota os bits, então `operator[]` devolve um
  // PROXY e não um `bool&`. Uma grade que promete `T&` não pode ser
  // instanciada com `bool`, e a mensagem abaixo é o que o estudante lê em vez
  // de "cannot bind non-const lvalue reference to an rvalue".
  //
  // A saída é `char` ou `std::uint8_t`, e a v2.5 usa `char` no mapa do que já
  // foi visitado. É por isso que a Aula 21 diz que `vector<bool>` não é um
  // vetor de bool (Aula 19 e Aula 21).
  static_assert(!std::is_same_v<T, bool>,
                "grade_de<bool> nao existe: std::vector<bool> empacota bits e "
                "devolve proxy, nao bool&. Use char ou std::uint8_t");

 public:
  grade_de(int largura, int altura)
      : largura_(exigir_positivo(largura, "largura")),
        altura_(exigir_positivo(altura, "altura")),
        celulas_(static_cast<std::size_t>(largura_) *
                 static_cast<std::size_t>(altura_)) {}

  [[nodiscard]] int largura() const noexcept { return largura_; }
  [[nodiscard]] int altura() const noexcept { return altura_; }
  [[nodiscard]] bool dentro(vetor2 p) const noexcept {
    return p.x >= 0 && p.y >= 0 && p.x < largura_ && p.y < altura_;
  }

  [[nodiscard]] const T& em(vetor2 p) const { return celulas_[indice(p)]; }
  [[nodiscard]] T& em(vetor2 p) { return celulas_[indice(p)]; }

  void preencher(const T& v) {
    for (T& c : celulas_) c = v;
  }

  /// O despejo depende do que `T` é, e a decisão acontece em tempo de
  /// COMPILAÇÃO. Com `if` comum, os três ramos teriam de ser válidos para
  /// todo `T` - e `c.glifo` não existe em `int`, então nem compilaria. É a
  /// diferença que `if constexpr` faz, e o motivo pelo qual ele substitui
  /// SFINAE (Aula 19).
  [[nodiscard]] std::string despejar() const {
    std::string s;
    for (int y = 0; y < altura_; ++y) {
      for (int x = 0; x < largura_; ++x) {
        const T& c = em({x, y});
        if constexpr (std::is_same_v<T, celula>) {
          s.push_back(c.glifo);
        } else if constexpr (std::is_same_v<T, char>) {
          s.push_back(c ? '+' : '.');
        } else if constexpr (std::is_integral_v<T>) {
          s.push_back(c < 0 ? '#' : static_cast<char>('0' + (c % 10)));
        } else {
          s.push_back('?');
        }
      }
      s.push_back('\n');
    }
    return s;
  }

  [[nodiscard]] std::size_t bytes_das_celulas() const noexcept {
    return celulas_.size() * sizeof(T);
  }

 private:
  [[nodiscard]] static int exigir_positivo(int valor, const char* qual) {
    if (valor <= 0) {
      throw std::invalid_argument(std::string("grade_de: ") + qual +
                                  " precisa ser positiva, recebeu " +
                                  std::to_string(valor));
    }
    return valor;
  }
  [[nodiscard]] std::size_t indice(vetor2 p) const noexcept {
    return static_cast<std::size_t>(p.y) * static_cast<std::size_t>(largura_) +
           static_cast<std::size_t>(p.x);
  }

  int largura_;
  int altura_;
  std::vector<T> celulas_;
};

/// A grade de células continua sendo o caso comum, e ganha um nome curto.
using grade_de_celulas = grade_de<celula>;

/// Herdar do CRTP não custa byte nenhum: base vazia, e o compilador a
/// otimiza. É a diferença entre polimorfismo estático e dinâmico, medida.
static_assert(sizeof(grade_de<celula>) == sizeof(int) * 2 + sizeof(std::vector<celula>),
              "o contador por CRTP nao aumenta o objeto");

}  // namespace deriva

#endif
