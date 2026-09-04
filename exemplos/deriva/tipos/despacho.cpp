#include "despacho.hpp"

#include <typeinfo>

namespace deriva::tipos {

fahrenheit para_fahrenheit(celsius c) {
  return fahrenheit(c.valor * 9.0 / 5.0 + 32.0);
}

std::string resolver(const colisao& a, const colisao& b) {
  // Duas perguntas de tipo, uma para cada operando, porque `virtual` resolve
  // por um só. Com N tipos, esta função cresce com N² - e é exatamente esse
  // crescimento que faz o Visitor existir.
  const bool a_sonda = dynamic_cast<const sonda_c*>(&a) != nullptr;
  const bool b_sonda = dynamic_cast<const sonda_c*>(&b) != nullptr;

  if (a_sonda && b_sonda) return "sonda x sonda: as duas param";
  if (a_sonda && !b_sonda) return "sonda x parede: a sonda para";
  if (!a_sonda && b_sonda) return "parede x sonda: a sonda para";
  return "parede x parede: nada acontece";
}

}  // namespace deriva::tipos
