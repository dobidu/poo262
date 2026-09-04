// Aula 01 - o par C contra C++: maneiras de errar
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "../comparativo/grade_procedural.hpp"
#include "deriva/grade.hpp"
#include "deriva/mapa.hpp"

using namespace deriva;
using namespace deriva::comparativo;

// A metrica da Aula 01 nao e elegancia: e quantas maneiras de errar o desenho
// permite. Sete contra uma, e as seis que somem nao somem por disciplina do
// programador - somem porque o compilador passou a impedi-las.
TEST_CASE("a versao OO fecha seis das sete maneiras de errar") {
  REQUIRE(maneiras_de_errar_em_c() == 7);
  REQUIRE(maneiras_de_errar_em_cpp() == 1);
}

TEST_CASE("em C, a copia da struct compartilha o buffer, e ninguem avisa") {
  grade_c a = criar(4, 3);
  escrever(&a, 0, 0, '@');

  grade_c b = a;                     // copia a struct: leva o PONTEIRO
  escrever(&b, 0, 0, '#');

  REQUIRE(em(&a, 0, 0) == '#');      // a "original" mudou
  REQUIRE(a.celulas == b.celulas);   // porque e o mesmo buffer

  destruir(&a);
  // destruir(&b) aqui seria a segunda liberacao. Nao a chamamos - e o fato de
  // termos de LEMBRAR disso e o defeito.
}

TEST_CASE("em C++, a mesma copia e profunda, e sem escrever uma linha") {
  grade a(4, 3);
  a.em({0, 0}).glifo = '@';

  grade b = a;                        // regra do zero: o vector copia
  b.em({0, 0}).glifo = '#';

  REQUIRE(a.em({0, 0}).glifo == '@');  // intacta
  REQUIRE(b.em({0, 0}).glifo == '#');
}

TEST_CASE("em C, largura e publica, e mexer nela corrompe a indexacao") {
  grade_c g = criar(4, 3);
  escrever(&g, 3, 2, 'X');
  g.largura = 2;                      // ninguem impede
  REQUIRE(em(&g, 3, 2) != 'X');       // e a mesma celula passou a ser outra
  destruir(&g);
}

TEST_CASE("em C++, a dimensao e invariante, e o tipo diz isso") {
  const grade g(4, 3);
  REQUIRE(g.largura() == 4);
  // `g.largura() = 2;` nao compila: o retorno e por valor, e nao ha setter.
  static_assert(!std::is_assignable_v<decltype(g.largura()), int>);
  SUCCEED("a invariante e garantida em compilacao, nao por lembranca");
}

TEST_CASE("em C, esquecer destruir nao produz sintoma nenhum hoje") {
  {
    grade_c g = criar(100, 100);
    escrever(&g, 0, 0, '@');
    // sem `destruir(&g)`: 10 KB vazam, e o programa termina bem
  }
  SUCCEED("e e por isso que este teste passa - o vazamento nao tem sintoma");
}

TEST_CASE("em C++, o escopo destroi, e o contador prova") {
  deriva::zerar_contadores();
  {
    const auto m = mapa::de_texto("###\n#@#\n###\n", "t");
    REQUIRE(deriva::contador_mapa::vivos == 1);
  }
  REQUIRE(deriva::contador_mapa::vivos == 0);
}
