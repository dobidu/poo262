#include "deriva/reparadora.hpp"

namespace deriva {

sonda_reparadora::sonda_reparadora(vetor2 pos, int energia)
    : sonda(pos, energia) {
  // A ordem de construção é: entidade, sonda, i_reparavel, sonda_reparadora.
  // Bases antes de membros, e bases na ordem de DECLARAÇÃO da lista de
  // herança - não na ordem em que a lista de inicialização as menciona
  // (Aula 17).
  ++vivos;
  ++criados;
}

sonda_reparadora::~sonda_reparadora() { --vivos; }

bool sonda_reparadora::reparar(celula& c) {
  if (energia() < 10) return false;
  if (c.glifo != '#') return false;      // só parede se repara
  c.glifo = '.';                          // vira piso transitável
  c.massa = 0;
  gastar(10);
  ++reparos_;
  return true;
}

}  // namespace deriva
