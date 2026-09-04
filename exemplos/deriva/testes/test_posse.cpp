// Aula 13 - o que um ciclo de shared_ptr realmente vaza
#include <cstdio>
#include <memory>

#include <catch2/catch_test_macros.hpp>

#include "deriva/medida_posse.hpp"

using deriva::medida::no;
using Aloc = deriva::medida::contando<no>;

// O número que o interativo "grafo de posse" (Aulas 12 e 13) exibe na linha de
// vazamento sai daqui. Antes ele era uma estimativa herdada do documento de
// design, e nada no código a sustentava.
TEST_CASE("um ciclo de shared_ptr prende bytes que ninguem mais alcanca") {
  const std::size_t com_ciclo = deriva::medida::bytes_presos<Aloc>(false);
  const std::size_t com_weak = deriva::medida::bytes_presos<Aloc>(true);

  INFO("sizeof(no) = " << sizeof(no));
  INFO("bytes presos pelo ciclo = " << com_ciclo);

  SECTION("o ciclo vaza, e vaza os dois nos inteiros") {
    REQUIRE(com_ciclo > 0);
    REQUIRE(com_ciclo >= 2 * sizeof(no));
  }
  SECTION("trocar uma ponta por weak_ptr leva a contagem a zero em cascata") {
    REQUIRE(com_weak == 0);
  }
  SECTION("as duas alocacoes acontecem, e so as do ciclo nao voltam") {
    REQUIRE(deriva::medida::contagem::pedidos == 2);
  }
}

// Este caso existe para IMPRIMIR o número, de modo que quem atualizar o
// material tenha de onde copiá-lo. Ele nunca falha.
TEST_CASE("o numero do material, para copiar") {
  const std::size_t presos = deriva::medida::bytes_presos<Aloc>(false);
  std::printf("\n[medida] sizeof(no)=%zu  ciclo prende %zu bytes\n",
              sizeof(no), presos);
  SUCCEED("medido");
}

// Aula 12 · os tamanhos que o capitulo afirma, medidos.
TEST_CASE("unique_ptr com deletor padrao e do tamanho de um ponteiro") {
  REQUIRE(sizeof(std::unique_ptr<int>) == sizeof(int*));
  REQUIRE(sizeof(std::unique_ptr<int, deriva::medida::deletor_sem_estado>) ==
          sizeof(int*));
}

TEST_CASE("deletor com estado cobra o estado dele") {
  REQUIRE(sizeof(std::unique_ptr<int, deriva::medida::deletor_com_estado>) >
          sizeof(std::unique_ptr<int>));
  REQUIRE(sizeof(std::unique_ptr<int, deriva::medida::deletor_com_estado>) ==
          sizeof(int*) + sizeof(const char*));
}

TEST_CASE("shared_ptr e o dobro, e weak_ptr tambem") {
  REQUIRE(sizeof(std::shared_ptr<int>) == 2 * sizeof(int*));
  REQUIRE(sizeof(std::weak_ptr<int>) == 2 * sizeof(int*));
  REQUIRE(sizeof(std::unique_ptr<int>) < sizeof(std::shared_ptr<int>));
}
