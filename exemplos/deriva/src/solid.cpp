#include "deriva/solid.hpp"

namespace deriva::solid {

std::string empurrar_todos(std::vector<obstaculo*>& quais, vetor2 delta) {
  // Nenhum try/catch, e é de propósito: esta função foi escrita contra a
  // promessa da base, e a promessa diz que `mover` não lança. Acrescentar
  // try/catch aqui seria pagar pela violação em vez de corrigi-la - e teria de
  // ser acrescentado em toda função que use `obstaculo&`.
  std::string s;
  for (obstaculo* o : quais) {
    const vetor2 onde = o->mover(delta);
    s.append(std::to_string(onde.x)).append(",")
     .append(std::to_string(onde.y)).append(" ");
  }
  return s;
}

}  // namespace deriva::solid
