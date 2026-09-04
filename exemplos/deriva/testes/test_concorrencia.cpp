// v2.4 - fila entre threads e a ordem preservada
#include <optional>
#include <string>
#include <thread>

#include <catch2/catch_test_macros.hpp>

#include "deriva/fila_de_comandos.hpp"
#include "deriva/medida_corrida.hpp"

using namespace deriva;

TEST_CASE("a fila preserva a ordem, e por isso o replay continua servindo") {
  // Duas threads, e a saida e deterministica: FIFO com UM consumidor. E o
  // ponto da Aula 22 - concorrencia nao implica indeterminismo.
  const std::string a = exercitar_fila(50);
  const std::string b = exercitar_fila(50);
  REQUIRE(a == b);
  REQUIRE(a.find("cmd0 cmd1 cmd2") == 0);
}

TEST_CASE("fechar acorda quem espera, e a espera termina") {
  fila_de_comandos fila;
  std::optional<std::string> resultado;

  std::thread esperando([&fila, &resultado] { resultado = fila.puxar(); });
  fila.fechar();
  esperando.join();

  REQUIRE_FALSE(resultado.has_value());   // fechada e vazia: fim, nao excecao
  REQUIRE(fila.fechada());
}

TEST_CASE("empurrar em fila fechada nao faz nada, e nao lanca") {
  fila_de_comandos fila;
  fila.fechar();
  fila.empurrar("tarde");
  REQUIRE(fila.tamanho() == 0);
}

TEST_CASE("tentar_puxar nao bloqueia, e serve ao laco de render") {
  fila_de_comandos fila;
  REQUIRE_FALSE(fila.tentar_puxar().has_value());
  fila.empurrar("norte");
  const auto c = fila.tentar_puxar();
  REQUIRE(c.has_value());
  REQUIRE(*c == "norte");
  REQUIRE_FALSE(fila.tentar_puxar().has_value());
}

// ATENCAO ao que este teste NAO afirma, e por que.
//
// A primeira versao dele exigia `r.perdidos_max > 0`: que a corrida se
// manifestasse. Ela falhou no portao, e com razao - a medida anterior mostrou
// oito execucoes de dez sem perda alguma. Um teste que depende de
// comportamento indefinido se manifestar e um teste INSTAVEL, e teste instavel
// e pior que teste ausente: ele treina a equipe a reexecutar o portao ate
// passar.
//
// A licao e essa mesma. Sobre a versao sem mutex nao ha o que afirmar, e por
// isso o teste apenas MEDE e relata. O que se afirma e o outro lado: com
// `scoped_lock` a conta fecha em toda execucao, sempre, e e disso que um teste
// pode falar.
TEST_CASE("com scoped_lock a conta fecha sempre; sem ele, nao ha o que afirmar") {
  SECTION("a versao protegida e exata em toda execucao") {
    for (int k = 0; k < 8; ++k) {
      REQUIRE(medida::contar_com_mutex(25000) == 50000);
    }
  }
  SECTION("a versao sem protecao e medida, e nao afirmada") {
    const medida::corrida r = medida::medir(6, 50000);
    REQUIRE(r.esperado == 100000);
    REQUIRE(r.execucoes == 6);
    // Nenhum REQUIRE sobre `perdidos_max`: ele pode ser zero, e isso nao
    // significa que o codigo esteja correto - significa que o defeito nao
    // apareceu HOJE.
    REQUIRE(r.perdidos_max <= r.esperado / 2);
    INFO("perdidos entre " << r.perdidos_min << " e " << r.perdidos_max
         << "; execucoes sem perda: " << r.execucoes_sem_perda << " de " << r.execucoes);
  }
}
