// Aula 14 - o que sobra na origem depois de std::move
#include <string>
#include <utility>

#include <catch2/catch_test_macros.hpp>

// O estado da origem depois de um `std::move`, MEDIDO neste alvo.
//
// O material antigo ensinava que a origem fica vazia. O documento de design
// que veio depois ensinava o contrário para string curta: que a otimização de
// string curta faria a libstdc++ copiar os bytes e deixar a origem intacta.
// As duas afirmações estão erradas aqui, e por motivos diferentes.
//
// O que este alvo faz: `basic_string(basic_string&&)` copia o buffer local
// quando a string é curta, rouba o ponteiro quando é longa, e nos DOIS casos
// termina chamando `_M_set_length(0)` na origem. Ela esvazia sempre.
//
// A lição não fica mais fraca, fica mais difícil: é justamente porque
// `REQUIRE(origem.empty())` PASSA aqui que o folclore sobrevive e o bug
// embarca. O padrão promete estado válido mas não-especificado, e o código que
// depende do vazio quebra na próxima implementação, não nesta.

namespace {
constexpr const char* kCurta = "sonda-01";                      // 8 ch, cabe no SSO
constexpr const char* kLonga = "sonda-de-inspecao-orbital-01";  // 28 ch, vai ao heap
}  // namespace

TEST_CASE("nesta implementacao a origem esvazia nos quatro casos") {
  SECTION("curta, por construcao") {
    std::string a(kCurta);
    const std::string b(std::move(a));
    REQUIRE(b == kCurta);
    REQUIRE(a.empty());
  }
  SECTION("longa, por construcao") {
    std::string a(kLonga);
    const std::string b(std::move(a));
    REQUIRE(b == kLonga);
    REQUIRE(a.empty());
  }
  SECTION("curta, por atribuicao") {
    std::string a(kCurta), b;
    b = std::move(a);
    REQUIRE(b == kCurta);
    REQUIRE(a.empty());
  }
  SECTION("longa, por atribuicao") {
    std::string a(kLonga), b;
    b = std::move(a);
    REQUIRE(b == kLonga);
    REQUIRE(a.empty());
  }
}

// A diferença que REALMENTE se observa entre curta e longa não é o estado da
// origem: é se algum byte foi copiado. É este o fato que o interativo da Aula
// 14 mostra, porque é o único que se reproduz.
TEST_CASE("move de string curta COPIA bytes; de string longa transfere ponteiro") {
  SECTION("curta: o buffer é interno, então não há ponteiro a roubar") {
    std::string a(kCurta);
    const void* antes = a.data();
    const std::string b(std::move(a));
    REQUIRE(a.data() == antes);          // a origem segue apontando para si mesma
    REQUIRE(b.data() != antes);          // e o destino teve de copiar 8 bytes
    REQUIRE(b.size() == 8);
  }
  SECTION("longa: o mesmo ponteiro de heap troca de dono") {
    std::string a(kLonga);
    const void* antes = a.data();
    const std::string b(std::move(a));
    REQUIRE(b.data() == antes);          // NENHUM byte de conteúdo foi copiado
    REQUIRE(a.data() != antes);          // a origem voltou ao buffer interno
    REQUIRE(b.size() == 28);
  }
}

TEST_CASE("o limite da otimizacao de string curta neste alvo") {
  REQUIRE(sizeof(std::string) == 32);
  std::string s;
  REQUIRE(s.capacity() == 15);           // 15 caracteres mais o terminador
  s.assign(15, 'x');
  const void* interno = s.data();
  s.push_back('x');                      // o décimo sexto força o heap
  REQUIRE(s.data() != interno);
}

// O que é seguro fazer com a origem, independentemente da implementação.
TEST_CASE("o contrato que vale em qualquer implementacao") {
  std::string a(kCurta);
  const std::string b(std::move(a));
  REQUIRE(b == kCurta);

  a = "sonda-02";                        // atribuir: sempre válido
  REQUIRE(a == "sonda-02");
  a.clear();                             // chamar método sem precondição: válido
  REQUIRE(a.empty());
  // LER o valor e depender dele: é o que o padrão não promete, e o que este
  // teste deliberadamente NÃO faz.
}
