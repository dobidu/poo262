// v1.7 · Aula 17 - herança múltipla, o diamante e a herança virtual
#ifndef DERIVA_REPARADORA_HPP
#define DERIVA_REPARADORA_HPP

#include <string>
#include <string_view>

#include "deriva/celula.hpp"
#include "deriva/entidade.hpp"

namespace deriva {

/// Interface pura: nenhum dado, nenhum construtor, destrutor virtual.
///
/// Interface pura é o **único** uso de herança múltipla que este material
/// recomenda sem ressalva. Ela não traz estado, então não há o que duplicar,
/// e o diamante que ela formaria é inofensivo.
class i_reparavel {
 public:
  virtual ~i_reparavel() = default;
  [[nodiscard]] virtual bool reparar(celula& c) = 0;
  [[nodiscard]] virtual int reparos_feitos() const = 0;
};

/// Uma sonda que também repara. Herda de `sonda` (que é entidade) e de
/// `i_reparavel`.
///
/// Este é o caso FÁCIL: `i_reparavel` não tem estado, então não há diamante de
/// dados. O caso difícil está em `diamante.hpp`, ao lado, e existe só para ser
/// medido.
class sonda_reparadora final : public sonda, public i_reparavel {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  explicit sonda_reparadora(vetor2 pos, int energia = 120);
  ~sonda_reparadora() override;

  [[nodiscard]] char glifo() const override { return 'R'; }
  [[nodiscard]] std::string_view nome() const override { return "sonda_reparadora"; }

  [[nodiscard]] bool reparar(celula& c) override;
  [[nodiscard]] int reparos_feitos() const override { return reparos_; }

 private:
  int reparos_ = 0;
};

}  // namespace deriva

#endif
