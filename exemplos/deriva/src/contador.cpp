#include "deriva/contador.hpp"

namespace deriva {

void zerar_contadores() noexcept {
  contador_mapa::vivos = 0;
  contador_mapa::criados = 0;
  contador_terminal::vivos = 0;
  contador_terminal::criados = 0;
}

int total_vivos() noexcept {
  return contador_mapa::vivos + contador_terminal::vivos;
}

}  // namespace deriva
