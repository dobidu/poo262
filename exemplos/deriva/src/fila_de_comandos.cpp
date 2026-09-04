#include "deriva/fila_de_comandos.hpp"

#include <thread>
#include <utility>

namespace deriva {

void fila_de_comandos::empurrar(std::string comando) {
  {
    const std::scoped_lock trava(mutex_);
    if (fechada_) return;
    fila_.push_back(std::move(comando));
  }
  // Notificar FORA da região travada: quem acorda tentaria travar de imediato,
  // e acordar antes de destravar custa uma ida e volta a mais no escalonador.
  tem_coisa_.notify_one();
}

std::optional<std::string> fila_de_comandos::puxar() {
  std::unique_lock trava(mutex_);
  // O predicado no `wait` não é conveniência: sem ele, um despertar espúrio
  // faria a thread seguir com a fila vazia. Ele é reavaliado a cada despertar,
  // e é o que torna a espera correta.
  tem_coisa_.wait(trava, [this] { return !fila_.empty() || fechada_; });
  if (fila_.empty()) return std::nullopt;   // fechada e vazia: fim
  std::string c = std::move(fila_.front());
  fila_.pop_front();
  return c;
}

std::optional<std::string> fila_de_comandos::tentar_puxar() {
  const std::scoped_lock trava(mutex_);
  if (fila_.empty()) return std::nullopt;
  std::string c = std::move(fila_.front());
  fila_.pop_front();
  return c;
}

void fila_de_comandos::fechar() {
  {
    const std::scoped_lock trava(mutex_);
    fechada_ = true;
  }
  tem_coisa_.notify_all();
}

bool fila_de_comandos::fechada() const {
  const std::scoped_lock trava(mutex_);
  return fechada_;
}

std::size_t fila_de_comandos::tamanho() const {
  const std::scoped_lock trava(mutex_);
  return fila_.size();
}

std::string exercitar_fila(int quantos) {
  fila_de_comandos fila;
  std::string consumido;

  std::thread produtora([&fila, quantos] {
    for (int i = 0; i < quantos; ++i) fila.empurrar("cmd" + std::to_string(i));
    fila.fechar();
  });

  // O consumidor é um só, e é isso que preserva a ordem. Com dois, a saída
  // deixaria de ser determinística e o replay não serviria.
  while (const std::optional<std::string> c = fila.puxar()) {
    consumido.append(*c).push_back(' ');
  }
  produtora.join();
  return consumido;
}

}  // namespace deriva
