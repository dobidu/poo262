#include "deriva/estacao.hpp"

#include <utility>

namespace deriva {

no_estacao::no_estacao(std::string nome) : nome_(std::move(nome)) {
  ++vivos;
  ++criados;
}

no_estacao::~no_estacao() { --vivos; }

void no_estacao::ligar(const std::shared_ptr<no_estacao>& a,
                       const std::shared_ptr<no_estacao>& b) {
  a->adiante_.push_back(b);   // posse: a contagem de b sobe
  b->volta_ = a;              // observação: a contagem de a NÃO sobe
}

std::string percorrer(const std::shared_ptr<no_estacao>& raiz) {
  std::string s;
  if (!raiz) return s;
  s.append(raiz->nome());
  for (const std::shared_ptr<no_estacao>& proximo : raiz->adiante()) {
    s.append(" -> ").append(percorrer(proximo));
  }
  return s;
}

void zerar_estacao() noexcept {
  no_estacao::vivos = 0;
  no_estacao::criados = 0;
}

}  // namespace deriva
