// Aula 22 - quantos incrementos a corrida perde
#include <cstdio>

#include <catch2/catch_test_macros.hpp>

#include "deriva/medida_corrida.hpp"

using namespace deriva::medida;

// O número que o Cap. 22 e o interativo de corrida de dados exibem. Não é um
// valor: é uma faixa, e a variação é o conteúdo.
//
// Este caso NÃO afirma que a corrida se manifesta, e a razão é a lição do
// capítulo. Corrida de dados é comportamento indefinido: nesta máquina, com
// g++ 13.3, oito de dez execuções não perdem um incremento. Um `REQUIRE` de
// que ela apareça reprova o portão em toda execução de sorte - e já reprovou.
//
// O que se afirma é o que o padrão garante: o lado protegido nunca perde, e
// o lado desprotegido não pode perder mais do que somou. O resto é medido e
// impresso, para quem for atualizar o material ler o seu próprio número.
TEST_CASE("a corrida e medida, e nada se afirma sobre ela aparecer") {
  const corrida r = medir(10, 100000);

  std::printf("\n[medida] corrida: esperado %d · perdidos entre %d e %d "
              "em %d execucoes · execucoes sem perda: %d\n",
              r.esperado, r.perdidos_min, r.perdidos_max, r.execucoes,
              r.execucoes_sem_perda);

  // não se perde mais do que se somou, e não se ganha do nada
  REQUIRE(r.perdidos_min >= 0);
  REQUIRE(r.perdidos_max <= r.esperado);
  REQUIRE(r.perdidos_min <= r.perdidos_max);
  REQUIRE(r.execucoes == 10);
  REQUIRE(r.execucoes_sem_perda <= r.execucoes);
}

TEST_CASE("com scoped_lock nao se perde nada, em nenhuma execucao") {
  for (int k = 0; k < 10; ++k) {
    REQUIRE(contar_com_mutex(50000) == 100000);
  }
}
