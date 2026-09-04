// v1.2 · Aula 12 - posse exclusiva com unique_ptr
#ifndef DERIVA_MUNDO_HPP
#define DERIVA_MUNDO_HPP

#include <cstddef>
#include <memory>
#include <string>
#include <vector>

#include "deriva/entidade.hpp"
#include "deriva/mapa.hpp"
#include "deriva/vetor2.hpp"

namespace deriva {

/// O estado do domínio: um setor e as entidades que estão nele.
///
/// A posse é **exclusiva e declarada no tipo**:
/// `std::vector<std::unique_ptr<entidade>>`. O `mundo` é o dono, e o tipo diz
/// isso sem precisar de comentário. Não há um `delete` em todo o Deriva.
///
/// O par `unique_ptr<entidade>` + destrutor virtual é o que amarra as Aulas 11
/// e 12: sem o destrutor virtual, este vetor destruiria só a parte base de
/// cada objeto, e nenhum aviso apareceria - porque o `delete` mora dentro do
/// `unique_ptr`, num cabeçalho do sistema. É o achado da variante
/// `v1.1-quebrada`.
///
/// `mundo` é movível e não copiável, e isso não é escolha de estilo: copiar
/// exigiria clonar polimorficamente cada entidade, o que é decisão de projeto
/// da Aula 25 (Factory), não operação implícita.
class mundo {
 public:
  explicit mundo(mapa m);

  mundo(const mundo&) = delete;
  mundo& operator=(const mundo&) = delete;
  mundo(mundo&&) noexcept = default;
  mundo& operator=(mundo&&) noexcept = default;
  ~mundo() = default;

  [[nodiscard]] const mapa& setor() const noexcept { return setor_; }
  [[nodiscard]] mapa& setor() noexcept { return setor_; }

  /// Toma posse. O `&&` na assinatura é o contrato: quem chama entrega o
  /// ponteiro e não fica com uma cópia dele.
  entidade& acrescentar(std::unique_ptr<entidade> e);

  /// Célula dentro do setor e sem parede. Não considera entidades: duas podem
  /// ocupar a mesma célula, e é a v2.6 que decide se isso é permitido.
  [[nodiscard]] bool livre(vetor2 p) const;

  /// Um turno para cada entidade, na ordem em que entraram. A ordem é parte
  /// do comportamento observável, e o replay depende dela.
  void turno();

  [[nodiscard]] std::size_t quantas() const noexcept { return entidades_.size(); }
  [[nodiscard]] const entidade& em(std::size_t i) const { return *entidades_[i]; }
  [[nodiscard]] entidade& em(std::size_t i) { return *entidades_[i]; }

  /// A primeira entidade cujo glifo casa, ou `nullptr`. Devolve ponteiro cru
  /// de propósito: é observação, não posse, e o tipo tem de dizer a diferença
  /// (Aula 12).
  [[nodiscard]] entidade* primeira_com(char glifo) const;

  /// Remove quem estiver na posição. Devolve o ponteiro: quem chamou passa a
  /// ser o dono, e se ignorar o retorno o objeto morre - daí o
  /// `[[nodiscard]]`.
  [[nodiscard]] std::unique_ptr<entidade> retirar_de(vetor2 p);

  /// Render determinístico: o setor com as entidades por cima, e a listagem.
  /// Mesma entrada, mesma saída, byte a byte.
  [[nodiscard]] std::string despejar() const;

 private:
  mapa setor_;
  std::vector<std::unique_ptr<entidade>> entidades_;
};

}  // namespace deriva

#endif
