#include "deriva/mundo.hpp"

#include <algorithm>
#include <utility>

namespace deriva {

mundo::mundo(mapa m) : setor_(std::move(m)) {}

entidade& mundo::acrescentar(std::unique_ptr<entidade> e) {
  entidades_.push_back(std::move(e));
  return *entidades_.back();
}

bool mundo::livre(vetor2 p) const {
  return setor_.g().dentro(p) && setor_.g().em(p).glifo != '#';
}

void mundo::turno() {
  // Índice em lugar de iterador: `agir` pode acrescentar entidade, e isso
  // invalidaria o iterador. Quem entra durante o turno age no turno seguinte,
  // e essa regra é observável no replay.
  const std::size_t n = entidades_.size();
  for (std::size_t i = 0; i < n; ++i) entidades_[i]->agir(*this);
}

entidade* mundo::primeira_com(char glifo) const {
  const auto it = std::find_if(entidades_.begin(), entidades_.end(),
                               [glifo](const std::unique_ptr<entidade>& e) {
                                 return e->glifo() == glifo;
                               });
  return it == entidades_.end() ? nullptr : it->get();
}

std::unique_ptr<entidade> mundo::retirar_de(vetor2 p) {
  const auto it = std::find_if(entidades_.begin(), entidades_.end(),
                               [p](const std::unique_ptr<entidade>& e) {
                                 return e->pos() == p;
                               });
  if (it == entidades_.end()) return nullptr;
  std::unique_ptr<entidade> saindo = std::move(*it);
  entidades_.erase(it);
  return saindo;
}

std::string mundo::despejar() const {
  std::string s = setor_.despejar();
  // As entidades entram por cima do glifo do terreno, na ordem de inserção.
  const int largura = setor_.g().largura();
  const std::size_t cabeca = s.find('\n', s.find('\n') + 1) + 1;
  for (const std::unique_ptr<entidade>& e : entidades_) {
    const vetor2 p = e->pos();
    if (!setor_.g().dentro(p)) continue;
    const std::size_t i = cabeca +
        static_cast<std::size_t>(p.y) * static_cast<std::size_t>(largura + 1) +
        static_cast<std::size_t>(p.x);
    if (i < s.size()) s[i] = e->glifo();
  }
  s.append("entidades ").append(std::to_string(entidades_.size())).append("\n");
  for (const std::unique_ptr<entidade>& e : entidades_) {
    s.append("  ").append(e->descrever()).append("\n");
  }
  return s;
}

}  // namespace deriva
