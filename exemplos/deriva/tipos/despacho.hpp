// Aula 05 - classificação de linguagens e sistemas de tipos
#ifndef DERIVA_TIPOS_DESPACHO_HPP
#define DERIVA_TIPOS_DESPACHO_HPP

#include <string>
#include <string_view>
#include <type_traits>

namespace deriva::tipos {

// ===========================================================================
// Os eixos da Aula 05, cada um com o que C++ faz de fato - e não com o que se
// costuma dizer que ele faz.
// ===========================================================================

/// EIXO 1 · estático × dinâmico. C++ é estaticamente tipado: o tipo é
/// propriedade da EXPRESSÃO, e o compilador o conhece. Estas três funções não
/// executam nada, e ainda assim respondem.
template <class T>
[[nodiscard]] constexpr std::string_view classificar() {
  if constexpr (std::is_integral_v<T>) return "inteiro";
  else if constexpr (std::is_floating_point_v<T>) return "ponto flutuante";
  else if constexpr (std::is_pointer_v<T>) return "ponteiro";
  else if constexpr (std::is_class_v<T>) return "classe";
  else return "outro";
}

/// EIXO 2 · forte × fraco. C++ é forte por padrão e fraco por convite: a
/// conversão implícita existe, e `explicit` é como se recusa o convite.
struct celsius {
  double valor;
};
struct fahrenheit {
  // Sem `explicit`, `fahrenheit f = 30.0;` compilaria, e 30 graus Celsius
  // viraria 30 Fahrenheit em silêncio. Com ele, o compilador exige a
  // conversão escrita - e é aí que o sistema de tipos fica forte.
  explicit fahrenheit(double v) : valor(v) {}
  double valor;
};

[[nodiscard]] fahrenheit para_fahrenheit(celsius c);

/// EIXO 3 · despacho simples × múltiplo. C++ tem despacho SIMPLES: `virtual`
/// resolve por UM tipo, o do objeto. Despacho por dois tipos ao mesmo tempo
/// não existe na linguagem, e o padrão Visitor é o contorno.
struct colisao {
  virtual ~colisao() = default;
  [[nodiscard]] virtual std::string_view quem() const = 0;
};
struct sonda_c final : colisao {
  [[nodiscard]] std::string_view quem() const override { return "sonda"; }
};
struct parede_c final : colisao {
  [[nodiscard]] std::string_view quem() const override { return "parede"; }
};

/// Despacho por DOIS tipos, feito à mão, porque a linguagem não o faz. O
/// nome desta função é a prova do ponto: se houvesse despacho múltiplo, ela
/// não existiria.
[[nodiscard]] std::string resolver(const colisao& a, const colisao& b);

/// EIXO 4 · herança, composição e traits. Em C++ o "trait" é um template que
/// responde sobre um tipo, e não uma construção da linguagem como em Rust ou
/// Scala. Este é um trait de verdade, escrito à mão.
template <class T, class = void>
struct tem_glifo : std::false_type {};

template <class T>
struct tem_glifo<T, std::void_t<decltype(std::declval<const T&>().glifo())>>
    : std::true_type {};

template <class T>
inline constexpr bool tem_glifo_v = tem_glifo<T>::value;

struct com_glifo {
  [[nodiscard]] char glifo() const { return '@'; }
};
struct sem_glifo {
  int x = 0;
};

}  // namespace deriva::tipos

#endif
