// Aula 03 - a armadilha de tempo de vida de string_view
#include <cstring>
#include <string>
#include <string_view>
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "deriva/mapa.hpp"

// Os quatro casos de tempo de vida que o LAB-02 (Aula 03) cobra. Nenhum deles
// lê memória liberada: demonstrar comportamento indefinido num teste seria
// trocar uma lição por um teste que às vezes passa. O que cada caso prova é a
// ESTRUTURA da pendura - de quem são os bytes, e quem os libera.

TEST_CASE("caso 1: a vista nao possui os bytes, ela aponta para eles") {
  const std::string dono = "estacao-orbital-eclusa-norte";
  const std::string_view vista = dono;

  REQUIRE(vista.size() == dono.size());
  REQUIRE(vista.data() == dono.data());   // o MESMO endereço, não uma cópia

  static_assert(sizeof(std::string_view) == 16, "ponteiro + tamanho, e nada mais");
  static_assert(std::is_trivially_copyable_v<std::string_view>);
}

TEST_CASE("caso 2: substr de string COPIA, substr de vista nao") {
  const std::string dono = "###.@.###";

  const std::string pedaco_copiado = dono.substr(3, 3);
  const std::string_view pedaco_visto = std::string_view(dono).substr(3, 3);

  REQUIRE(pedaco_copiado == ".@.");
  REQUIRE(pedaco_visto == ".@.");
  REQUIRE(pedaco_copiado.data() != dono.data() + 3);   // buffer novo
  REQUIRE(pedaco_visto.data() == dono.data() + 3);     // dentro do original

  INFO("é esta diferença que faz `de_texto` receber string_view: as fileiras "
       "do mapa apontam para dentro do texto, sem uma cópia por linha");
}

TEST_CASE("caso 3: a vista NAO termina em nul") {
  const std::string dono = "eclusa-norte";
  const std::string_view prefixo = std::string_view(dono).substr(0, 6);

  REQUIRE(prefixo == "eclusa");
  REQUIRE(prefixo.size() == 6);
  // O byte seguinte ao fim da vista é '-', não '\0'. Passar `prefixo.data()`
  // a uma função que espera `const char*` leria doze caracteres, não seis.
  REQUIRE(prefixo.data()[prefixo.size()] == '-');
  REQUIRE(std::strlen(prefixo.data()) == dono.size());   // e não 6

  INFO("para uma API de C, o caminho é std::string(prefixo), que copia de "
       "propósito - e aí o custo está declarado");
}

// Caso 4: a assimetria da assinatura de `mapa::de_texto(string_view, string)`.
// O texto é lido e descartado dentro da função, então vista basta. O nome é
// GUARDADO no objeto, então tem de ser possuído - e por isso é `std::string`.
TEST_CASE("caso 4: o que a funcao guarda tem de possuir") {
  std::optional<deriva::mapa> m;
  {
    const std::string texto = "#####\n#.@.#\n#####\n";
    m = deriva::mapa::de_texto(texto, "setor-efemero");
    REQUIRE(m.has_value());
  }  // `texto` morreu aqui, e o mapa continua íntegro

  REQUIRE(m->g().largura() == 5);
  REQUIRE(m->nome() == "setor-efemero");
  REQUIRE(m->despejar().find("mapa setor-efemero 5x3") == 0);

  INFO("se `nome_` fosse string_view, esta leitura seria referência pendurada, "
       "e o teste passaria na maioria das execuções - que é o pior resultado");
}

TEST_CASE("o parametro por vista aceita as tres formas sem copiar") {
  const std::string dedo = "#####\n#.@.#\n#####\n";
  const char* cru = "#####\n#.@.#\n#####\n";

  REQUIRE(deriva::mapa::de_texto(dedo, "a").has_value());
  REQUIRE(deriva::mapa::de_texto(cru, "b").has_value());
  REQUIRE(deriva::mapa::de_texto("#####\n#.@.#\n#####\n", "c").has_value());
}
