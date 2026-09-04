// v0.2 - contador, instrumento e terminal_bruto
#include <algorithm>
#include <stdexcept>
#include <string>
#include <vector>

#include <catch2/catch_test_macros.hpp>

#include "deriva/contador.hpp"
#include "deriva/instrumento.hpp"
#include "deriva/terminal_bruto.hpp"

using deriva::instrumento;
using deriva::marca_de_vida;

// A instrumentação de ciclo de vida existe para SUBSTITUIR o sanitizer que o
// laboratório não tem. Aqui ela é usada como o estudante vai usá-la: o traço
// impresso tem de bater, linha por linha, com o roteiro esperado.
TEST_CASE("a ordem de destruicao e a inversa da de construcao") {
  instrumento::limpar();
  {
    // `[[maybe_unused]]` diz ao compilador o que `(void)x` dizia por gesto:
    // o objeto existe pelo efeito do construtor e do destrutor, não pelo
    // valor. O atributo é C++17 e é o lugar mais natural dele em todo o
    // Deriva (Aula 03).
    [[maybe_unused]] const marca_de_vida a("a");
    [[maybe_unused]] const marca_de_vida b("b");
    {
      [[maybe_unused]] const marca_de_vida c("c");
    }
  }
  REQUIRE(instrumento::despejo() ==
          "+a\n"
          "+b\n"
          "+c\n"
          "-c\n"   // o escopo interno fecha primeiro
          "-b\n"   // e o externo desmonta na ordem inversa
          "-a\n");
}

TEST_CASE("a excecao nao pula destrutor - ela o chama ao desenrolar a pilha") {
  instrumento::limpar();
  try {
    [[maybe_unused]] const marca_de_vida externo("externo");
    {
      [[maybe_unused]] const marca_de_vida interno("interno");
      throw std::runtime_error("falha de leitura do setor");
    }
  } catch (const std::runtime_error&) {
    instrumento::anotar("!", "capturada");
  }
  REQUIRE(instrumento::despejo() ==
          "+externo\n"
          "+interno\n"
          "-interno\n"      // desenrolamento: de dentro para fora
          "-externo\n"
          "!capturada\n");
}

TEST_CASE("a copia aparece no traco - inclusive a que ninguem pediu") {
  instrumento::limpar();
  {
    const marca_de_vida original("obj");
    [[maybe_unused]] const marca_de_vida copia = original;   // é o ponto do teste
  }
  REQUIRE(instrumento::despejo() ==
          "+obj\n"
          "+obj'\n"
          "-obj'\n"
          "-obj\n");
}

// terminal_bruto: em teste a saída não é tty, então nada é alterado no
// terminal de quem roda o ctest - mas o ciclo de vida continua contado.
TEST_CASE("terminal_bruto conta como vivo e restaura ao morrer") {
  deriva::zerar_contadores();
  {
    const deriva::terminal_bruto t;
    REQUIRE(deriva::contador_terminal::vivos == 1);
    REQUIRE_FALSE(t.ativo());   // ctest não roda num tty
  }
  REQUIRE(deriva::contador_terminal::vivos == 0);
}

TEST_CASE("terminal_bruto nao e copiavel - ha um terminal so") {
  static_assert(!std::is_copy_constructible_v<deriva::terminal_bruto>);
  static_assert(!std::is_copy_assignable_v<deriva::terminal_bruto>);
  SUCCEED("verificado em tempo de compilacao");
}

// Aula 10 · o traco da ordem base-derivada.
//
// O par instrumentado e LOCAL a este arquivo, e nao `entidade`/`drone` de
// verdade: poluir o despejo que o replay compara custaria o portao 3/4. O que
// se mede aqui e a ORDEM, e ela e a mesma em qualquer hierarquia.
namespace {
std::vector<std::string> ordem;

struct base_marcada {
  base_marcada() { ordem.push_back("+base"); }
  virtual ~base_marcada() { ordem.push_back("-base"); }
};

struct membro_marcado {
  membro_marcado() { ordem.push_back("+membro"); }
  ~membro_marcado() { ordem.push_back("-membro"); }
};

struct derivada_marcada final : base_marcada {
  derivada_marcada() { ordem.push_back("+derivada"); }
  ~derivada_marcada() override { ordem.push_back("-derivada"); }
  membro_marcado m_;   // declarado DEPOIS da base, construido depois dela
};
}  // namespace

TEST_CASE("a ordem e base, membros, corpo da derivada - e o inverso ao morrer") {
  ordem.clear();
  { const derivada_marcada d; }

  REQUIRE(ordem.size() == 6);
  REQUIRE(ordem[0] == "+base");        // a base primeiro, sempre
  REQUIRE(ordem[1] == "+membro");      // depois os membros, na ordem de declaracao
  REQUIRE(ordem[2] == "+derivada");    // e so entao o corpo do construtor
  REQUIRE(ordem[3] == "-derivada");    // e a destruicao inverte os tres
  REQUIRE(ordem[4] == "-membro");
  REQUIRE(ordem[5] == "-base");
}

TEST_CASE("o corpo da derivada roda por ultimo, e isso tem consequencia") {
  // A base nao pode contar com nada que o corpo da derivada faca: quando o
  // construtor da base roda, a derivada ainda nao existe. E por isso que
  // chamar metodo virtual dentro do construtor da base chama a versao DA
  // BASE, e nao a sobrescrita - o objeto ainda nao e do tipo derivado.
  ordem.clear();
  { const derivada_marcada d; }
  const auto pos_base = std::find(ordem.begin(), ordem.end(), "+base");
  const auto pos_corpo = std::find(ordem.begin(), ordem.end(), "+derivada");
  REQUIRE(pos_base < pos_corpo);
}
