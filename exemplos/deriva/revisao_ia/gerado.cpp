#include "gerado.hpp"

#include <numeric>
#include <string_view>
#include <utility>

namespace deriva::revisao {

double sensor_termico::media() const {
  if (leituras_.empty()) return 0.0;
  return std::accumulate(leituras_.begin(), leituras_.end(), 0.0) /
         static_cast<double>(leituras_.size());
}

void painel::acrescentar(std::unique_ptr<sensor_base> s) {
  if (s) sensores_.push_back(std::move(s));
}

double painel::media_geral() const {
  if (sensores_.empty()) return 0.0;
  double soma = 0.0;
  for (const std::unique_ptr<sensor_base>& s : sensores_) soma += s->media();
  return soma / static_cast<double>(sensores_.size());
}

std::vector<achado> defeitos_plantados() {
  return {
      // Os rotulos sao os de `conteudo/mapa.py`, e `build/verifica_numeros.py`
      // recusa o build se divergirem. Ja divergiram: este material numerou a
      // propria rubrica de tres maneiras diferentes.
      {1, "R1 · Posse",
       "leituras_ publico: a invariante que registrar() protege e contornavel"},
      {2, "R5 · Hierarquia",
       "base polimorfica com destrutor nao virtual: ~sensor_termico() nao roda"},
      {3, "R3 · const-correctness",
       "nome() nao e const nem [[nodiscard]], e devolve copia a cada chamada"},
  };
}

namespace revisado {

sensor_termico::sensor_termico(std::string nome) : sensor_base(std::move(nome)) {
  ++vivos;
}
sensor_termico::~sensor_termico() { --vivos; }

bool sensor_termico::registrar(double v) {
  if (v < 0.0) return false;   // a invariante, e agora ela e garantida
  leituras_.push_back(v);
  return true;
}

double sensor_termico::media() const {
  if (leituras_.empty()) return 0.0;
  return std::accumulate(leituras_.begin(), leituras_.end(), 0.0) /
         static_cast<double>(leituras_.size());
}

}  // namespace revisado
}  // namespace deriva::revisao
