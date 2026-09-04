#include "deriva/fov.hpp"

#include <cstdlib>

namespace deriva {

std::vector<vetor2> linha(vetor2 a, vetor2 b) {
  // Bresenham em inteiros. Nenhum ponto flutuante, nenhum arredondamento
  // dependente de plataforma: a mesma entrada dá a mesma linha em qualquer
  // máquina, e é essa propriedade que o replay da Aula 16 compra.
  std::vector<vetor2> pontos;
  int x = a.x, y = a.y;
  const int dx = std::abs(b.x - a.x), dy = std::abs(b.y - a.y);
  const int sx = a.x < b.x ? 1 : -1, sy = a.y < b.y ? 1 : -1;
  int erro = dx - dy;
  for (;;) {
    pontos.push_back({x, y});
    if (x == b.x && y == b.y) break;
    const int e2 = 2 * erro;
    if (e2 > -dy) { erro -= dy; x += sx; }
    if (e2 < dx) { erro += dx; y += sy; }
  }
  return pontos;
}

std::set<vetor2> visiveis(const mapa& m, vetor2 origem, int raio) {
  std::set<vetor2> vistas;
  if (!m.g().dentro(origem)) return vistas;
  vistas.insert(origem);

  for (int dy = -raio; dy <= raio; ++dy) {
    for (int dx = -raio; dx <= raio; ++dx) {
      const vetor2 alvo{origem.x + dx, origem.y + dy};
      if (!m.g().dentro(alvo)) continue;
      if (origem.manhattan(alvo) > raio) continue;   // a métrica é da grade

      for (const vetor2& p : linha(origem, alvo)) {
        vistas.insert(p);
        // A parede é vista, e bloqueia o que está atrás dela.
        if (!(p == origem) && m[p].glifo == '#') break;
      }
    }
  }
  return vistas;
}

std::string despejar_fov(const mapa& m, vetor2 origem, int raio) {
  const std::set<vetor2> vistas = visiveis(m, origem, raio);
  std::string s;
  s.append("fov ").append(std::to_string(origem.x)).append(",")
   .append(std::to_string(origem.y)).append(" raio ")
   .append(std::to_string(raio)).append(" vistas ")
   .append(std::to_string(vistas.size())).append("\n");
  for (int y = 0; y < m.g().altura(); ++y) {
    for (int x = 0; x < m.g().largura(); ++x) {
      const vetor2 p{x, y};
      s.push_back(vistas.count(p) ? (p == origem ? '@' : m[p].glifo) : ' ');
    }
    s.push_back('\n');
  }
  return s;
}

}  // namespace deriva
