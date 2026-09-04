#include "deriva/apresentacao.hpp"

#include <utility>

#include "deriva/mundo.hpp"

namespace deriva {

void apresentacao_em_texto::desenhar(const mundo& m) { saida_.append(m.despejar()); }

void apresentacao_em_texto::mensagem(std::string_view texto) {
  saida_.append("> ").append(texto).push_back('\n');
}

bool mover_sonda::executar(mundo& m) {
  entidade* s = m.primeira_com('@');
  if (!s) return false;
  const vetor2 alvo = s->pos() + delta_;
  if (!m.livre(alvo)) return false;
  de_onde_ = s->pos();
  s->mover_para(alvo);
  executou_ = true;
  return true;
}

void mover_sonda::desfazer(mundo& m) {
  if (!executou_) return;
  if (entidade* s = m.primeira_com('@')) s->mover_para(de_onde_);
  executou_ = false;
}

bool historico::aplicar(std::unique_ptr<i_comando> c, mundo& m) {
  if (!c) return false;
  if (!c->executar(m)) return false;   // o que não deu certo não entra na pilha
  feitos_.push_back(std::move(c));
  return true;
}

bool historico::desfazer_ultimo(mundo& m) {
  if (feitos_.empty()) return false;
  feitos_.back()->desfazer(m);
  feitos_.pop_back();
  return true;
}

std::string historico::despejar() const {
  std::string s = "historico " + std::to_string(feitos_.size()) + "\n";
  for (const std::unique_ptr<i_comando>& c : feitos_) {
    s.append("  ").append(c->nome()).push_back('\n');
  }
  return s;
}

void registro_em_memoria::aconteceu(std::string_view evento) {
  eventos_.emplace_back(evento);
}

std::unique_ptr<entidade> criar_por_glifo(char glifo, vetor2 pos) {
  // A tabela é aqui, e só aqui. Acrescentar uma entidade nova é acrescentar um
  // caso - e nada no carregador de mapa muda.
  switch (glifo) {
    case '@': return std::make_unique<sonda>(pos);
    case 'd': return std::make_unique<drone>(pos);
    case '!': return std::make_unique<item>(pos, "sucata", 3);
    default: return nullptr;   // glifo que não é entidade: o terreno cuida
  }
}

estrategia estrategia_de_patrulha(vetor2 rumo) {
  // A captura é por VALOR, e é obrigatório que seja: a lambda sobrevive à
  // chamada que a criou, e capturar `rumo` por referência deixaria uma
  // referência pendurada. É a mesma armadilha do `string_view` da Aula 03,
  // noutra roupa.
  return [rumo](const entidade& e, const mundo& m) {
    const vetor2 alvo = e.pos() + rumo;
    return m.livre(alvo) ? alvo : e.pos();
  };
}

estrategia estrategia_de_perseguicao(char glifo_alvo) {
  return [glifo_alvo](const entidade& e, const mundo& m) {
    const entidade* alvo = m.primeira_com(glifo_alvo);
    if (!alvo) return e.pos();
    // Um passo na direção que mais reduz a distância de Manhattan.
    const vetor2 d = alvo->pos() - e.pos();
    const vetor2 passo = (d.x != 0) ? vetor2{d.x > 0 ? 1 : -1, 0}
                                    : vetor2{0, d.y > 0 ? 1 : -1};
    const vetor2 candidato = e.pos() + passo;
    return m.livre(candidato) ? candidato : e.pos();
  };
}

estrategia estrategia_parada() {
  return [](const entidade& e, const mundo&) { return e.pos(); };
}

}  // namespace deriva
