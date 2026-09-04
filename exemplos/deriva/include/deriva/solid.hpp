// v2.6 · Aula 24 - LSP e ISP, escritos para serem violados de propósito
#ifndef DERIVA_SOLID_HPP
#define DERIVA_SOLID_HPP

#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

#include "deriva/vetor2.hpp"

namespace deriva::solid {

// ===========================================================================
// LSP · a violação, e ela não é erro de digitação
//
// `parede` É um obstáculo, e obstáculo tem posição. Herdar parece natural, e o
// código compila. O que ela quebra é a promessa da BASE: `mover` devolve a
// nova posição, e a parede não tem nova posição - então ela lança.
//
// O sintoma não aparece na parede: aparece em toda função que recebe
// `obstaculo&` e chama `mover`, escrita antes de a parede existir e correta
// quando foi escrita.
// ===========================================================================
class obstaculo {
 public:
  virtual ~obstaculo() = default;
  explicit obstaculo(vetor2 pos) noexcept : pos_(pos) {}

  /// A promessa: devolve onde o obstáculo ficou depois de tentar mover.
  /// Nunca lança, e para quem não pode mover a resposta é a posição atual.
  [[nodiscard]] virtual vetor2 mover(vetor2 delta) = 0;
  [[nodiscard]] vetor2 pos() const noexcept { return pos_; }

 protected:
  void definir(vetor2 p) noexcept { pos_ = p; }

 private:
  vetor2 pos_;
};

class caixa final : public obstaculo {
 public:
  using obstaculo::obstaculo;
  [[nodiscard]] vetor2 mover(vetor2 delta) override {
    definir(pos() + delta);
    return pos();
  }
};

/// A VIOLAÇÃO. Compila, e quebra o contrato da base.
class parede_que_lanca final : public obstaculo {
 public:
  using obstaculo::obstaculo;
  [[nodiscard]] vetor2 mover(vetor2) override {
    throw std::logic_error("parede nao se move");
  }
};

/// A correção, e ela não é try/catch: é honrar a promessa. Parede que não se
/// move devolve a posição em que está, e quem chama não precisa saber que ela
/// é parede.
class parede_honesta final : public obstaculo {
 public:
  using obstaculo::obstaculo;
  [[nodiscard]] vetor2 mover(vetor2) override { return pos(); }
};

/// Escrita antes de a parede existir, e correta quando foi escrita. É ela que
/// a violação quebra, e é por isso que LSP se mede no CHAMADOR.
[[nodiscard]] std::string empurrar_todos(std::vector<obstaculo*>& quais,
                                         vetor2 delta);

// ===========================================================================
// ISP · a interface gorda, e a segregação
//
// `i_tudo` obriga quem só desenha a implementar salvar e reparar. O sintoma é
// o método vazio, ou pior, o que lança - e método vazio numa interface é a
// confissão de que ela pede demais.
// ===========================================================================
class i_tudo {
 public:
  virtual ~i_tudo() = default;
  virtual void desenhar() = 0;
  virtual void salvar() = 0;
  virtual void reparar() = 0;
};

/// Quem só desenha, obrigado a mentir em dois métodos.
class so_desenha_gordo final : public i_tudo {
 public:
  void desenhar() override { desenhou = true; }
  void salvar() override {}                       // vazio: a confissão
  void reparar() override {}                      // vazio: a segunda
  bool desenhou = false;
};

/// A segregação: três interfaces, e cada um implementa o que faz.
class i_desenhavel {
 public:
  virtual ~i_desenhavel() = default;
  virtual void desenhar() = 0;
};
class i_salvavel {
 public:
  virtual ~i_salvavel() = default;
  virtual void salvar() = 0;
};

class so_desenha final : public i_desenhavel {
 public:
  void desenhar() override { desenhou = true; }
  bool desenhou = false;
};

class desenha_e_salva final : public i_desenhavel, public i_salvavel {
 public:
  void desenhar() override { desenhou = true; }
  void salvar() override { salvou = true; }
  bool desenhou = false;
  bool salvou = false;
};

/// Quantos métodos cada forma obriga a escrever para quem só desenha.
/// É a métrica de ISP, e ela é contável.
[[nodiscard]] constexpr int metodos_obrigados_gordo() { return 3; }
[[nodiscard]] constexpr int metodos_obrigados_segregado() { return 1; }

}  // namespace deriva::solid

#endif
