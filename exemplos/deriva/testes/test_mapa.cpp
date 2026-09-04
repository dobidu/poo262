// v0.3 - mapa: carregamento, despejo e construcoes
#include <string>
#include <string_view>
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "deriva/contador.hpp"
#include "deriva/instrumento.hpp"
#include "deriva/mapa.hpp"

using deriva::mapa;
using deriva::vetor2;

namespace {
constexpr std::string_view kSetor =
    "#####\n"
    "#.@.#\n"
    "#.!.#\n"
    "#####\n";
}  // namespace

TEST_CASE("carregar de texto le a grade e a entrada") {
  deriva::zerar_contadores();
  const auto m = mapa::de_texto(kSetor, "teste");
  REQUIRE(m.has_value());
  REQUIRE(m->g().largura() == 5);
  REQUIRE(m->g().altura() == 4);
  REQUIRE(m->entrada() == vetor2{2, 1});
  REQUIRE(m->nome() == "teste");

  SECTION("a entrada vira piso - o @ e a sonda, nao o chao") {
    REQUIRE(m->g().em({2, 1}).glifo == '.');
  }
  SECTION("parede tem massa que a sonda nao move") {
    REQUIRE(m->g().em({0, 0}).massa == 1000);
  }
  SECTION("item tem massa transportavel") {
    REQUIRE(m->g().em({2, 2}).glifo == '!');
    REQUIRE(m->g().em({2, 2}).massa == 3);
  }
}

TEST_CASE("ausencia de resultado nao e excecao") {
  REQUIRE_FALSE(mapa::de_texto("", "vazio").has_value());
  REQUIRE_FALSE(mapa::de_texto("###\n##\n", "torto").has_value());
  REQUIRE_FALSE(mapa::carregar("nao/existe/em/lugar/algum.txt").has_value());
}

TEST_CASE("o despejo e deterministico") {
  const auto a = mapa::de_texto(kSetor, "teste");
  const auto b = mapa::de_texto(kSetor, "teste");
  REQUIRE(a->despejar() == b->despejar());
  REQUIRE(a->despejar().find("mapa teste 5x4") == 0);
  REQUIRE(a->despejar().find("entrada 2,1") != std::string::npos);
}

// O contador de instâncias vivas: é ele, e não um sanitizer, que a disciplina
// usa como portão. Este teste é o gabarito de como ele se usa.
TEST_CASE("o contador de instancias vivas fecha em zero") {
  deriva::zerar_contadores();
  REQUIRE(deriva::contador_mapa::vivos == 0);
  {
    const auto m = mapa::de_texto(kSetor, "teste");
    REQUIRE(deriva::contador_mapa::vivos == 1);
    {
      const mapa copia = *m;   // cópia: nasce um objeto, e o contador sabe
      REQUIRE(deriva::contador_mapa::vivos == 2);
      REQUIRE(copia.despejar() == m->despejar());
    }
    REQUIRE(deriva::contador_mapa::vivos == 1);
  }
  REQUIRE(deriva::contador_mapa::vivos == 0);

  // Três criados: o mapa local de `de_texto` (1), o que vai para dentro do
  // `std::optional` (2), e a cópia explícita deste teste (3).
  //
  // Esta linha é o argumento da regra dos cinco (Aula 14), e o argumento não
  // é o que parecia: quando o construtor de movimento entrou na v1.4, este
  // número NÃO caiu. Medido nos dois estados do código, `de_texto` custa duas
  // construções com movimento e duas sem - o contador conta objetos, e dois
  // objetos nascem nos dois casos. A terceira aqui é a cópia explícita deste
  // teste.
  REQUIRE(deriva::contador_mapa::criados == 3);
}

TEST_CASE("mapa TEM as cinco operacoes, e o contador nao viu diferenca") {
  // Este caso substituiu um que afirmava o contrario, e o titulo antigo era
  // falso desde a v1.4. Ele ficava verde porque o `static_assert` era sobre
  // `is_trivially_move_constructible`, que continua falso mesmo com o
  // construtor de movimento presente - um assert que nao verificava o que o
  // titulo prometia.
  static_assert(std::is_copy_constructible_v<deriva::mapa>);
  static_assert(std::is_move_constructible_v<deriva::mapa>);
  static_assert(std::is_move_assignable_v<deriva::mapa>);
  static_assert(std::is_destructible_v<deriva::mapa>);
  static_assert(std::is_nothrow_move_constructible_v<deriva::mapa>,
                "noexcept: e o que faz std::vector<mapa> mover ao realocar");

  // MEDIDO nos dois estados do codigo: `de_texto` custa DUAS construcoes com
  // o movimento declarado, e duas sem ele. O contador conta objetos, e dois
  // objetos nascem nos dois casos.
  deriva::zerar_contadores();
  {
    const auto m = mapa::de_texto(kSetor, "medida");
    REQUIRE(m.has_value());
    REQUIRE(deriva::contador_mapa::criados == 2);
  }
  REQUIRE(deriva::contador_mapa::vivos == 0);
}

TEST_CASE("atribuicao nao cria nem destroi objeto") {
  deriva::zerar_contadores();
  auto a = mapa::de_texto(kSetor, "a");
  auto b = mapa::de_texto("###\n#.#\n###\n", "b");
  REQUIRE(deriva::contador_mapa::vivos == 2);
  *b = *a;
  REQUIRE(deriva::contador_mapa::vivos == 2);   // continua sendo dois
  REQUIRE(b->despejar() == a->despejar());
}

// v1.4 · Aula 14 - o que o movimento muda, e o que ele NÃO muda.
//
// Surpresa medida: o contador de `criados` continua em 3 para um `carregar`,
// exatamente como antes do construtor de movimento existir. O contador conta
// OBJETOS, e três objetos nascem nos dois casos. O que mudou é o custo de
// cada nascimento, e isso o contador não vê.
TEST_CASE("mover um mapa transfere o buffer da grade em vez de copia-lo") {
  auto a = mapa::de_texto(kSetor, "origem");
  REQUIRE(a.has_value());
  const void* buffer_antes = &a->g().em({0, 0});

  const mapa movido(std::move(*a));
  REQUIRE(&movido.g().em({0, 0}) == buffer_antes);   // o MESMO bloco de heap

  const mapa copiado(movido);
  REQUIRE(&copiado.g().em({0, 0}) != buffer_antes);  // buffer novo, 60 células
}

TEST_CASE("o contador nao distingue copia de movimento, e isso e o limite dele") {
  deriva::zerar_contadores();
  {
    auto a = mapa::de_texto(kSetor, "a");
    const int depois_de_carregar = deriva::contador_mapa::criados;

    const mapa movido(std::move(*a));
    const mapa copiado(movido);

    // Dois nascimentos a mais, e o contador soma os dois igual - mesmo que um
    // deles não tenha alocado um byte.
    REQUIRE(deriva::contador_mapa::criados == depois_de_carregar + 2);
  }
  REQUIRE(deriva::contador_mapa::vivos == 0);
}
