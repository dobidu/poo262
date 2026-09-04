#include "deriva/inventario.hpp"

#include <utility>

namespace deriva {

peca::peca(std::string rotulo, int massa)
    : rotulo_(std::move(rotulo)), massa_(massa) {}

inventario::inventario(int capacidade) noexcept
    // `std::clamp` no lugar do min/max aninhado: a capacidade fica entre 0 e
    // 999 sem que ninguém precise ler duas chamadas encaixadas para saber
    // disso. Cuidado com o retorno por referência - aqui o resultado é
    // copiado para um `int`, e é isso que o torna seguro.
    : capacidade_(std::clamp(capacidade, 0, 999)) {}

bool inventario::guardar(std::unique_ptr<componente> c) {
  if (!c) return false;
  if (c->massa() > folga()) return false;
  pecas_.push_back(std::move(c));
  return true;
}

int inventario::massa_total() const {
  // `accumulate` com lambda: o zero inicial é `int`, e é ele que define o tipo
  // da soma. Passar `0.0` daria soma em double sem ninguém pedir.
  return std::accumulate(pecas_.begin(), pecas_.end(), 0,
                         [](int soma, const std::unique_ptr<componente>& c) {
                           return soma + c->massa();
                         });
}

int inventario::folga() const { return capacidade_ - massa_total(); }

const componente* inventario::mais_pesada() const {
  const auto it = std::max_element(
      pecas_.begin(), pecas_.end(),
      [](const std::unique_ptr<componente>& a, const std::unique_ptr<componente>& b) {
        return a->massa() < b->massa();
      });
  return it == pecas_.end() ? nullptr : it->get();
}

std::size_t inventario::contar_se(
    const std::function<bool(const componente&)>& criterio) const {
  return static_cast<std::size_t>(std::count_if(
      pecas_.begin(), pecas_.end(),
      [&criterio](const std::unique_ptr<componente>& c) { return criterio(*c); }));
}

std::size_t inventario::descartar_se(
    const std::function<bool(const componente&)>& criterio) {
  // Erase-remove. Em C++20: std::erase_if(pecas_, ...), uma chamada.
  const auto novo_fim = std::remove_if(
      pecas_.begin(), pecas_.end(),
      [&criterio](const std::unique_ptr<componente>& c) { return criterio(*c); });
  const std::size_t saiu = static_cast<std::size_t>(pecas_.end() - novo_fim);
  pecas_.erase(novo_fim, pecas_.end());
  return saiu;
}

void inventario::ordenar_por_massa() {
  std::sort(pecas_.begin(), pecas_.end(),
            [](const std::unique_ptr<componente>& a,
               const std::unique_ptr<componente>& b) {
              // Desempate pelo rótulo: sem ele, a ordem entre massas iguais
              // seria a que o `sort` quisesse, e o despejo deixaria de ser
              // determinístico - o replay quebraria.
              if (a->massa() != b->massa()) return a->massa() > b->massa();
              return a->rotulo() < b->rotulo();
            });
}

std::string inventario::despejar() const {
  std::string s = "inventario " + std::to_string(massa_total()) + "/" +
                  std::to_string(capacidade_) + " em " +
                  std::to_string(pecas_.size()) + " peca(s)\n";
  for (const std::unique_ptr<componente>& c : pecas_) {
    s.append("  ").append(c->rotulo()).append(" ")
     .append(std::to_string(c->massa()));
    if (c->pecas() > 1) s.append(" (").append(std::to_string(c->pecas())).append(" pecas)");
    s.push_back('\n');
  }
  return s;
}

mochila::mochila(std::string rotulo, int tara)
    : rotulo_(std::move(rotulo)), tara_(tara) {}

int mochila::massa() const {
  return std::accumulate(dentro_.begin(), dentro_.end(), tara_,
                         [](int soma, const std::unique_ptr<componente>& c) {
                           return soma + c->massa();
                         });
}

int mochila::pecas() const {
  return std::accumulate(dentro_.begin(), dentro_.end(), 1,
                         [](int soma, const std::unique_ptr<componente>& c) {
                           return soma + c->pecas();
                         });
}

void mochila::por_dentro(std::unique_ptr<componente> c) {
  if (c) dentro_.push_back(std::move(c));
}

void zerar_inventario() noexcept {
  contador_de_instancias<peca>::zerar();
  contador_de_instancias<mochila>::zerar();
}

}  // namespace deriva
