// Aula 07/11 - os números que os interativos exibem, aferidos pelo compilador
#ifndef DERIVA_LEIAUTE_HPP
#define DERIVA_LEIAUTE_HPP

#include "deriva/vetor2.hpp"

namespace deriva::leiaute {

/// Este cabeçalho não entra no jogo: existe para que os números que os
/// interativos do site mostram sejam os que o g++ realmente produz.
///
/// A hierarquia de verdade - `entidade` → `sonda`/`drone`/`item` - chega na
/// v1.0 (Aula 10). O par abaixo é o mínimo que responde à pergunta da Aula
/// 11: quanto custa o `vptr`?

/// Sem nenhum método virtual: não há vtable, e portanto não há `vptr`.
struct entidade_simples {
  vetor2 pos;
};
struct drone_simples : entidade_simples {};

/// Com um método virtual: o compilador põe um ponteiro para a vtable como
/// primeiro campo do objeto. São 8 bytes por OBJETO, não por classe.
struct entidade {
  vetor2 pos;
  virtual ~entidade() = default;
  virtual void desenhar() const = 0;
};
struct drone : entidade {
  void desenhar() const override {}
};

/// E quando a derivada acrescenta dado, o custo do vptr não desaparece - ele
/// se soma. É a v1.2, quando o drone ganha carga.
struct drone_com_carga : entidade {
  int carga = 0;
  void desenhar() const override {}
};

static_assert(sizeof(entidade_simples) == 8, "só a posição");
static_assert(sizeof(drone_simples) == 8, "herdar de classe não-polimórfica é grátis");
static_assert(sizeof(entidade) == 16, "8 do vptr + 8 da posição");
static_assert(sizeof(drone) == 16, "a derivada sem dado novo não cresce");
static_assert(sizeof(drone_com_carga) == 24, "8 vptr + 8 pos + 4 carga + 4 de padding");

}  // namespace deriva::leiaute

#endif
