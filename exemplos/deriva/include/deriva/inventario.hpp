// v2.3 · Aula 21 - STL, lambdas e std::clamp
#ifndef DERIVA_INVENTARIO_HPP
#define DERIVA_INVENTARIO_HPP

#include <algorithm>
#include <functional>
#include <memory>
#include <numeric>
#include <string>
#include <string_view>
#include <vector>

#include "deriva/contador_crtp.hpp"

namespace deriva {

/// Uma peça que a sonda carrega.
///
/// Base de um Composite (Aula 25): `massa()` é virtual porque uma mochila
/// dentro da mochila responde somando o que tem dentro. Aqui, na Aula 21, ela
/// é só o elemento sobre o qual os algoritmos operam.
class componente {
 public:
  virtual ~componente() = default;
  componente(const componente&) = delete;
  componente& operator=(const componente&) = delete;

  [[nodiscard]] virtual int massa() const = 0;
  [[nodiscard]] virtual std::string_view rotulo() const = 0;
  [[nodiscard]] virtual int pecas() const { return 1; }

 protected:
  componente() = default;
};

/// Peça simples: massa própria, e nada dentro.
class peca final : public componente, public contador_de_instancias<peca> {
 public:
  peca(std::string rotulo, int massa);

  [[nodiscard]] int massa() const override { return massa_; }
  [[nodiscard]] std::string_view rotulo() const override { return rotulo_; }

 private:
  std::string rotulo_;
  int massa_;
};

/// O inventário da sonda.
///
/// A capacidade é o que faz os algoritmos valerem a pena: sem limite, guardar
/// é `push_back` e pronto. Com limite, aparecem as perguntas que a STL
/// responde em uma linha - o que cabe, o que sai primeiro, qual é o mais
/// pesado, quanto sobra.
///
/// `std::clamp` (C++17) está no cálculo de carga: ele substitui o par
/// `std::min(std::max(...))` aninhado, e devolve **referência**, o que é uma
/// armadilha própria - não alimente `clamp` com temporário e guarde o
/// resultado por referência.
class inventario {
 public:
  explicit inventario(int capacidade) noexcept;

  /// Guarda se couber. Devolve se guardou, e `[[nodiscard]]` porque ignorar a
  /// resposta é perder a peça em silêncio.
  [[nodiscard]] bool guardar(std::unique_ptr<componente> c);

  [[nodiscard]] int massa_total() const;
  [[nodiscard]] int capacidade() const noexcept { return capacidade_; }
  [[nodiscard]] int folga() const;
  [[nodiscard]] std::size_t quantas() const noexcept { return pecas_.size(); }

  /// A peça mais pesada, ou `nullptr` se vazio. `std::max_element` com lambda
  /// de comparação: uma linha, e a intenção fica no lugar da mecânica.
  [[nodiscard]] const componente* mais_pesada() const;

  /// Quantas peças satisfazem o critério. O predicado vem de fora, e é isso
  /// que torna a função útil sem saber o que se vai perguntar.
  [[nodiscard]] std::size_t contar_se(
      const std::function<bool(const componente&)>& criterio) const;

  /// Descarta o que o critério aprovar, e devolve quantas saíram.
  /// Erase-remove: `std::remove_if` empurra para o fim e `erase` corta. Em
  /// C++20 seria `std::erase_if`, que é uma chamada só - e é a razão para
  /// esta linha estar comentada com o nome dele.
  std::size_t descartar_se(const std::function<bool(const componente&)>& criterio);

  /// Ordena por massa decrescente. `std::sort` é instável de propósito; para
  /// preservar a ordem de entrada entre iguais, seria `std::stable_sort`, e a
  /// diferença aparece no despejo.
  void ordenar_por_massa();

  [[nodiscard]] std::string despejar() const;

 private:
  int capacidade_;
  std::vector<std::unique_ptr<componente>> pecas_;
};

/// Composite: uma mochila é um componente que contém componentes.
/// Introduzida aqui porque o inventário já a comporta; o padrão em si é a
/// Aula 25.
class mochila final : public componente, public contador_de_instancias<mochila> {
 public:
  mochila(std::string rotulo, int tara);

  [[nodiscard]] int massa() const override;
  [[nodiscard]] std::string_view rotulo() const override { return rotulo_; }
  [[nodiscard]] int pecas() const override;

  void por_dentro(std::unique_ptr<componente> c);

 private:
  std::string rotulo_;
  int tara_;
  std::vector<std::unique_ptr<componente>> dentro_;
};

void zerar_inventario() noexcept;

}  // namespace deriva

#endif
