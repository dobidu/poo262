// v0.1 · Aula 07 - encapsulamento, const-correctness, [[nodiscard]]
#ifndef DERIVA_VETOR2_HPP
#define DERIVA_VETOR2_HPP

namespace deriva {

/// Posição ou deslocamento na grade da estação, em células.
///
/// É agregado de propósito: não há invariante a proteger - qualquer par de
/// inteiros é um vetor2 válido. Encapsular o que não tem invariante só
/// acrescenta cerimônia (Aula 07).
///
/// Os operadores aritméticos chegam na v1.5 (Aula 15). Aqui só o que a v0.1
/// precisa: comparação, e ela é `constexpr` porque pode ser.
struct vetor2 {
  int x = 0;
  int y = 0;

  [[nodiscard]] constexpr bool operator==(const vetor2& o) const noexcept {
    return x == o.x && y == o.y;
  }
  [[nodiscard]] constexpr bool operator!=(const vetor2& o) const noexcept {
    return !(*this == o);
  }

  // v1.5 · Aula 15. Os compostos são MEMBROS porque modificam o objeto da
  // esquerda; os binários são funções LIVRES, logo abaixo, porque tratam os
  // dois lados igual. Escrever `+` em termos de `+=` é a forma que não
  // duplica a regra.
  constexpr vetor2& operator+=(const vetor2& o) noexcept {
    x += o.x;
    y += o.y;
    return *this;
  }
  constexpr vetor2& operator-=(const vetor2& o) noexcept {
    x -= o.x;
    y -= o.y;
    return *this;
  }
  constexpr vetor2& operator*=(int k) noexcept {
    x *= k;
    y *= k;
    return *this;
  }

  /// Distância de Manhattan, que é a métrica da grade: a sonda não anda em
  /// diagonal, então a distância euclidiana mentiria sobre o número de turnos.
  [[nodiscard]] constexpr int manhattan(const vetor2& o) const noexcept {
    const int dx = x > o.x ? x - o.x : o.x - x;
    const int dy = y > o.y ? y - o.y : o.y - y;
    return dx + dy;
  }
};

// Funções livres: simétricas por construção, e é isso que as torna a forma
// idiomática. Um `operator+` membro aceitaria `a + b` e recusaria conversões
// do lado esquerdo.
[[nodiscard]] constexpr vetor2 operator+(vetor2 a, const vetor2& b) noexcept {
  return a += b;
}
[[nodiscard]] constexpr vetor2 operator-(vetor2 a, const vetor2& b) noexcept {
  return a -= b;
}
[[nodiscard]] constexpr vetor2 operator*(vetor2 v, int k) noexcept { return v *= k; }
[[nodiscard]] constexpr vetor2 operator*(int k, vetor2 v) noexcept { return v *= k; }

/// Ordem total, para usar `vetor2` como chave de `std::map` e para que o
/// despejo tenha ordem estável - o replay depende disso.
[[nodiscard]] constexpr bool operator<(const vetor2& a, const vetor2& b) noexcept {
  return a.y != b.y ? a.y < b.y : a.x < b.x;
}

static_assert(sizeof(vetor2) == 8, "dois int, sem padding: é o caso mais simples");

// Os operadores são `constexpr`, então o compilador afirma o comportamento:
// se um deles quebrar, o Deriva não compila.
static_assert(vetor2{1, 2} + vetor2{3, 4} == vetor2{4, 6});
static_assert(vetor2{5, 5} - vetor2{1, 2} == vetor2{4, 3});
static_assert(vetor2{2, 3} * 3 == vetor2{6, 9});
static_assert(2 * vetor2{2, 3} == vetor2{4, 6});
static_assert(vetor2{0, 0}.manhattan({3, 4}) == 7);
static_assert(vetor2{1, 0} < vetor2{0, 1}, "a ordem é por fileira, depois coluna");

}  // namespace deriva

#endif
