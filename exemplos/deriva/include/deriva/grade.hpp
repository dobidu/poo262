// v0.2 · Aula 08/09 - construtores, lista de inicialização, regra do ZERO
#ifndef DERIVA_GRADE_HPP
#define DERIVA_GRADE_HPP

#include <cstddef>
#include <vector>

#include "deriva/celula.hpp"
#include "deriva/vetor2.hpp"

namespace deriva {

/// A grade de células da estação.
///
/// Não declara destrutor, cópia, movimento nem atribuição: é a **regra do
/// zero** (Aula 09). O único membro que gerencia recurso é o
/// `std::vector`, e ele já sabe se copiar, se mover e se destruir
/// corretamente. As cinco operações que o compilador gera são melhores do que
/// as que escreveríamos aqui - e não podem ficar desatualizadas quando um
/// membro novo aparecer.
///
/// A variante `variantes/v0.3-quebrada/` faz o oposto: guarda `celula*` cru,
/// declara destrutor e esquece a cópia. É a **caça ao bug 1** da semana 5, e
/// o contador de instâncias vivas é o que a acusa.
class grade {
 public:
  grade(int largura, int altura);

  [[nodiscard]] int largura() const noexcept { return largura_; }
  [[nodiscard]] int altura() const noexcept { return altura_; }
  [[nodiscard]] bool dentro(vetor2 p) const noexcept;

  /// Sem verificação de limite: quem chama já perguntou `dentro()`.
  /// O `operator[]` de `mapa` chega na v1.5 (Aula 15).
  [[nodiscard]] const celula& em(vetor2 p) const;
  [[nodiscard]] celula& em(vetor2 p);

  /// Quantos bytes as células ocupam de fato. Serve à Aula 07: com
  /// `celula_ingenua` este número cresce um terço sem nada mudar de
  /// significado.
  [[nodiscard]] std::size_t bytes_das_celulas() const noexcept;

 private:
  int largura_;
  int altura_;
  std::vector<celula> celulas_;
};

}  // namespace deriva

#endif
