// v2.5 - serializacao versionada: ida e volta
#include <string>

#include <catch2/catch_test_macros.hpp>

#include "deriva/mundo.hpp"
#include "deriva/partida.hpp"

using namespace deriva;

TEST_CASE("serializar e desserializar sao inversas") {
  partida p;
  p.setor = "estacao-01";
  p.sonda = {9, 3};
  p.carga = 7;
  p.turno = 42;
  p.energia = 88;

  const auto lida = partida::desserializar(p.serializar());
  REQUIRE(lida.has_value());
  REQUIRE(lida->setor == p.setor);
  REQUIRE(lida->sonda == p.sonda);
  REQUIRE(lida->carga == p.carga);
  REQUIRE(lida->turno == p.turno);
  REQUIRE(lida->energia == p.energia);
  REQUIRE(lida->serializar() == p.serializar());   // e o texto tambem
}

TEST_CASE("a versao e a primeira linha, porque quem le precisa dela antes") {
  partida p;
  p.setor = "x";
  REQUIRE(p.serializar().find("deriva-partida 2") == 0);
}

// Compatibilidade regressiva: um arquivo da versao 1 nao tem `energia`, e o
// leitor v2 tem de aceitar isso. O valor padrao do membro e o que responde
// por ele - sem esse padrao, a sonda carregaria com zero de energia e
// apareceria morta, que e o defeito classico de migracao de formato.
TEST_CASE("o leitor v2 abre uma partida v1") {
  const std::string v1 =
      "deriva-partida 1\n"
      "setor estacao-01\n"
      "sonda 4 5\n"
      "carga 3\n"
      "turno 10\n";

  const auto lida = partida::desserializar(v1);
  REQUIRE(lida.has_value());
  REQUIRE(lida->versao == 1);
  REQUIRE(lida->sonda == vetor2{4, 5});
  REQUIRE(lida->energia == 100);   // o padrao, e nao zero
}

// A outra ponta: chave desconhecida e PULADA, e nao recusada. E o que permite
// a um leitor v2 abrir um arquivo v3 que so acrescentou campos.
TEST_CASE("chave desconhecida e pulada, nao recusa o arquivo") {
  const std::string v3 =
      "deriva-partida 2\n"
      "setor estacao-01\n"
      "sonda 1 1\n"
      "reputacao 55\n"
      "carga 0\n";
  const auto lida = partida::desserializar(v3);
  REQUIRE(lida.has_value());
  REQUIRE(lida->setor == "estacao-01");
  REQUIRE(lida->sonda == vetor2{1, 1});
}

TEST_CASE("texto que nao e partida devolve nullopt, e nao lanca") {
  REQUIRE_FALSE(partida::desserializar("").has_value());
  REQUIRE_FALSE(partida::desserializar("outra-coisa 1\n").has_value());
  REQUIRE_FALSE(partida::desserializar("deriva-partida 99\nsetor x\n").has_value());
  REQUIRE_FALSE(partida::desserializar("deriva-partida 2\n").has_value());  // sem setor
}

TEST_CASE("extrair de um mundo em execucao") {
  zerar_entidades();
  auto m = mapa::de_texto("#####\n#.@.#\n#####\n", "setor-t");
  mundo w(std::move(*m));
  w.acrescentar(std::make_unique<sonda>(vetor2{2, 1}, 77));

  const partida p = partida::de(w, 5);
  REQUIRE(p.setor == "setor-t");
  REQUIRE(p.sonda == vetor2{2, 1});
  REQUIRE(p.energia == 77);
  REQUIRE(p.turno == 5);
  REQUIRE(p.versao == partida::kVersaoAtual);
}

TEST_CASE("o leitor declara quais versoes entende") {
  const auto v = versoes_aceitas();
  REQUIRE(v.size() == 2);
  REQUIRE(v.front() == 1);
  REQUIRE(v.back() == partida::kVersaoAtual);
}
