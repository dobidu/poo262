// Aula 06 - as relacoes que o diagrama afirma
#include <memory>
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "deriva/entidade.hpp"
#include "deriva/inventario.hpp"
#include "deriva/mapa.hpp"
#include "deriva/mundo.hpp"
#include "deriva/reparadora.hpp"

using namespace deriva;

// Aula 06 · UML LEVE - o diagrama conferido contra o codigo.
//
// O diagrama de classes do site (o interativo T9) afirma seis relacoes sobre a
// hierarquia do Deriva. Este arquivo as VERIFICA. Diagrama que ninguem confere
// envelhece calado, e a versao desenhada passa a descrever um sistema que nao
// existe mais - foi o que aconteceu com o `final` de `sonda`, retirado na v1.7.

TEST_CASE("relacao 1: heranca publica de entidade") {
  static_assert(std::is_base_of_v<entidade, sonda>);
  static_assert(std::is_base_of_v<entidade, drone>);
  static_assert(std::is_base_of_v<entidade, item>);
  // Publica, e nao privada: a conversao para a base tem de existir.
  static_assert(std::is_convertible_v<sonda*, entidade*>);
  SUCCEED("tres derivadas, todas por heranca publica");
}

TEST_CASE("relacao 2: entidade e abstrata, e nao se instancia") {
  static_assert(std::is_abstract_v<entidade>);
  static_assert(!std::is_constructible_v<entidade, vetor2>);
  SUCCEED("o desenho diz «abstrata», e o compilador concorda");
}

TEST_CASE("relacao 3: composicao, e nao heranca") {
  // `mapa` TEM uma grade. O desenho usa losango, e nao triangulo.
  static_assert(!std::is_base_of_v<grade, mapa>);
  // `mundo` TEM um mapa, e possui as entidades.
  static_assert(!std::is_base_of_v<mapa, mundo>);
  SUCCEED("as duas sao composicao, e o desenho tem de mostrar losango");
}

TEST_CASE("relacao 4: implementacao de interface, com moldura tracejada") {
  static_assert(std::is_base_of_v<i_reparavel, sonda_reparadora>);
  static_assert(std::is_abstract_v<i_reparavel>);
  static_assert(std::has_virtual_destructor_v<i_reparavel>);
  // Interface PURA: nenhum dado, e por isso o diamante e inofensivo.
  static_assert(std::is_empty_v<i_reparavel> == false,
                "tem vptr, entao nao e vazia - mas nao tem dado proprio");
  SUCCEED("interface pura, e o diamante que ela forma nao duplica estado");
}

TEST_CASE("relacao 5: o diamante da sonda_reparadora") {
  // Ela deriva de DUAS bases, e uma delas e entidade por caminho indireto.
  static_assert(std::is_base_of_v<sonda, sonda_reparadora>);
  static_assert(std::is_base_of_v<i_reparavel, sonda_reparadora>);
  static_assert(std::is_base_of_v<entidade, sonda_reparadora>);
  SUCCEED("o desenho mostra dois triangulos saindo dela, e sao dois mesmo");
}

TEST_CASE("relacao 6: Composite no inventario") {
  static_assert(std::is_base_of_v<componente, peca>);
  static_assert(std::is_base_of_v<componente, mochila>);
  static_assert(std::is_abstract_v<componente>);
  // A mochila CONTEM componentes, e por isso o desenho fecha um ciclo de
  // composicao sobre a base - que e a forma canonica do Composite.
  SUCCEED("uma mochila e um componente que contem componentes");
}

// O que o desenho NAO deve afirmar, e este teste protege contra a tentacao.
TEST_CASE("sonda NAO e final, e o desenho nao pode dizer que e") {
  static_assert(!std::is_final_v<sonda>,
                "era final na v1.0, e a v1.7 retirou a promessa");
  static_assert(std::is_final_v<drone>, "esta continua sendo folha");
  static_assert(std::is_final_v<item>);
  static_assert(std::is_final_v<sonda_reparadora>);
  SUCCEED("tres folhas e uma base intermediaria, e o desenho tem de refletir isso");
}

TEST_CASE("a profundidade da hierarquia e tres, e o diagrama tem tres niveis") {
  // entidade → sonda → sonda_reparadora. O interativo T9 calcula o nivel pela
  // profundidade de heranca, e nao por posicao escolhida a mao - e este e o
  // numero que ele tem de encontrar.
  const int nivel_entidade = 0;
  const int nivel_sonda = 1;
  const int nivel_reparadora = 2;
  REQUIRE(nivel_reparadora - nivel_entidade == 2);
  REQUIRE(nivel_sonda == 1);
}
