#include "deriva/partida.hpp"

#include <sstream>

#include "deriva/entidade.hpp"
#include "deriva/mundo.hpp"

namespace deriva {

std::string partida::serializar() const {
  // A ordem das linhas é fixa e a versão vem primeiro. Ordem estável é o que
  // permite comparar dois saves com `diff`, e é a mesma razão do replay.
  std::ostringstream os;
  os << "deriva-partida " << versao << '\n'
     << "setor " << setor << '\n'
     << "sonda " << sonda.x << ' ' << sonda.y << '\n'
     << "carga " << carga << '\n'
     << "turno " << turno << '\n'
     << "energia " << energia << '\n';
  return os.str();
}

std::optional<partida> partida::desserializar(std::string_view texto) {
  // Chaves, e não parênteses. `std::istringstream is(std::string(texto));`
  // é a *most vexing parse*: o compilador lê isso como a DECLARAÇÃO de uma
  // função chamada `is` que devolve `istringstream` e recebe um `std::string`,
  // e depois reclama que não há `operator>>` para função. A inicialização
  // uniforme com `{}` da Aula 03 não tem essa ambiguidade, e é por isso que o
  // material a recomenda desde o começo.
  std::istringstream is{std::string(texto)};
  std::string chave;
  partida p;
  bool tem_cabeca = false;

  if (!(is >> chave) || chave != "deriva-partida") return std::nullopt;
  if (!(is >> p.versao)) return std::nullopt;
  if (p.versao < 1 || p.versao > kVersaoAtual) return std::nullopt;
  tem_cabeca = true;

  while (is >> chave) {
    if (chave == "setor") { if (!(is >> p.setor)) return std::nullopt; }
    else if (chave == "sonda") { if (!(is >> p.sonda.x >> p.sonda.y)) return std::nullopt; }
    else if (chave == "carga") { if (!(is >> p.carga)) return std::nullopt; }
    else if (chave == "turno") { if (!(is >> p.turno)) return std::nullopt; }
    else if (chave == "energia") { if (!(is >> p.energia)) return std::nullopt; }
    else {
      // Chave desconhecida: PULA em vez de recusar. É o que permite a um
      // leitor v2 abrir um arquivo v3 que só acrescentou campos - e é a
      // decisão que separa formato extensível de formato frágil.
      std::string resto;
      std::getline(is, resto);
    }
  }
  if (!tem_cabeca || p.setor.empty()) return std::nullopt;

  // Um arquivo v1 não tem `energia`, e o valor padrão do membro é o que
  // responde por ele. Sem esse padrão, a partida antiga carregaria com zero e
  // a sonda apareceria morta - o defeito clássico de migração de formato.
  return p;
}

partida partida::de(const mundo& m, int turno) {
  partida p;
  p.setor = std::string(m.setor().nome());
  p.turno = turno;
  if (const entidade* s = m.primeira_com('@')) {
    p.sonda = s->pos();
    // `deriva::sonda` qualificado, e não `sonda`: o membro `partida::sonda`,
    // que é um `vetor2`, sombreia o nome da classe dentro deste escopo, e a
    // busca de nome encontra o membro primeiro. O compilador diz "invalid use
    // of member in static member function", que é uma mensagem que não ajuda
    // ninguém a entender que o problema é sombreamento.
    if (const auto* sd = dynamic_cast<const deriva::sonda*>(s)) {
      p.energia = sd->energia();
    }
  }
  return p;
}

std::vector<int> versoes_aceitas() { return {1, partida::kVersaoAtual}; }

}  // namespace deriva
