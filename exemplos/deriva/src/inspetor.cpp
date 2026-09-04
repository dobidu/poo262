#include "deriva/inspetor.hpp"

#include <typeinfo>

#include "deriva/mundo.hpp"
#include "deriva/reparadora.hpp"

namespace deriva {

std::string inspecionar(const entidade& e) {
  std::string s = e.descrever();

  // A ordem importa: `sonda_reparadora` também É `sonda`, então testá-la
  // depois nunca aconteceria. Perguntar pelo tipo mais derivado primeiro é a
  // armadilha número um de cadeia de dynamic_cast - e é o argumento de que
  // essa cadeia deveria ser uma função virtual.
  if (const auto* r = dynamic_cast<const sonda_reparadora*>(&e)) {
    s.append("  [reparadora, ").append(std::to_string(r->reparos_feitos()))
     .append(" reparo(s), energia ").append(std::to_string(r->energia())).append("]");
  } else if (const auto* sd = dynamic_cast<const sonda*>(&e)) {
    s.append("  [sonda, energia ").append(std::to_string(sd->energia())).append("]");
  } else if (const auto* dr = dynamic_cast<const drone*>(&e)) {
    s.append("  [drone, rumo ").append(std::to_string(dr->rumo().x)).append(",")
     .append(std::to_string(dr->rumo().y)).append("]");
  } else if (const auto* it = dynamic_cast<const item*>(&e)) {
    s.append("  [item, massa ").append(std::to_string(it->massa())).append("]");
  }
  return s;
}

std::string listar_reparadoras(const mundo& m) {
  std::string s;
  int achadas = 0;
  for (std::size_t i = 0; i < m.quantas(); ++i) {
    // `dynamic_cast` para a INTERFACE, e não para a classe concreta: é a
    // pergunta certa, porque o que interessa é a capacidade e não o tipo.
    if (dynamic_cast<const i_reparavel*>(&m.em(i)) != nullptr) {
      s.append("  ").append(m.em(i).descrever()).append("\n");
      ++achadas;
    }
  }
  return "reparadoras " + std::to_string(achadas) + "\n" + s;
}

std::string tipo_cru(const entidade& e) { return typeid(e).name(); }

}  // namespace deriva
