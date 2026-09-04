#include "deriva/entidade.hpp"

#include <utility>

#include "deriva/mundo.hpp"

namespace deriva {

std::string entidade::descrever() const {
  // A moldura é da base, o glifo e o nome são da derivada. Nenhuma derivada
  // reescreve este texto, e nenhuma precisa.
  std::string s;
  s.push_back(glifo());
  s.append(" ").append(nome());
  s.append(" @ ").append(std::to_string(pos().x)).append(",")
   .append(std::to_string(pos().y));
  return s;
}

void sonda::gastar(int quanto) noexcept {
  energia_ -= quanto;
  if (energia_ < 0) energia_ = 0;
}

void sonda::agir(mundo& m) {
  // A sonda não decide sozinha: quem a move é o comando do jogador, e o turno
  // dela só cobra a energia da inspeção. É a v2.6 que transforma isto em
  // Command (Aula 25).
  if (energia_ > 0) gastar(1);
  (void)m;
}

void drone::agir(mundo& m) {
  const vetor2 alvo{pos().x + rumo_.x, pos().y + rumo_.y};
  if (m.livre(alvo)) {
    mover_para(alvo);
  } else {
    rumo_ = {-rumo_.x, -rumo_.y};   // bateu: inverte, e tenta no turno seguinte
  }
}

item::item(vetor2 pos, std::string nome, int massa) noexcept
    : entidade(pos), nome_(std::move(nome)), massa_(massa) {
  ++vivos;
  ++criados;
}

int entidades_vivas() noexcept { return sonda::vivos + drone::vivos + item::vivos; }

void zerar_entidades() noexcept {
  sonda::vivos = sonda::criados = 0;
  drone::vivos = drone::criados = 0;
  item::vivos = item::criados = 0;
}

}  // namespace deriva
