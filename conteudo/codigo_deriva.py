# -*- coding: utf-8 -*-
"""GERADO por build/extrair_codigo.py - não edite.

Trechos extraídos de `exemplos/deriva/`, que compila com
`-std=c++17 -Wall -Wextra -Wpedantic` e passa `make verifica`.
Para mudar um trecho, mude o CÓDIGO - não este arquivo.

aula 00: 2 · aula 01: 5 · aula 02: 7 · aula 03: 5 · aula 04: 3 · aula 05: 3 · aula 06: 5 · aula 07: 10 · aula 08: 6 · aula 09: 5 · aula 10: 5 · aula 11: 6 · aula 12: 3 · aula 13: 5 · aula 14: 10 · aula 15: 5 · aula 16: 7 · aula 17: 7 · aula 18: 4 · aula 19: 6 · aula 20: 6 · aula 21: 6 · aula 22: 9 · aula 23: 3 · aula 24: 7 · aula 25: 10 · aula 26: 6
"""

CODIGO = {
    'grade-em-c': {
        'aula': 1,
        'lang': 'cpp',
        'legenda': 'comparativo/grade_procedural.hpp · a grade em estilo C',
        'nota': 'Cinco regras que só existem na cabeça de quem chama, e nenhuma delas está escrita no código. A métrica da Aula 01 não é elegância: é quantas maneiras de errar o desenho permite - sete aqui, uma na versão OO.',
        'arquivo': 'exemplos/deriva/comparativo/grade_procedural.hpp',
        'linha': 10,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A grade da estação em estilo C: dado exposto, funções livres, e o
/// contrato inteiro na cabeça de quem chama.
///
/// Isto não é caricatura. É a forma que o C permite e que o C++ herdou, e
/// funciona - com uma condição: que todo mundo lembre das regras. As regras
/// são cinco, e nenhuma delas está escrita no código.
///
///   1. chame `criar` antes de qualquer outra coisa;
///   2. chame `destruir` exatamente uma vez, e nunca depois de copiar;
///   3. não copie a struct - ela leva o ponteiro, e não os dados;
///   4. não escreva em `largura` nem `altura` depois de criada;
///   5. confira o limite antes de indexar, porque ninguém confere por você.
struct grade_c {
  int largura;
  int altura;
  char* celulas;
};""",
    },
    'copia-que-nao-copia': {
        'aula': 1,
        'lang': 'cpp',
        'legenda': 'testes/test_comparativo.cpp · a cópia que não copia',
        'nota': 'Copiar a struct leva o ponteiro, não os dados, e ninguém avisa. A versão C++ faz a cópia profunda pela regra do zero, sem escrever uma linha - e é essa diferença, e não a sintaxe, que o capítulo defende.',
        'arquivo': 'exemplos/deriva/testes/test_comparativo.cpp',
        'linha': 21,
        'quebrado_de_proposito': True,
        'codigo': """\
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
}""",
    },
    'vazamento-sem-sintoma': {
        'aula': 1,
        'lang': 'cpp',
        'legenda': 'testes/test_comparativo.cpp · o vazamento que passa no teste',
        'nota': 'Dez quilobytes vazam e o teste passa, porque o vazamento não tem sintoma. É o argumento inteiro do contador de instâncias da Aula 07.',
        'arquivo': 'exemplos/deriva/testes/test_comparativo.cpp',
        'linha': 63,
        'quebrado_de_proposito': True,
        'codigo': """\
TEST_CASE("em C, esquecer destruir nao produz sintoma nenhum hoje") {
  {
    grade_c g = criar(100, 100);
    escrever(&g, 0, 0, '@');
    // sem `destruir(&g)`: 10 KB vazam, e o programa termina bem
  }""",
    },
    'codigo-gerado': {
        'aula': 4,
        'lang': 'cpp',
        'legenda': 'revisao_ia/gerado.hpp · o que um modelo produz',
        'nota': 'Compila sem um aviso e passa no teste que o próprio modelo escreveu. Tem três defeitos plantados, um por item da rubrica, e nenhum é erro de digitação: os três são decisões plausíveis, e é isso que os torna caros.',
        'arquivo': 'exemplos/deriva/revisao_ia/gerado.hpp',
        'linha': 29,
        'quebrado_de_proposito': True,
        'codigo': """\
/// A base da hierarquia gerada.
struct sensor_base {
  explicit sensor_base(std::string nome) : nome_(std::move(nome)) {}

  // DEFEITO 2 · item R5 da rubrica (Hierarquia): destrutor NÃO virtual numa base com
  // método virtual. Deletar por `sensor_base*` não roda o destrutor da
  // derivada. Com o `delete` dentro de um `unique_ptr`, o compilador não
  // emite aviso algum.
  ~sensor_base() = default;   // R5

  virtual double media() const = 0;

  // DEFEITO 3 · item R3 da rubrica (const-correctness): devolve cópia da string a cada chamada,
  // e não é `const` nem `[[nodiscard]]`. Chamar num objeto `const` não
  // compila, e o custo passa despercebido em laço.
  std::string nome() { return nome_; }   // R3

 protected:
  std::string nome_;
};""",
    },
    'teste-que-nao-prova': {
        'aula': 4,
        'lang': 'cpp',
        'legenda': 'testes/test_revisao_ia.cpp · o teste que o modelo escreveu',
        'nota': 'Ele passa, e não prova nada do que importa. É o item R7 da rubrica: o teste tem de falhar se o comportamento mudar, e não se a implementação mudar.',
        'arquivo': 'exemplos/deriva/testes/test_revisao_ia.cpp',
        'linha': 12,
        'quebrado_de_proposito': False,
        'codigo': """\
// O teste que o proprio modelo escreveu para o codigo dele. Passa. E nao prova
// nada do que importa - e essa e a licao do item R7 da rubrica.
TEST_CASE("o teste que veio com o codigo gerado passa") {
  sensor_termico t("termico-01");
  t.registrar(20.0);
  t.registrar(22.0);
  REQUIRE(t.media() == 21.0);
  REQUIRE(t.nome() == "termico-01");
}""",
    },
    'defeito-invariante': {
        'aula': 4,
        'lang': 'cpp',
        'legenda': 'testes/test_revisao_ia.cpp · R1, medido nos dois lados',
        'nota': 'Com o vetor público, `registrar` protege uma invariante que qualquer um contorna de fora - e a média passa a mentir. A versão revisada recusa o valor e mantém o vetor privado.',
        'arquivo': 'exemplos/deriva/testes/test_revisao_ia.cpp',
        'linha': 31,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("R1: o vetor publico anula a invariante da classe") {
  sensor_termico t("x");
  t.registrar(20.0);
  t.leituras_.push_back(-999.0);   // ninguem impede, e a media mente
  REQUIRE(t.media() < 0.0);

  SECTION("na versao revisada, registrar RECUSA e o vetor e privado") {
    revisado::sensor_termico r("x");
    REQUIRE(r.registrar(20.0));
    REQUIRE_FALSE(r.registrar(-999.0));
    REQUIRE(r.quantas() == 1);
    REQUIRE(r.media() == 20.0);
  }""",
    },
    'despacho-simples': {
        'aula': 5,
        'lang': 'cpp',
        'legenda': 'tipos/despacho.cpp · C++ tem despacho simples',
        'nota': 'Duas perguntas de tipo, uma por operando, porque `virtual` resolve por um só. Com N tipos esta função cresce com N², e é esse crescimento que faz o Visitor existir. Se houvesse despacho múltiplo, a função não existiria.',
        'arquivo': 'exemplos/deriva/tipos/despacho.cpp',
        'linha': 11,
        'quebrado_de_proposito': False,
        'codigo': """\
std::string resolver(const colisao& a, const colisao& b) {
  // Duas perguntas de tipo, uma para cada operando, porque `virtual` resolve
  // por um só. Com N tipos, esta função cresce com N² - e é exatamente esse
  // crescimento que faz o Visitor existir.
  const bool a_sonda = dynamic_cast<const sonda_c*>(&a) != nullptr;
  const bool b_sonda = dynamic_cast<const sonda_c*>(&b) != nullptr;

  if (a_sonda && b_sonda) return "sonda x sonda: as duas param";
  if (a_sonda && !b_sonda) return "sonda x parede: a sonda para";
  if (!a_sonda && b_sonda) return "parede x sonda: a sonda para";
  return "parede x parede: nada acontece";
}""",
    },
    'explicit-recusa': {
        'aula': 5,
        'lang': 'cpp',
        'legenda': 'tipos/despacho.hpp · forte por padrão, fraco por convite',
        'nota': 'Sem `explicit`, trinta graus Celsius viraria trinta Fahrenheit em silêncio. Com ele, o compilador exige a conversão escrita - e é aí que o sistema de tipos fica forte.',
        'arquivo': 'exemplos/deriva/tipos/despacho.hpp',
        'linha': 33,
        'quebrado_de_proposito': False,
        'codigo': """\
struct fahrenheit {
  // Sem `explicit`, `fahrenheit f = 30.0;` compilaria, e 30 graus Celsius
  // viraria 30 Fahrenheit em silêncio. Com ele, o compilador exige a
  // conversão escrita - e é aí que o sistema de tipos fica forte.
  explicit fahrenheit(double v) : valor(v) {}
  double valor;
};""",
    },
    'trait-a-mao': {
        'aula': 5,
        'lang': 'cpp',
        'legenda': 'tipos/despacho.hpp · trait em C++ é template, não construção',
        'nota': 'Em Rust ou Scala o trait é construção da linguagem; aqui é um template que responde sobre um tipo. O teste o aplica a `sonda` e a `mapa`, e a resposta vem sem executar nada.',
        'arquivo': 'exemplos/deriva/tipos/despacho.hpp',
        'linha': 66,
        'quebrado_de_proposito': False,
        'codigo': """\
struct tem_glifo : std::false_type {};""",
    },
    'uml-conferida': {
        'aula': 6,
        'lang': 'cpp',
        'legenda': 'testes/test_uml.cpp · o diagrama, conferido',
        'nota': '`mapa` TEM uma grade, e o desenho usa losango e não triângulo. Diagrama que ninguém confere envelhece calado, e a versão desenhada passa a descrever um sistema que já não existe.',
        'arquivo': 'exemplos/deriva/testes/test_uml.cpp',
        'linha': 37,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("relacao 3: composicao, e nao heranca") {
  // `mapa` TEM uma grade. O desenho usa losango, e nao triangulo.
  static_assert(!std::is_base_of_v<grade, mapa>);
  // `mundo` TEM um mapa, e possui as entidades.
  static_assert(!std::is_base_of_v<mapa, mundo>);
  SUCCEED("as duas sao composicao, e o desenho tem de mostrar losango");
}""",
    },
    'uml-final-retirado': {
        'aula': 6,
        'lang': 'cpp',
        'legenda': 'testes/test_uml.cpp · o que o desenho não pode afirmar',
        'nota': '`sonda` era `final` na v1.0 e deixou de ser na v1.7. Este teste protege contra a tentação de o diagrama continuar dizendo que é - foi um diagrama envelhecido que motivou escrever este arquivo.',
        'arquivo': 'exemplos/deriva/testes/test_uml.cpp',
        'linha': 72,
        'quebrado_de_proposito': False,
        'codigo': """\
// O que o desenho NAO deve afirmar, e este teste protege contra a tentacao.
TEST_CASE("sonda NAO e final, e o desenho nao pode dizer que e") {
  static_assert(!std::is_final_v<sonda>,
                "era final na v1.0, e a v1.7 retirou a promessa");
  static_assert(std::is_final_v<drone>, "esta continua sendo folha");
  static_assert(std::is_final_v<item>);
  static_assert(std::is_final_v<sonda_reparadora>);
  SUCCEED("tres folhas e uma base intermediaria, e o desenho tem de refletir isso");
}""",
    },
    'cmake-nucleo': {
        'aula': 2,
        'lang': 'cmake',
        'legenda': 'CMakeLists.txt · a biblioteca do núcleo',
        'nota': 'O núcleo não conhece UI nenhuma. É esta separação, e não uma promessa, que faz o argumento do segundo front-end da Aula 26 fechar.',
        'arquivo': 'exemplos/deriva/CMakeLists.txt',
        'linha': 21,
        'quebrado_de_proposito': False,
        'codigo': """\
# ---------------------------------------------------------------------------
# o núcleo: nada de UI aqui dentro. É esta separação que faz o argumento do
# segundo front-end (Aula 26) fechar - e ela existe desde a v0.2.
# ---------------------------------------------------------------------------
add_library(deriva_nucleo
  src/contador.cpp
  src/instrumento.cpp
  src/grade.cpp
  src/mapa.cpp
  src/entidade.cpp
  src/mundo.cpp
  src/estacao.cpp
  src/fov.cpp
  src/reparadora.cpp
  src/inspetor.cpp
  src/erro.cpp
  src/inventario.cpp
  src/partida.cpp
  src/fila_de_comandos.cpp
  src/apresentacao.cpp
  src/padroes.cpp
  src/solid.cpp
  comparativo/grade_procedural.cpp
  tipos/despacho.cpp
  src/terminal_bruto.cpp
)""",
    },
    'cmake-warnings': {
        'aula': 2,
        'lang': 'cmake',
        'legenda': 'CMakeLists.txt · o portão de warning',
        'nota': 'Os avisos incidem no núcleo e só nele. FTXUI e Catch2 entram como SYSTEM logo abaixo - para que o aviso deles não conte, e para que ninguém se esconda atrás deles.',
        'arquivo': 'exemplos/deriva/CMakeLists.txt',
        'linha': 51,
        'quebrado_de_proposito': False,
        'codigo': """\
# O portão de zero warning incide sobre ISTO, e só. Dependência de terceiro
# entra como SYSTEM mais abaixo, justamente para que o aviso dela não conte -
# e para que ninguém se esconda atrás dela.
target_compile_options(deriva_nucleo PRIVATE
  -Wall -Wextra -Wpedantic -Wshadow -Wnon-virtual-dtor -Wold-style-cast
  -Wcast-align -Wunused -Woverloaded-virtual -Wconversion -Wsign-conversion
  -Wdouble-promotion -Wformat=2
)""",
    },
    'cmake-ftxui': {
        'aula': 2,
        'lang': 'cmake',
        'legenda': 'CMakeLists.txt · FTXUI com tag fixa',
        'nota': 'A tag não flutua. A v5.0.0 declara cxx_std_17; as v6/v7 podem elevar o padrão exigido e derrubar o alvo da disciplina.',
        'arquivo': 'exemplos/deriva/CMakeLists.txt',
        'linha': 93,
        'quebrado_de_proposito': False,
        'codigo': """\
FetchContent_Declare(ftxui
  GIT_REPOSITORY https://github.com/ArthurSonzogni/FTXUI.git
  GIT_TAG v5.0.0
  GIT_SHALLOW TRUE
  SYSTEM
)""",
    },
    'gdb-no-destrutor': {
        'aula': 2,
        'lang': 'make',
        'legenda': 'Makefile · gdb com ponto de parada em destrutor',
        'nota': 'A terceira das três técnicas que substituem o sanitizer ausente. É ela que mostra, na Aula 11, o destrutor da derivada nunca sendo alcançado quando se deleta por ponteiro da base.',
        'arquivo': 'exemplos/deriva/Makefile',
        'linha': 71,
        'quebrado_de_proposito': False,
        'codigo': """\
# Aula 08 e 11: provar que o destrutor roda - e onde ele não roda.
gdb-dtor: compila
	@gdb -batch -ex 'break deriva::mapa::~mapa' -ex run -ex 'info locals' -ex bt \\
	     -ex 'continue' --args ./$(BUILD)/deriva --render 2>&1 | head -30""",
    },
    'fora-de-limite': {
        'aula': 2,
        'lang': 'cpp',
        'legenda': 'sanitizers/defeitos_de_memoria.cpp · sem `dentro()` ao lado',
        'nota': 'O `operator[]` do `vector` não confere limite - `at()` conferiria, e é a escolha que a versão boa deixa explícita para quem chama. O ASan aponta a linha da escrita E a linha da alocação, que é a informação que faltava.',
        'arquivo': 'exemplos/deriva/sanitizers/defeitos_de_memoria.cpp',
        'linha': 57,
        'quebrado_de_proposito': True,
        'codigo': """\
// DEFEITO 1 · acesso fora de limite.
//
// Sem `dentro()` ao lado, esta função aceita qualquer posição. O
// `operator[]` do vector não confere - `at()` conferiria, e é a escolha que
// a versão boa deixa explícita.
[[nodiscard]] celula& em(int x, int y) {
  return celulas_[static_cast<std::size_t>(y) * static_cast<std::size_t>(largura_) +
                  static_cast<std::size_t>(x)];
}""",
    },
    'estouro-com-sinal': {
        'aula': 2,
        'lang': 'cpp',
        'legenda': 'sanitizers/defeitos_de_memoria.cpp · o estouro que não avisa',
        'nota': 'Com literais, o g++ dobra a conta, vê o estouro e avisa por `-Woverflow`. Com os valores vindo de fora ele não tem o que dobrar, o aviso desaparece, e o estouro passa a acontecer em execução. O compilador pega o que consegue ver, e é por isso que o defeito real nunca chega com número escrito no código.',
        'arquivo': 'exemplos/deriva/sanitizers/defeitos_de_memoria.cpp',
        'linha': 99,
        'quebrado_de_proposito': True,
        'codigo': """\
// As dimensões vêm de FORA - de linha de comando, como vêm de um arquivo
// de mapa no Deriva de verdade. E é essa a diferença que importa.
//
// Escrito com literais - `const int p = 50000 * 50000;` - o g++ dobra a
// conta em tempo de compilação, vê o estouro e avisa: `-Woverflow`,
// "integer overflow in expression of type 'int' results in
// '-1794967296'". O defeito não embarca.
//
// Com os valores vindo de fora, o compilador não tem o que dobrar, o aviso
// desaparece, e o estouro passa a acontecer em execução. É assim que ele
// chega em produção: não com número escrito no código, mas com número
// lido de um arquivo que alguém editou.
const int largura = std::atoi("50000");
const int altura = std::atoi("50000");
const int produto = largura * altura;       // <-- o estouro, sem aviso
std::printf("   largura x altura ... %d  <-- deveria ser 2500000000\\n", produto);
std::printf("   como size_t ........ %zu\\n", static_cast<std::size_t>(produto));
std::puts("   a conta acontece em int, e nenhum static_cast depois a conserta.");
std::puts("   a versao boa converte CADA fator ANTES de multiplicar.");""",
    },
    'string-view-vida': {
        'aula': 3,
        'lang': 'cpp',
        'legenda': 'src/mapa.cpp · string_view e tempo de vida',
        'nota': '`string_view` não possui os bytes. As fileiras apontam para dentro de `texto`, e nada disso é guardado depois - se fosse, seriam referências penduradas no instante em que a função retornasse.',
        'arquivo': 'exemplos/deriva/src/mapa.cpp',
        'linha': 66,
        'quebrado_de_proposito': False,
        'codigo': """\
std::optional<mapa> mapa::de_texto(std::string_view texto, std::string nome) {
  // `string_view` não possui os bytes: `texto` tem de continuar vivo durante
  // toda esta função. É por isso que as fileiras abaixo são `string_view`
  // para dentro de `texto`, e nada disso é guardado depois (Aula 03).
  std::vector<std::string_view> fileiras;
  std::size_t inicio = 0;
  while (inicio <= texto.size()) {
    const std::size_t fim = texto.find('\\n', inicio);
    std::string_view linha = texto.substr(
        inicio, fim == std::string_view::npos ? std::string_view::npos : fim - inicio);
    if (!linha.empty()) fileiras.push_back(linha);
    if (fim == std::string_view::npos) break;
    inicio = fim + 1;
  }

  if (fileiras.empty()) return std::nullopt;""",
    },
    'ligacao-estruturada': {
        'aula': 3,
        'lang': 'cpp',
        'legenda': 'src/main.cpp · ligação estruturada',
        'nota': '`for (const auto& [nome, delta] : tabela)` - por referência, e `const` porque só se lê. Copiar por valor aqui seria copiar a tabela inteira a cada volta.',
        'arquivo': 'exemplos/deriva/src/main.cpp',
        'linha': 78,
        'quebrado_de_proposito': False,
        'codigo': """\
// ligação estruturada (C++17) sobre a tabela de comandos
static const std::pair<std::string_view, deriva::vetor2> tabela[] = {
    {"norte", {0, -1}}, {"sul", {0, 1}}, {"leste", {1, 0}},
    {"oeste", {-1, 0}}, {"esperar", {0, 0}}};
for (const auto& [nome, delta] : tabela) {
  if (linha == nome) {
    passos.push_back({linha, delta});
    break;
  }""",
    },
    'string-view-sem-nul': {
        'aula': 3,
        'lang': 'cpp',
        'legenda': 'testes/test_string_view.cpp · a vista não termina em nul',
        'nota': 'É o caso que mais morde: `strlen(vista.data())` devolve o tamanho da string de origem, não o da vista. Para uma API de C o caminho é `std::string(vista)`, que copia de propósito - e aí o custo está declarado.',
        'arquivo': 'exemplos/deriva/testes/test_string_view.cpp',
        'linha': 42,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("caso 3: a vista NAO termina em nul") {
  const std::string dono = "eclusa-norte";
  const std::string_view prefixo = std::string_view(dono).substr(0, 6);

  REQUIRE(prefixo == "eclusa");
  REQUIRE(prefixo.size() == 6);
  // O byte seguinte ao fim da vista é '-', não '\\0'. Passar `prefixo.data()`
  // a uma função que espera `const char*` leria doze caracteres, não seis.
  REQUIRE(prefixo.data()[prefixo.size()] == '-');
  REQUIRE(std::strlen(prefixo.data()) == dono.size());   // e não 6

  INFO("para uma API de C, o caminho é std::string(prefixo), que copia de "
       "propósito - e aí o custo está declarado");
}""",
    },
    'maybe-unused': {
        'aula': 3,
        'lang': 'cpp',
        'legenda': 'testes/test_ciclo_de_vida.cpp · [[maybe_unused]]',
        'nota': 'O atributo diz ao compilador o que `(void)x` dizia por gesto: o objeto existe pelo efeito do construtor e do destrutor, não pelo valor.',
        'arquivo': 'exemplos/deriva/testes/test_ciclo_de_vida.cpp',
        'linha': 22,
        'quebrado_de_proposito': False,
        'codigo': """\
// `[[maybe_unused]]` diz ao compilador o que `(void)x` dizia por gesto:
// o objeto existe pelo efeito do construtor e do destrutor, não pelo
// valor. O atributo é C++17 e é o lugar mais natural dele em todo o
// Deriva (Aula 03).
[[maybe_unused]] const marca_de_vida a("a");
[[maybe_unused]] const marca_de_vida b("b");
{
  [[maybe_unused]] const marca_de_vida c("c");
}""",
    },
    'nodiscard-vetor2': {
        'aula': 3,
        'lang': 'cpp',
        'legenda': 'include/deriva/vetor2.hpp · v0.1',
        'nota': '`[[nodiscard]]` numa comparação: chamar `a == b` e jogar o resultado fora é sempre erro, e agora o compilador diz isso.',
        'arquivo': 'exemplos/deriva/include/deriva/vetor2.hpp',
        'linha': 15,
        'quebrado_de_proposito': False,
        'codigo': """\
struct vetor2 {
  int x = 0;
  int y = 0;

  [[nodiscard]] constexpr bool operator==(const vetor2& o) const noexcept {
    return x == o.x && y == o.y;
  }
  [[nodiscard]] constexpr bool operator!=(const vetor2& o) const noexcept {
    return !(*this == o);
  }

  // v1.5 · Aula 15. Os compostos são MEMBROS porque modificam o objeto da
  // esquerda; os binários são funções LIVRES, logo abaixo, porque tratam os
  // dois lados igual. Escrever `+` em termos de `+=` é a forma que não
  // duplica a regra.
  constexpr vetor2& operator+=(const vetor2& o) noexcept {
    x += o.x;
    y += o.y;
    return *this;
  }
  constexpr vetor2& operator-=(const vetor2& o) noexcept {
    x -= o.x;
    y -= o.y;
    return *this;
  }
  constexpr vetor2& operator*=(int k) noexcept {
    x *= k;
    y *= k;
    return *this;
  }

  /// Distância de Manhattan, que é a métrica da grade: a sonda não anda em
  /// diagonal, então a distância euclidiana mentiria sobre o número de turnos.
  [[nodiscard]] constexpr int manhattan(const vetor2& o) const noexcept {
    const int dx = x > o.x ? x - o.x : o.x - x;
    const int dy = y > o.y ? y - o.y : o.y - y;
    return dx + dy;
  }
};""",
    },
    'celula-boa': {
        'aula': 7,
        'lang': 'cpp',
        'legenda': 'include/deriva/celula.hpp · 12 bytes',
        'nota': 'Agrupada por tamanho. Os offsets no comentário não são estimativa: os `static_assert` no fim do arquivo os afirmam, e o build falha se mudarem.',
        'arquivo': 'exemplos/deriva/include/deriva/celula.hpp',
        'linha': 9,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Uma célula da grade da estação.
///
/// A ordem dos membros aqui NÃO é estética: agrupada por tamanho, a célula
/// ocupa 12 bytes. Declarada na ordem "natural" - o glifo primeiro, porque é
/// o que se vê - , ocupa 16. Numa grade de 80×24 são 1920 células, logo 23 KB
/// contra 30 KB, e é o mesmo código.
///
/// `celula_ingenua` existe só para ser medida: é o contraexemplo do
/// interativo "inspetor de objeto" (Aula 07), e os static_assert abaixo são o
/// que impede o material de mentir sobre esses números.
struct celula {
  int energia = 0;   // 4 B  @ 0
  int massa = 0;     // 4 B  @ 4
  char glifo = '.';  // 1 B  @ 8
  char sigla = ' ';  // 1 B  @ 9
                     //       + 2 B de padding no fim
};""",
    },
    'celula-ingenua': {
        'aula': 7,
        'lang': 'cpp',
        'legenda': 'include/deriva/celula.hpp · 16 bytes',
        'nota': 'A MESMA célula, na ordem em que se pensa nela. Quatro bytes a mais por célula, 7,5 KB numa grade de 80×24, e nada em troca.',
        'arquivo': 'exemplos/deriva/include/deriva/celula.hpp',
        'linha': 27,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A MESMA célula, na ordem em que se pensa nela. Não use.
struct celula_ingenua {
  char glifo = '.';  // 1 B  @ 0   + 3 B de padding
  int energia = 0;   // 4 B  @ 4
  char sigla = ' ';  // 1 B  @ 8   + 3 B de padding
  int massa = 0;     // 4 B  @ 12
};""",
    },
    'static-assert-leiaute': {
        'aula': 7,
        'lang': 'cpp',
        'legenda': 'include/deriva/celula.hpp · os números, aferidos',
        'nota': 'É esta linha que impede o material de mentir. Se o leiaute mudar, o Deriva não compila - e o interativo da Aula 07 não passa a exibir número errado em silêncio.',
        'arquivo': 'exemplos/deriva/include/deriva/celula.hpp',
        'linha': 35,
        'quebrado_de_proposito': False,
        'codigo': """\
static_assert(sizeof(celula) == 12, "agrupada por tamanho");
static_assert(sizeof(celula_ingenua) == 16, "a ordem ingênua custa 4 bytes por célula");
static_assert(alignof(celula) == 4, "o maior membro manda no alinhamento");
static_assert(offsetof(celula, glifo) == 8, "os dois int primeiro, sem buraco entre eles");""",
    },
    'contador-vivos': {
        'aula': 7,
        'lang': 'cpp',
        'legenda': 'include/deriva/contador.hpp · o detector de vazamento',
        'nota': '`inline static` é variável inline, C++17: dispensa a definição num .cpp. A repetição em cada classe é deliberada - é ela que motiva o `contador_de_instancias<T>` da Aula 19.',
        'arquivo': 'exemplos/deriva/include/deriva/contador.hpp',
        'linha': 7,
        'quebrado_de_proposito': False,
        'codigo': """\
/// O detector de vazamento da disciplina, e ele não depende de sanitizer.
///
/// `vivos` é `inline static` - variável inline é C++17, e é o que dispensa a
/// definição num .cpp. Incrementa no construtor, decrementa no destrutor: se
/// não fecha em zero no fim de `main`, um destrutor não rodou.
///
/// Nesta versão o contador é escrito À MÃO em cada classe que o quer. Essa
/// repetição é deliberada: é ela que motiva o `contador_de_instancias<T>` por
/// CRTP na Aula 19. Template que chega antes de o estudante sentir a
/// repetição é solução para um problema que ele não teve.
///
/// Não é seguro entre threads. A Aula 22 mostra exatamente esta variável
/// perdendo um incremento - e é o interativo de corrida de dados.
struct contador_mapa {
  inline static int vivos = 0;
  inline static int criados = 0;
};""",
    },
    'lista-de-inicializacao': {
        'aula': 8,
        'lang': 'cpp',
        'legenda': 'src/grade.cpp · validar NA lista de inicialização',
        'nota': 'A primeira versão validava no corpo, e um teste pegou: com `grade(5, -1)` o vector lançava `length_error` antes de o corpo rodar. A lista de inicialização acontece inteira antes da primeira linha do corpo.',
        'arquivo': 'exemplos/deriva/src/grade.cpp',
        'linha': 9,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Valida NA lista de inicialização, não no corpo.
///
/// A primeira versão deste construtor validava no corpo, e um teste pegou o
/// erro: com `grade(5, -1)`, o `-1` virava `size_t` enorme e o `std::vector`
/// lançava `length_error` **antes** de o corpo rodar. A mensagem que o
/// estudante veria era "cannot create std::vector larger than max_size()", que
/// não diz nada sobre a grade.
///
/// A lista de inicialização roda inteira antes da primeira linha do corpo:
/// validação de argumento que protege a construção de um membro tem de estar
/// na lista, e a ordem é a de DECLARAÇÃO dos membros - `largura_` e `altura_`
/// vêm antes de `celulas_`, então a checagem acontece a tempo (Aula 08).
[[nodiscard]] int exigir_positivo(int valor, const char* qual) {
  if (valor <= 0) {
    throw std::invalid_argument(std::string("grade: ") + qual +
                                " precisa ser positiva, recebeu " +
                                std::to_string(valor));
  }""",
    },
    'marca-de-vida': {
        'aula': 8,
        'lang': 'cpp',
        'legenda': 'src/instrumento.cpp · instrumentação de ciclo de vida',
        'nota': 'Construtor e destrutor imprimindo a própria execução. Substitui o sanitizer que o laboratório não tem: o estudante LÊ o traço e o compara com o roteiro.',
        'arquivo': 'exemplos/deriva/src/instrumento.cpp',
        'linha': 40,
        'quebrado_de_proposito': False,
        'codigo': """\
marca_de_vida::marca_de_vida(std::string nome) : nome_(std::move(nome)) {
  instrumento::anotar("+", nome_);
}

marca_de_vida::~marca_de_vida() { instrumento::anotar("-", nome_); }

// A cópia é anotada com sufixo próprio: é assim que o estudante vê, no traço,
// que houve uma cópia que ele não pediu.
marca_de_vida::marca_de_vida(const marca_de_vida& o) : nome_(o.nome_ + "'") {
  instrumento::anotar("+", nome_);
}

marca_de_vida& marca_de_vida::operator=(const marca_de_vida& o) {""",
    },
    'terminal-raii': {
        'aula': 8,
        'lang': 'cpp',
        'legenda': 'src/terminal_bruto.cpp · o construtor adquire',
        'nota': '`isatty` primeiro: em pipe, em teste ou em CI não há modo bruto a alterar. Sem essa guarda, `ctest` deixaria o terminal de quem roda os testes em estado imprevisível.',
        'arquivo': 'exemplos/deriva/src/terminal_bruto.cpp',
        'linha': 14,
        'quebrado_de_proposito': False,
        'codigo': """\
terminal_bruto::terminal_bruto() {
  ++contador_terminal::vivos;
  ++contador_terminal::criados;

  if (::isatty(STDIN_FILENO) == 0) return;  // pipe, teste, CI: não há o que mexer
  if (::tcgetattr(STDIN_FILENO, &salvo()) != 0) return;

  termios bruto = salvo();

  // ICANON e ECHO são macros de `int`. `~(ICANON | ECHO)` é um int NEGATIVO,
  // e atribuí-lo a `c_lflag`, que é `unsigned`, muda o valor de -11 para
  // 4294967285. O resultado funciona por acidente do complemento de dois, e
  // -Wsign-conversion está certo em reclamar. Converter primeiro, complementar
  // depois: aí a operação toda acontece em `tcflag_t`.
  const tcflag_t cru = static_cast<tcflag_t>(ICANON) | static_cast<tcflag_t>(ECHO);
  bruto.c_lflag &= ~cru;
  bruto.c_cc[VMIN] = 1;
  bruto.c_cc[VTIME] = 0;
  if (::tcsetattr(STDIN_FILENO, TCSAFLUSH, &bruto) == 0) ativo_ = true;
}""",
    },
    'terminal-dtor': {
        'aula': 8,
        'lang': 'cpp',
        'legenda': 'src/terminal_bruto.cpp · o destrutor libera',
        'nota': 'Duas linhas. São elas que separam “o terminal volta ao normal” de “o estudante digita `reset` às cegas” - e o recurso aqui sobrevive ao processo, então ninguém vai desfazer isso por ele.',
        'arquivo': 'exemplos/deriva/src/terminal_bruto.cpp',
        'linha': 35,
        'quebrado_de_proposito': False,
        'codigo': """\
// É esta linha que separa "o terminal do estudante volta ao normal" de "ele
// digita `reset` às cegas". A variante quebrada não a tem.
terminal_bruto::~terminal_bruto() {
  if (ativo_) ::tcsetattr(STDIN_FILENO, TCSAFLUSH, &salvo());
  --contador_terminal::vivos;
}""",
    },
    'traco-excecao': {
        'aula': 8,
        'lang': 'cpp',
        'legenda': 'testes/test_ciclo_de_vida.cpp · o desenrolar da pilha',
        'nota': 'O teste afirma a ordem exata, linha por linha. A exceção não pula os destrutores: ela os chama, de dentro para fora. É essa garantia, e nada mais, que faz RAII funcionar.',
        'arquivo': 'exemplos/deriva/testes/test_ciclo_de_vida.cpp',
        'linha': 41,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("a excecao nao pula destrutor - ela o chama ao desenrolar a pilha") {
  instrumento::limpar();
  try {
    [[maybe_unused]] const marca_de_vida externo("externo");
    {
      [[maybe_unused]] const marca_de_vida interno("interno");
      throw std::runtime_error("falha de leitura do setor");
    }""",
    },
    'grade-regra-do-zero': {
        'aula': 9,
        'lang': 'cpp',
        'legenda': 'include/deriva/grade.hpp · regra do zero',
        'nota': 'Nenhuma das cinco operações especiais é declarada. O único membro que gerencia recurso é o `std::vector`, e as operações que o compilador gera são melhores que as que escreveríamos - e não ficam desatualizadas quando um membro novo aparecer.',
        'arquivo': 'exemplos/deriva/include/deriva/grade.hpp',
        'linha': 13,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A grade de células da estação.
///
/// Não declara destrutor, cópia, movimento nem atribuição: é a **regra do
/// zero** (Aula 09). O único membro que gerencia recurso é o
/// `std::vector`, e ele já sabe se copiar, se mover e se destruir
/// corretamente. As cinco operações que o compilador gera são melhores do que
/// as que escreveríamos aqui - e não podem ficar desatualizadas quando um
/// membro novo aparecer.
///
/// A variante `variantes/v0.3-quebrada/` faz o oposto: guarda `celula*` cru,
/// declara destrutor e esquece a cópia. É a **caça ao bug 1** da semana 5, e
/// o contador de instâncias vivas é o que a acusa.
class grade {
 public:
  grade(int largura, int altura);

  [[nodiscard]] int largura() const noexcept { return largura_; }
  [[nodiscard]] int altura() const noexcept { return altura_; }
  [[nodiscard]] bool dentro(vetor2 p) const noexcept;

  /// Sem verificação de limite: quem chama já perguntou `dentro()`.
  /// O `operator[]` de `mapa` chega na v1.5 (Aula 15).
  [[nodiscard]] const celula& em(vetor2 p) const;
  [[nodiscard]] celula& em(vetor2 p);

  /// Quantos bytes as células ocupam de fato. Serve à Aula 07: com
  /// `celula_ingenua` este número cresce um terço sem nada mudar de
  /// significado.
  [[nodiscard]] std::size_t bytes_das_celulas() const noexcept;

 private:
  int largura_;
  int altura_;
  std::vector<celula> celulas_;
};""",
    },
    'grade-quebrada': {
        'aula': 9,
        'lang': 'cpp',
        'legenda': 'v0.3-quebrada · cópia rasa · CAÇA AO BUG 1',
        'nota': 'Destrutor declarado, cópia esquecida: a violação mais barata da regra do três, e a que mais sobrevive à revisão. `-Wall -Wextra -Wpedantic` não emite uma palavra sobre isto.',
        'arquivo': 'exemplos/deriva/variantes/v0.3-quebrada/grade_quebrada.cpp',
        'linha': 26,
        'quebrado_de_proposito': True,
        'codigo': """\
/// A grade da v0.3, com uma diferença: o buffer é um ponteiro cru, e a posse
/// dele é do destrutor.
class grade {
 public:
  grade(int largura, int altura)
      : largura_(largura),
        altura_(altura),
        dados_(new celula[static_cast<std::size_t>(largura) *
                          static_cast<std::size_t>(altura)]) {}

  // Destrutor declarado. A partir daqui, a cópia gerada pelo compilador
  // passou a ser um erro - e o compilador não avisa, porque gerar cópia
  // membro a membro é exatamente o que a linguagem manda fazer.
  ~grade() { delete[] dados_; }

  // FALTA: grade(const grade&)
  // FALTA: grade& operator=(const grade&)
  // (é a regra do três, e ela está pela metade)

  [[nodiscard]] celula& em(int x, int y) {
    return dados_[static_cast<std::size_t>(y) * static_cast<std::size_t>(largura_) +
                  static_cast<std::size_t>(x)];
  }
  [[nodiscard]] const celula* buffer() const noexcept { return dados_; }

 private:
  int largura_;
  int altura_;
  celula* dados_;
};""",
    },
    'copia-nao-pedida': {
        'aula': 9,
        'lang': 'cpp',
        'legenda': 'testes/test_mapa.cpp · o contador como portão',
        'nota': 'Três objetos nascem para um `carregar`, e o contador soma os três. Repare no que ele NÃO distingue: depois de a Aula 14 acrescentar o construtor de movimento, o número continua três, porque continuam sendo três nascimentos - o que mudou foi o custo de cada um. O contador conta objetos, não alocações, e saber o que o instrumento não vê vale tanto quanto saber usá-lo.',
        'arquivo': 'exemplos/deriva/testes/test_mapa.cpp',
        'linha': 60,
        'quebrado_de_proposito': False,
        'codigo': """\
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
    }""",
    },
    'ciclo-medido': {
        'aula': 13,
        'lang': 'cpp',
        'legenda': 'include/deriva/medida_posse.hpp · o ciclo, medido',
        'nota': 'O vazamento do ciclo não dá para travar em `static_assert`: o tamanho do bloco de controle é escolha da implementação. Então ele é medido, por um alocador que conta exatamente o que o `shared_ptr` pede.',
        'arquivo': 'exemplos/deriva/include/deriva/medida_posse.hpp',
        'linha': 72,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Monta o ciclo, deixa os dois `shared_ptr` locais morrerem, e devolve
/// quantos bytes ficaram presos. Com `usar_weak`, uma das pontas passa a
/// observar em vez de possuir, e o resultado tem de ser zero.
template <class Aloc>
[[nodiscard]] std::size_t bytes_presos(bool usar_weak) {
  contagem::zerar();
  {
    auto a = std::allocate_shared<no>(Aloc{}, no{"eclusa", nullptr, {}});
    auto b = std::allocate_shared<no>(Aloc{}, no{"corredor", nullptr, {}});
    a->vizinho = b;
    if (usar_weak) {
      b->volta = a;      // observa: a contagem de `a` não sobe
    } else {
      b->vizinho = a;    // possui: fecha o ciclo, e ninguém chega a zero
    }""",
    },
    'alocador-que-conta': {
        'aula': 13,
        'lang': 'cpp',
        'legenda': 'include/deriva/medida_posse.hpp · a armadilha do rebind',
        'nota': '`std::allocate_shared` não usa o alocador que você passa: ele o rebinda para o tipo interno do bloco de controle. Contador `inline static` dentro do template conta na instanciação errada, e a primeira versão desta medida deu zero byte vazado por isso.',
        'arquivo': 'exemplos/deriva/include/deriva/medida_posse.hpp',
        'linha': 24,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Os contadores vivem FORA do template, e há um motivo que custou uma
/// depuração: `std::allocate_shared` não usa o alocador que você passa. Ele o
/// rebinda para o tipo interno do bloco de controle, e um `inline static`
/// dentro de `contando<T>` passaria a contar em `contando<no>` enquanto as
/// alocações reais aconteceriam em `contando<_Sp_counted_ptr_inplace<...>>`.
/// A primeira versão deste cabeçalho media zero byte vazado por isso.
struct contagem {
  inline static std::size_t pedidos = 0;
  inline static std::size_t devolvidos = 0;
  inline static std::size_t bytes_pedidos = 0;
  inline static std::size_t bytes_devolvidos = 0;

  static void zerar() noexcept {
    pedidos = devolvidos = bytes_pedidos = bytes_devolvidos = 0;
  }
  [[nodiscard]] static std::size_t vazados() noexcept {
    return bytes_pedidos - bytes_devolvidos;
  }
};""",
    },
    'hierarquia-entidade': {
        'aula': 10,
        'lang': 'cpp',
        'legenda': 'include/deriva/entidade.hpp · a base que o domínio pediu',
        'nota': 'A hierarquia é a que o domínio pede: sonda, drone e item são coisas diferentes que ocupam posição e desenham um glifo. O contador de instâncias mora em cada classe concreta, não na base - o da base contaria objetos e não tipos.',
        'arquivo': 'exemplos/deriva/include/deriva/entidade.hpp',
        'linha': 15,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Qualquer coisa que ocupa uma célula e faz algo por turno.
///
/// A hierarquia é a que o domínio pede, não taxonomia inventada para o
/// exercício: uma sonda, um drone e um item são coisas diferentes que ocupam
/// posição e desenham um glifo. O que varia é o que cada uma faz no turno.
///
/// **Abstrata** (v1.1): `desenhar` é puramente virtual, então `entidade` não
/// se instancia. Isso não é cerimônia - uma entidade sem glifo não tem
/// significado no domínio, e o compilador passa a dizer isso.
///
/// **Destrutor virtual** (v1.1): sem ele, `delete` por `entidade*` não roda o
/// destrutor da derivada, e nenhum aviso aparece quando o `delete` mora dentro
/// de um `unique_ptr`. A variante `variantes/v1.1-quebrada/` mede os três
/// casos. É a caça ao bug 2.
///
/// O contador de instâncias vivas mora em CADA classe concreta, escrito à mão,
/// e não na base. Duas razões: o contador da base contaria objetos e não tipos,
/// e a repetição é o que motiva o `contador_de_instancias<T>` da Aula 19.
class entidade {
 public:
  explicit entidade(vetor2 pos) noexcept : pos_(pos) {}

  virtual ~entidade() = default;

  // Base polimórfica não se copia por valor: copiar por `entidade&` fatiaria
  // o objeto. A cópia correta é `clonar`, que a Aula 25 transforma em padrão.
  entidade(const entidade&) = delete;
  entidade& operator=(const entidade&) = delete;

  [[nodiscard]] virtual char glifo() const = 0;
  [[nodiscard]] virtual std::string_view nome() const = 0;

  /// Um turno. A base não faz nada, e a derivada que não age não precisa
  /// dizer nada - é o caso do `item`.
  virtual void agir(mundo&) {}

  [[nodiscard]] vetor2 pos() const noexcept { return pos_; }
  void mover_para(vetor2 p) noexcept { pos_ = p; }

  /// Não-virtual de propósito, e chamando o virtual: é o Template Method na
  /// sua forma mais curta. A moldura do texto é da base; o glifo é da
  /// derivada (Aula 11).
  [[nodiscard]] std::string descrever() const;

 private:
  vetor2 pos_;
};""",
    },
    'final-retirado': {
        'aula': 10,
        'lang': 'cpp',
        'legenda': 'include/deriva/entidade.hpp · o `final` que teve de sair',
        'nota': 'Na v1.0 esta classe era `final`. A v1.7 introduziu a `sonda_reparadora` e o compilador recusou: "cannot derive from final base". A palavra saiu, e a lição fica - `final` é promessa, e retirá-la é admitir que a hierarquia mudou de forma.',
        'arquivo': 'exemplos/deriva/include/deriva/entidade.hpp',
        'linha': 63,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A sonda que o estudante opera. Tem energia, e gasta energia agindo.
///
/// **Não é `final`, e já foi.** Na v1.0 esta classe era `final`, porque nada
/// derivava dela e a palavra documentava a intenção. A v1.7 introduziu
/// `sonda_reparadora`, e o compilador recusou: "cannot derive from final base".
/// A palavra saiu, e a lição fica: `final` é promessa, não decoração, e
/// retirá-la é admitir que a hierarquia mudou de forma. Quem depende de a
/// classe ser folha - devirtualização, por exemplo - perde a garantia nesse
/// instante (Aula 11 e Aula 17).
class sonda : public entidade {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  explicit sonda(vetor2 pos, int energia = 100) noexcept
      : entidade(pos), energia_(energia) {
    ++vivos;
    ++criados;
  }
  ~sonda() override { --vivos; }

  [[nodiscard]] char glifo() const override { return '@'; }
  [[nodiscard]] std::string_view nome() const override { return "sonda"; }
  void agir(mundo& m) override;

  [[nodiscard]] int energia() const noexcept { return energia_; }
  void gastar(int quanto) noexcept;

 private:
  int energia_;""",
    },
    'template-method': {
        'aula': 10,
        'lang': 'cpp',
        'legenda': 'src/entidade.cpp · Template Method na forma mais curta',
        'nota': 'Não-virtual chamando virtual: a moldura do texto é da base, o glifo e o nome são da derivada, e nenhuma derivada reescreve o formato.',
        'arquivo': 'exemplos/deriva/src/entidade.cpp',
        'linha': 9,
        'quebrado_de_proposito': False,
        'codigo': """\
std::string entidade::descrever() const {
  // A moldura é da base, o glifo e o nome são da derivada. Nenhuma derivada
  // reescreve este texto, e nenhuma precisa.
  std::string s;
  s.push_back(glifo());
  s.append(" ").append(nome());
  s.append(" @ ").append(std::to_string(pos().x)).append(",")
   .append(std::to_string(pos().y));
  return s;
}""",
    },
    'destrutor-virtual-provado': {
        'aula': 11,
        'lang': 'cpp',
        'legenda': 'testes/test_entidade.cpp · a prova do destrutor virtual',
        'nota': 'O contador de cada classe concreta é o que acusa. Sem `virtual` no destrutor da base, `sonda::vivos` ficaria em 1 no fim do escopo - e nenhum aviso apareceria, porque o `delete` mora dentro do `unique_ptr`.',
        'arquivo': 'exemplos/deriva/testes/test_entidade.cpp',
        'linha': 42,
        'quebrado_de_proposito': False,
        'codigo': """\
// A prova do destrutor virtual: deletar por ponteiro da base tem de rodar o
// destrutor da derivada, e o contador de CADA classe concreta e o que acusa.
TEST_CASE("deletar por entidade* destroi a derivada") {
  zerar_entidades();
  {
    std::unique_ptr<entidade> e = std::make_unique<sonda>(vetor2{1, 1});
    REQUIRE(sonda::vivos == 1);
  }""",
    },
    'tres-avisos': {
        'aula': 11,
        'lang': 'cpp',
        'legenda': 'v1.1-quebrada · destrutor não virtual · CAÇA AO BUG 2',
        'nota': 'Medido em g++ 13.3: `delete` textual dá 1 aviso; o mesmo `delete` dentro de `unique_ptr` dá ZERO, porque passou a morar num cabeçalho do sistema; com `-Wnon-virtual-dtor` são 3, e nas declarações. C++ moderno, correto em tudo o mais, silenciou o único diagnóstico.',
        'arquivo': 'exemplos/deriva/variantes/v1.1-quebrada/destrutor_quebrado.cpp',
        'linha': 39,
        'quebrado_de_proposito': True,
        'codigo': """\
/// A base da hierarquia da v1.0. Tem função virtual, então é polimórfica -
/// e é para ser usada por ponteiro de base.
struct entidade {
  explicit entidade(char glifo) : glifo_(glifo) {
    ++contador::vivos;
    ++contador::criados;
  }

  // FALTA a palavra `virtual` aqui. É a única diferença entre esta variante e
  // a v1.1 boa.
  ~entidade() {
    ++contador::destrutores_de_base;
    --contador::vivos;
  }

  virtual void desenhar() const { std::putchar(glifo_); }

 protected:
  char glifo_;
};""",
    },
    'posse-no-tipo': {
        'aula': 12,
        'lang': 'cpp',
        'legenda': 'include/deriva/mundo.hpp · a posse declarada no tipo',
        'nota': '`vector<unique_ptr<entidade>>` diz quem é o dono sem precisar de comentário, e não há um `delete` em todo o Deriva. O par com o destrutor virtual é o que amarra as Aulas 11 e 12.',
        'arquivo': 'exemplos/deriva/include/deriva/mundo.hpp',
        'linha': 16,
        'quebrado_de_proposito': False,
        'codigo': """\
/// O estado do domínio: um setor e as entidades que estão nele.
///
/// A posse é **exclusiva e declarada no tipo**:
/// `std::vector<std::unique_ptr<entidade>>`. O `mundo` é o dono, e o tipo diz
/// isso sem precisar de comentário. Não há um `delete` em todo o Deriva.
///
/// O par `unique_ptr<entidade>` + destrutor virtual é o que amarra as Aulas 11
/// e 12: sem o destrutor virtual, este vetor destruiria só a parte base de
/// cada objeto, e nenhum aviso apareceria - porque o `delete` mora dentro do
/// `unique_ptr`, num cabeçalho do sistema. É o achado da variante
/// `v1.1-quebrada`.
///
/// `mundo` é movível e não copiável, e isso não é escolha de estilo: copiar
/// exigiria clonar polimorficamente cada entidade, o que é decisão de projeto
/// da Aula 25 (Factory), não operação implícita.
class mundo {
 public:
  explicit mundo(mapa m);

  mundo(const mundo&) = delete;
  mundo& operator=(const mundo&) = delete;
  mundo(mundo&&) noexcept = default;
  mundo& operator=(mundo&&) noexcept = default;
  ~mundo() = default;

  [[nodiscard]] const mapa& setor() const noexcept { return setor_; }
  [[nodiscard]] mapa& setor() noexcept { return setor_; }

  /// Toma posse. O `&&` na assinatura é o contrato: quem chama entrega o
  /// ponteiro e não fica com uma cópia dele.
  entidade& acrescentar(std::unique_ptr<entidade> e);

  /// Célula dentro do setor e sem parede. Não considera entidades: duas podem
  /// ocupar a mesma célula, e é a v2.6 que decide se isso é permitido.
  [[nodiscard]] bool livre(vetor2 p) const;

  /// Um turno para cada entidade, na ordem em que entraram. A ordem é parte
  /// do comportamento observável, e o replay depende dela.
  void turno();

  [[nodiscard]] std::size_t quantas() const noexcept { return entidades_.size(); }
  [[nodiscard]] const entidade& em(std::size_t i) const { return *entidades_[i]; }
  [[nodiscard]] entidade& em(std::size_t i) { return *entidades_[i]; }

  /// A primeira entidade cujo glifo casa, ou `nullptr`. Devolve ponteiro cru
  /// de propósito: é observação, não posse, e o tipo tem de dizer a diferença
  /// (Aula 12).
  [[nodiscard]] entidade* primeira_com(char glifo) const;

  /// Remove quem estiver na posição. Devolve o ponteiro: quem chamou passa a
  /// ser o dono, e se ignorar o retorno o objeto morre - daí o
  /// `[[nodiscard]]`.
  [[nodiscard]] std::unique_ptr<entidade> retirar_de(vetor2 p);

  /// Render determinístico: o setor com as entidades por cima, e a listagem.
  /// Mesma entrada, mesma saída, byte a byte.
  [[nodiscard]] std::string despejar() const;

 private:
  mapa setor_;
  std::vector<std::unique_ptr<entidade>> entidades_;
};""",
    },
    'transferir-posse': {
        'aula': 12,
        'lang': 'cpp',
        'legenda': 'src/mundo.cpp · devolver posse é devolver o ponteiro',
        'nota': 'O retorno é `[[nodiscard]]` porque ignorá-lo destrói o objeto na hora. Compare com `primeira_com`, que devolve ponteiro cru: ali é observação, e o tipo tem de dizer a diferença.',
        'arquivo': 'exemplos/deriva/src/mundo.cpp',
        'linha': 35,
        'quebrado_de_proposito': False,
        'codigo': """\
std::unique_ptr<entidade> mundo::retirar_de(vetor2 p) {
  const auto it = std::find_if(entidades_.begin(), entidades_.end(),
                               [p](const std::unique_ptr<entidade>& e) {
                                 return e->pos() == p;
                               });
  if (it == entidades_.end()) return nullptr;
  std::unique_ptr<entidade> saindo = std::move(*it);
  entidades_.erase(it);
  return saindo;
}""",
    },
    'shared-e-weak': {
        'aula': 13,
        'lang': 'cpp',
        'legenda': 'src/estacao.cpp · a assimetria que impede o ciclo',
        'nota': 'Duas linhas, e é nelas que está a lição: a ligação para frente possui e a de volta observa. Trocar `volta_` por `shared_ptr` fecha o ciclo e prende 160 bytes por par de nós.',
        'arquivo': 'exemplos/deriva/src/estacao.cpp',
        'linha': 14,
        'quebrado_de_proposito': False,
        'codigo': """\
void no_estacao::ligar(const std::shared_ptr<no_estacao>& a,
                       const std::shared_ptr<no_estacao>& b) {
  a->adiante_.push_back(b);   // posse: a contagem de b sobe
  b->volta_ = a;              // observação: a contagem de a NÃO sobe
}""",
    },
    'weak-obriga-perguntar': {
        'aula': 13,
        'lang': 'cpp',
        'legenda': 'testes/test_estacao.cpp · weak_ptr não pendura',
        'nota': '`lock()` devolve `nullptr` quando o objeto morreu. É a pergunta obrigatória que torna o ponteiro pendurado impossível - e é o que `shared_ptr` na volta impediria de acontecer, porque o objeto nunca morreria.',
        'arquivo': 'exemplos/deriva/testes/test_estacao.cpp',
        'linha': 45,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("weak_ptr obriga a perguntar, e por isso nao pendura") {
  zerar_estacao();
  std::shared_ptr<no_estacao> b;
  {
    auto a = std::make_shared<no_estacao>("a");
    b = std::make_shared<no_estacao>("b");
    no_estacao::ligar(a, b);
    REQUIRE(b->anterior() != nullptr);
  }""",
    },
    'origem-esvazia': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'testes/test_move_string.cpp · a origem, nos quatro casos',
        'nota': 'Curta e longa, construção e atribuição: a origem esvazia nos quatro. É justamente porque `REQUIRE(origem.empty())` PASSA aqui que o folclore sobrevive e o erro embarca - o padrão promete estado válido, não vazio.',
        'arquivo': 'exemplos/deriva/testes/test_move_string.cpp',
        'linha': 28,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("nesta implementacao a origem esvazia nos quatro casos") {
  SECTION("curta, por construcao") {
    std::string a(kCurta);
    const std::string b(std::move(a));
    REQUIRE(b == kCurta);
    REQUIRE(a.empty());
  }""",
    },
    'copia-ou-ponteiro': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'testes/test_move_string.cpp · a diferença que se reproduz',
        'nota': 'Curta: o endereço do destino é NOVO, porque oito bytes foram copiados - não havia ponteiro a roubar. Longa: o mesmo ponteiro de heap troca de dono, e nenhum byte de conteúdo se move.',
        'arquivo': 'exemplos/deriva/testes/test_move_string.cpp',
        'linha': 55,
        'quebrado_de_proposito': False,
        'codigo': """\
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
  }""",
    },
    'move-de-mapa': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'src/mapa.cpp · o construtor de movimento',
        'nota': '`noexcept` não é decoração: `std::vector<mapa>` só usa o movimento ao realocar se ele for `noexcept`; sem a palavra, copia.',
        'arquivo': 'exemplos/deriva/src/mapa.cpp',
        'linha': 41,
        'quebrado_de_proposito': False,
        'codigo': """\
// Mover um mapa não copia a grade: o `std::vector` de dentro dela transfere o
// ponteiro do heap. O que ainda custa é o contador - um objeto NASCEU, mesmo
// que sem alocar, e por isso `criados` sobe.
//
// `noexcept` não é decoração: `std::vector<mapa>` só usa o movimento ao
// realocar se ele for `noexcept`; sem a palavra, ele copia (Aula 14).
mapa::mapa(mapa&& o) noexcept
    : nome_(std::move(o.nome_)),
      grade_(std::move(o.grade_)),
      entrada_(o.entrada_),
      marca_(std::move(o.marca_)) {
  ++contador_mapa::vivos;
  ++contador_mapa::criados;
}""",
    },
    'move-transfere-buffer': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'testes/test_mapa.cpp · o que o movimento muda',
        'nota': 'Mover devolve o MESMO endereço de buffer; copiar devolve um novo. E o contador não distingue os dois, porque conta objetos e não alocações.',
        'arquivo': 'exemplos/deriva/testes/test_mapa.cpp',
        'linha': 122,
        'quebrado_de_proposito': False,
        'codigo': """\
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
}""",
    },
    'operadores-livres': {
        'aula': 15,
        'lang': 'cpp',
        'legenda': 'include/deriva/vetor2.hpp · binário é função livre',
        'nota': 'O composto é membro porque modifica o objeto da esquerda; o binário é livre porque trata os dois lados igual. Escrever `+` em termos de `+=` é a forma que não duplica a regra.',
        'arquivo': 'exemplos/deriva/include/deriva/vetor2.hpp',
        'linha': 55,
        'quebrado_de_proposito': False,
        'codigo': """\
// Funções livres: simétricas por construção, e é isso que as torna a forma
// idiomática. Um `operator+` membro aceitaria `a + b` e recusaria conversões
// do lado esquerdo.
[[nodiscard]] constexpr vetor2 operator+(vetor2 a, const vetor2& b) noexcept {
  return a += b;
}""",
    },
    'par-const-nao-const': {
        'aula': 15,
        'lang': 'cpp',
        'legenda': 'include/deriva/mapa.hpp · o par que existe por uma razão',
        'nota': 'Uma sobrecarga só, devolvendo referência não-const, permitiria escrever através de um mapa constante; devolvendo referência const, impediria escrever em qualquer um.',
        'arquivo': 'exemplos/deriva/include/deriva/mapa.hpp',
        'linha': 79,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Render determinístico. Mesma entrada, mesma saída, byte a byte - é o que
/// torna o replay da Aula 16 possível.
/// v1.5 · Aula 15. O par const / não-const existe porque `mapa` const tem
/// de deixar LER a célula e não deixar escrever nela. Uma sobrecarga só,
/// devolvendo referência não-const, permitiria escrever através de um mapa
/// constante; devolvendo referência const, impediria escrever em qualquer um.
[[nodiscard]] const celula& operator[](vetor2 p) const { return grade_.em(p); }
[[nodiscard]] celula& operator[](vetor2 p) { return grade_.em(p); }""",
    },
    'fov-puro': {
        'aula': 16,
        'lang': 'cpp',
        'legenda': 'src/fov.cpp · Bresenham em inteiros',
        'nota': 'Nenhum ponto flutuante, nenhum arredondamento dependente de plataforma. É essa propriedade que o replay compra, e é por isso que o campo de visão é o PRIMEIRO alvo dos testes e não o último: função pura se testa sem montar o mundo.',
        'arquivo': 'exemplos/deriva/src/fov.cpp',
        'linha': 7,
        'quebrado_de_proposito': False,
        'codigo': """\
std::vector<vetor2> linha(vetor2 a, vetor2 b) {
  // Bresenham em inteiros. Nenhum ponto flutuante, nenhum arredondamento
  // dependente de plataforma: a mesma entrada dá a mesma linha em qualquer
  // máquina, e é essa propriedade que o replay da Aula 16 compra.
  std::vector<vetor2> pontos;
  int x = a.x, y = a.y;
  const int dx = std::abs(b.x - a.x), dy = std::abs(b.y - a.y);
  const int sx = a.x < b.x ? 1 : -1, sy = a.y < b.y ? 1 : -1;
  int erro = dx - dy;
  for (;;) {
    pontos.push_back({x, y});
    if (x == b.x && y == b.y) break;
    const int e2 = 2 * erro;
    if (e2 > -dy) { erro -= dy; x += sx; }
    if (e2 < dx) { erro += dx; y += sy; }
  }""",
    },
    'diamante-medido': {
        'aula': 17,
        'lang': 'cpp',
        'legenda': 'include/deriva/diamante.hpp · os números do diamante',
        'nota': 'Contraria a intuição, e por isso está medido: a herança virtual é a MAIOR das três formas, 48 bytes contra 40 da duplicada. O que ela compra não é tamanho, é correção - um campo em vez de dois ambíguos.',
        'arquivo': 'exemplos/deriva/include/deriva/diamante.hpp',
        'linha': 39,
        'quebrado_de_proposito': False,
        'codigo': """\
// Os números medidos em g++ 13.3 x86-64, e eles contrariam a intuição:
//
//   nucleo                16    vptr 8 + int 4 + padding 4
//   movel / sensor        16    a base cabe no mesmo alinhamento
//   patrulha_duplicada    40    DUAS bases de 16, mais rota e padding
//   patrulha_unica        48    UMA base, e mais um ponteiro por ramo virtual
//   patrulha_composta     56    nenhum diamante, e o maior de todos
//
// A herança virtual é a MAIOR das três, não a menor. O ponteiro para a base
// virtual que cada ramo carrega custa mais do que duplicar uma base de 16
// bytes. Escrever aqui que ela "economiza memória" seria mentir, e a primeira
// versão deste cabeçalho tinha um `static_assert` invertido afirmando
// exatamente isso - o compilador o recusou.
//
// O que a herança virtual compra não é tamanho: é **correção**. Na forma
// duplicada existem dois campos `leituras` com endereços diferentes, e nenhum
// dos dois é "o" valor; escrever por um ramo e ler pelo outro devolve lixo
// coerente. Na forma virtual existe um campo só. É por isso que se paga.
static_assert(sizeof(nucleo) == 16, "vptr 8 + int 4 + padding 4");
static_assert(sizeof(patrulha_duplicada) == 40, "duas bases de 16, mais rota");
static_assert(sizeof(patrulha_unica) == 48, "uma base, mais um ponteiro por ramo");
static_assert(sizeof(patrulha_unica) > sizeof(patrulha_duplicada),
              "a indireção virtual custa MAIS bytes que a duplicação que evita");""",
    },
    'interface-pura': {
        'aula': 17,
        'lang': 'cpp',
        'legenda': 'include/deriva/reparadora.hpp · o caso fácil',
        'nota': 'Interface pura é o único uso de herança múltipla que este material recomenda sem ressalva: nenhum dado, então não há o que duplicar, e o diamante que ela formaria é inofensivo.',
        'arquivo': 'exemplos/deriva/include/deriva/reparadora.hpp',
        'linha': 13,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Interface pura: nenhum dado, nenhum construtor, destrutor virtual.
///
/// Interface pura é o **único** uso de herança múltipla que este material
/// recomenda sem ressalva. Ela não traz estado, então não há o que duplicar,
/// e o diamante que ela formaria é inofensivo.
class i_reparavel {
 public:
  virtual ~i_reparavel() = default;
  [[nodiscard]] virtual bool reparar(celula& c) = 0;
  [[nodiscard]] virtual int reparos_feitos() const = 0;
};""",
    },
    'cadeia-dynamic-cast': {
        'aula': 18,
        'lang': 'cpp',
        'legenda': 'src/inspetor.cpp · a ordem da cadeia é obrigatória',
        'nota': 'A `sonda_reparadora` também É `sonda`, então testá-la depois nunca aconteceria. Perguntar pelo tipo mais derivado primeiro é a armadilha número um - e é o argumento de que essa cadeia deveria ser uma função virtual.',
        'arquivo': 'exemplos/deriva/src/inspetor.cpp',
        'linha': 10,
        'quebrado_de_proposito': False,
        'codigo': """\
std::string inspecionar(const entidade& e) {
  std::string s = e.descrever();

  // A ordem importa: `sonda_reparadora` também É `sonda`, então testá-la
  // depois nunca aconteceria. Perguntar pelo tipo mais derivado primeiro é a
  // armadilha número um de cadeia de dynamic_cast - e é o argumento de que
  // essa cadeia deveria ser uma função virtual.
  if (const auto* r = dynamic_cast<const sonda_reparadora*>(&e)) {
    s.append("  [reparadora, ").append(std::to_string(r->reparos_feitos()))
     .append(" reparo(s), energia ").append(std::to_string(r->energia())).append("]");
  } else if (const auto* sd = dynamic_cast<const sonda*>(&e)) {
    s.append("  [sonda, energia ").append(std::to_string(sd->energia())).append("]");
  } else if (const auto* dr = dynamic_cast<const drone*>(&e)) {
    s.append("  [drone, rumo ").append(std::to_string(dr->rumo().x)).append(",")
     .append(std::to_string(dr->rumo().y)).append("]");
  } else if (const auto* it = dynamic_cast<const item*>(&e)) {
    s.append("  [item, massa ").append(std::to_string(it->massa())).append("]");
  }""",
    },
    'cast-para-interface': {
        'aula': 18,
        'lang': 'cpp',
        'legenda': 'src/inspetor.cpp · perguntar por capacidade, não por tipo',
        'nota': '`dynamic_cast` para a interface, e não para a classe concreta: é a pergunta certa, porque o que interessa é a capacidade. Este é o único lugar do Deriva onde `dynamic_cast` é a resposta e não o sintoma.',
        'arquivo': 'exemplos/deriva/src/inspetor.cpp',
        'linha': 31,
        'quebrado_de_proposito': False,
        'codigo': """\
std::string listar_reparadoras(const mundo& m) {
  std::string s;
  int achadas = 0;
  for (std::size_t i = 0; i < m.quantas(); ++i) {
    // `dynamic_cast` para a INTERFACE, e não para a classe concreta: é a
    // pergunta certa, porque o que interessa é a capacidade e não o tipo.
    if (dynamic_cast<const i_reparavel*>(&m.em(i)) != nullptr) {
      s.append("  ").append(m.em(i).descrever()).append("\\n");
      ++achadas;
    }""",
    },
    'custo-do-vptr': {
        'aula': 11,
        'lang': 'cpp',
        'legenda': 'include/deriva/leiaute.hpp · quanto custa o vptr',
        'nota': '8 bytes por OBJETO, não por classe. E o custo não desaparece quando a derivada acrescenta dado: ele se soma - 8 do vptr, 8 da posição, 4 da carga, 4 de padding.',
        'arquivo': 'exemplos/deriva/include/deriva/leiaute.hpp',
        'linha': 16,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Sem nenhum método virtual: não há vtable, e portanto não há `vptr`.
struct entidade_simples {
  vetor2 pos;
};
struct drone_simples : entidade_simples {};

/// Com um método virtual: o compilador põe um ponteiro para a vtable como
/// primeiro campo do objeto. São 8 bytes por OBJETO, não por classe.
struct entidade {
  vetor2 pos;
  virtual ~entidade() = default;
  virtual void desenhar() const = 0;
};
struct drone : entidade {
  void desenhar() const override {}
};

/// E quando a derivada acrescenta dado, o custo do vptr não desaparece - ele
/// se soma. É a v1.2, quando o drone ganha carga.
struct drone_com_carga : entidade {
  int carga = 0;
  void desenhar() const override {}
};

static_assert(sizeof(entidade_simples) == 8, "só a posição");
static_assert(sizeof(drone_simples) == 8, "herdar de classe não-polimórfica é grátis");
static_assert(sizeof(entidade) == 16, "8 do vptr + 8 da posição");
static_assert(sizeof(drone) == 16, "a derivada sem dado novo não cresce");
static_assert(sizeof(drone_com_carga) == 24, "8 vptr + 8 pos + 4 carga + 4 de padding");""",
    },
    'crtp-contador': {
        'aula': 19,
        'lang': 'cpp',
        'legenda': 'include/deriva/contador_crtp.hpp · o contador generalizado',
        'nota': 'O parâmetro `T` é o truque: cada instanciação é um TIPO diferente, logo tem os seus próprios `vivos`. Herança comum compartilharia um contador só entre todas as derivadas, que é exatamente o erro que o contador na base cometeria.',
        'arquivo': 'exemplos/deriva/include/deriva/contador_crtp.hpp',
        'linha': 30,
        'quebrado_de_proposito': False,
        'codigo': """\
class contador_de_instancias {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  static void zerar() noexcept { vivos = criados = 0; }

  /// Verdadeiro quando todo objeto deste tipo já foi destruído. É o que o
  /// portão `make verifica` consulta.
  [[nodiscard]] static bool fechou() noexcept { return vivos == 0; }

 protected:
  // Protegido e não-virtual: esta base não é para ser usada por ponteiro, e
  // por isso não paga destrutor virtual. Quem herdar dela e for base
  // polimórfica declara o SEU destrutor virtual, como `entidade` faz.
  contador_de_instancias() noexcept {
    ++vivos;
    ++criados;
  }
  contador_de_instancias(const contador_de_instancias&) noexcept {
    ++vivos;
    ++criados;   // cópia também é nascimento, e o manual esquecia disso
  }
  contador_de_instancias(contador_de_instancias&&) noexcept {
    ++vivos;
    ++criados;
  }
  contador_de_instancias& operator=(const contador_de_instancias&) noexcept {
    return *this;   // atribuição não cria nem destrói
  }
  contador_de_instancias& operator=(contador_de_instancias&&) noexcept {
    return *this;
  }
  ~contador_de_instancias() noexcept { --vivos; }
};""",
    },
    'if-constexpr-poda': {
        'aula': 19,
        'lang': 'cpp',
        'legenda': 'include/deriva/grade_generica.hpp · if constexpr no despejo',
        'nota': 'Com `if` comum os três ramos teriam de ser válidos para todo `T`, e `c.glifo` não existe em `int` - não compilaria. É a diferença que `if constexpr` faz, e o motivo pelo qual ele substitui SFINAE.',
        'arquivo': 'exemplos/deriva/include/deriva/grade_generica.hpp',
        'linha': 65,
        'quebrado_de_proposito': False,
        'codigo': """\
/// O despejo depende do que `T` é, e a decisão acontece em tempo de
/// COMPILAÇÃO. Com `if` comum, os três ramos teriam de ser válidos para
/// todo `T` - e `c.glifo` não existe em `int`, então nem compilaria. É a
/// diferença que `if constexpr` faz, e o motivo pelo qual ele substitui
/// SFINAE (Aula 19).
[[nodiscard]] std::string despejar() const {
  std::string s;
  for (int y = 0; y < altura_; ++y) {
    for (int x = 0; x < largura_; ++x) {
      const T& c = em({x, y});
      if constexpr (std::is_same_v<T, celula>) {
        s.push_back(c.glifo);
      } else if constexpr (std::is_same_v<T, char>) {
        s.push_back(c ? '+' : '.');
      } else if constexpr (std::is_integral_v<T>) {
        s.push_back(c < 0 ? '#' : static_cast<char>('0' + (c % 10)));
      } else {
        s.push_back('?');
      }""",
    },
    'static-assert-proprio': {
        'aula': 19,
        'lang': 'cpp',
        'legenda': 'include/deriva/grade_generica.hpp · a mensagem é a nossa',
        'nota': '`std::vector<bool>` empacota bits e devolve proxy, não `bool&`. Sem este `static_assert`, o estudante leria "cannot bind non-const lvalue reference to an rvalue" vindo de dentro da biblioteca.',
        'arquivo': 'exemplos/deriva/include/deriva/grade_generica.hpp',
        'linha': 32,
        'quebrado_de_proposito': False,
        'codigo': """\
// `std::vector<bool>` é a especialização mais famosa da biblioteca padrão, e
// a mais lamentada: ela empacota os bits, então `operator[]` devolve um
// PROXY e não um `bool&`. Uma grade que promete `T&` não pode ser
// instanciada com `bool`, e a mensagem abaixo é o que o estudante lê em vez
// de "cannot bind non-const lvalue reference to an rvalue".
//
// A saída é `char` ou `std::uint8_t`, e a v2.5 usa `char` no mapa do que já
// foi visitado. É por isso que a Aula 21 diz que `vector<bool>` não é um
// vetor de bool (Aula 19 e Aula 21).
static_assert(!std::is_same_v<T, bool>,
              "grade_de<bool> nao existe: std::vector<bool> empacota bits e "
              "devolve proxy, nao bool&. Use char ou std::uint8_t");""",
    },
    'tres-formas-de-erro': {
        'aula': 20,
        'lang': 'cpp',
        'legenda': 'include/deriva/erro.hpp · optional, variant ou exceção',
        'nota': 'Três formas de dizer que algo não deu certo, e a escolha está no tipo: `optional` para ausência, `variant` para erro esperado com informação, exceção para o que rompe a operação.',
        'arquivo': 'exemplos/deriva/include/deriva/erro.hpp',
        'linha': 69,
        'quebrado_de_proposito': False,
        'codigo': """\
/// O resultado de tentar interpretar um texto como mapa.
///
/// **A escolha de projeto da Aula 20**, e ela é declarada no tipo: três formas
/// de dizer que algo não deu certo, cada uma para um caso diferente.
///
/// - `std::optional` para **ausência**: o arquivo não existe. Não é erro, é
///   resposta. É o que `mapa::carregar` devolve desde a v0.3.
/// - `std::variant` para **erro esperado com informação**: o texto existe e
///   não é mapa, e quem chamou precisa saber por quê para decidir. Não é
///   exceção porque acontece no fluxo normal - o estudante vai errar o mapa
///   dele muitas vezes.
/// - **exceção** para o que rompe a operação: não deu para LER o arquivo.
///   Quem chamou não tem o que decidir, e o desenrolar da pilha é a resposta
///   certa.
using resultado_de_mapa = std::variant<mapa, razao>;""",
    },
    'garantia-forte-barata': {
        'aula': 20,
        'lang': 'cpp',
        'legenda': 'src/erro.cpp · validar antes de construir',
        'nota': 'A garantia forte é barata aqui porque nada é alocado até se saber que o texto serve - não há o que desfazer. É por isso que a leitura é separada da aplicação.',
        'arquivo': 'exemplos/deriva/src/erro.cpp',
        'linha': 30,
        'quebrado_de_proposito': False,
        'codigo': """\
resultado_de_mapa interpretar(std::string_view texto, std::string nome) {
  // Repare que a validação acontece ANTES de qualquer construção: nada é
  // alocado até se saber que o texto serve. É o que torna a garantia forte
  // barata - não há o que desfazer.
  if (texto.empty()) return razao::vazio;

  std::size_t largura = 0, entradas = 0, fileiras = 0, inicio = 0;
  while (inicio <= texto.size()) {
    const std::size_t fim = texto.find('\\n', inicio);
    const std::string_view linha = texto.substr(
        inicio, fim == std::string_view::npos ? std::string_view::npos : fim - inicio);
    if (!linha.empty()) {
      if (fileiras == 0) largura = linha.size();
      else if (linha.size() != largura) return razao::fileira_torta;
      ++fileiras;
      for (const char c : linha) {
        if (c == '@') ++entradas;
        else if (c != '#' && c != '.' && c != '!') return razao::glifo_desconhecido;
      }""",
    },
    'clamp-no-lugar': {
        'aula': 21,
        'lang': 'cpp',
        'legenda': 'src/inventario.cpp · std::clamp em vez de min/max aninhado',
        'nota': '`clamp` devolve **referência**, e é a armadilha dele: não o alimente com temporário guardando o resultado por referência. Aqui o valor é copiado para um `int`, e é isso que o torna seguro.',
        'arquivo': 'exemplos/deriva/src/inventario.cpp',
        'linha': 10,
        'quebrado_de_proposito': False,
        'codigo': """\
inventario::inventario(int capacidade) noexcept
    // `std::clamp` no lugar do min/max aninhado: a capacidade fica entre 0 e
    // 999 sem que ninguém precise ler duas chamadas encaixadas para saber
    // disso. Cuidado com o retorno por referência - aqui o resultado é
    // copiado para um `int`, e é isso que o torna seguro.
    : capacidade_(std::clamp(capacidade, 0, 999)) {}""",
    },
    'erase-remove': {
        'aula': 21,
        'lang': 'cpp',
        'legenda': 'src/inventario.cpp · erase-remove',
        'nota': '`remove_if` empurra para o fim e devolve o novo fim; `erase` corta. Em C++20 seria `std::erase_if`, uma chamada só - e é por isso que o material nomeia o idioma antigo em vez de fingir que ele é natural.',
        'arquivo': 'exemplos/deriva/src/inventario.cpp',
        'linha': 51,
        'quebrado_de_proposito': False,
        'codigo': """\
std::size_t inventario::descartar_se(
    const std::function<bool(const componente&)>& criterio) {
  // Erase-remove. Em C++20: std::erase_if(pecas_, ...), uma chamada.
  const auto novo_fim = std::remove_if(
      pecas_.begin(), pecas_.end(),
      [&criterio](const std::unique_ptr<componente>& c) { return criterio(*c); });
  const std::size_t saiu = static_cast<std::size_t>(pecas_.end() - novo_fim);
  pecas_.erase(novo_fim, pecas_.end());
  return saiu;
}""",
    },
    'sort-deterministico': {
        'aula': 21,
        'lang': 'cpp',
        'legenda': 'src/inventario.cpp · o desempate que o replay exige',
        'nota': '`std::sort` é instável. Sem o desempate pelo rótulo, a ordem entre massas iguais seria a que o algoritmo quisesse, e o despejo deixaria de ser determinístico.',
        'arquivo': 'exemplos/deriva/src/inventario.cpp',
        'linha': 62,
        'quebrado_de_proposito': False,
        'codigo': """\
void inventario::ordenar_por_massa() {
  std::sort(pecas_.begin(), pecas_.end(),
            [](const std::unique_ptr<componente>& a,
               const std::unique_ptr<componente>& b) {
              // Desempate pelo rótulo: sem ele, a ordem entre massas iguais
              // seria a que o `sort` quisesse, e o despejo deixaria de ser
              // determinístico - o replay quebraria.
              if (a->massa() != b->massa()) return a->massa() > b->massa();
              return a->rotulo() < b->rotulo();
            });
}""",
    },
    'o-que-se-compartilha': {
        'aula': 22,
        'lang': 'cpp',
        'legenda': 'include/deriva/fila_de_comandos.hpp · a fila é a única fronteira',
        'nota': 'O `mundo` continua sendo de uma thread só. O que atravessa a fronteira são comandos, um por vez, protegidos - e é o oposto da tentação de deixar as duas threads mexerem no mundo.',
        'arquivo': 'exemplos/deriva/include/deriva/fila_de_comandos.hpp',
        'linha': 13,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A fila entre a thread que lê o teclado e a que desenha.
///
/// **O que se compartilha é esta fila, e nada mais.** É a decisão de projeto
/// da Aula 22, e ela é o oposto da tentação: seria mais fácil deixar as duas
/// threads mexerem no `mundo`, e é exatamente isso que produz a corrida que o
/// interativo mostra. Aqui o `mundo` continua sendo de uma thread só; o que
/// atravessa a fronteira são comandos, um por vez, protegidos.
///
/// `std::scoped_lock` (C++17) no lugar de `std::lock_guard`: aceita mais de um
/// mutex e resolve a ordem de travamento sozinho, o que elimina uma classe
/// inteira de impasse. Para um mutex só, os dois são equivalentes, e usar o
/// novo é hábito.
///
/// A condição de parada não é uma variável booleana lida sem proteção - esse é
/// o erro que a Aula 22 mostra medido. Ela é parte do estado guardado pelo
/// mesmo mutex, e a espera usa `condition_variable`, que acorda quem espera em
/// vez de queimar processador.
class fila_de_comandos {
 public:
  /// Põe um comando na fila e acorda quem estiver esperando.
  void empurrar(std::string comando);

  /// Bloqueia até haver comando ou a fila ser fechada. `std::nullopt` quando
  /// fechada e vazia - é o sinal de fim, e não uma exceção.
  [[nodiscard]] std::optional<std::string> puxar();

  /// Tira sem bloquear. Serve ao laço de render, que não pode parar.
  [[nodiscard]] std::optional<std::string> tentar_puxar();

  /// Fecha para sempre e acorda todos. Idempotente.
  void fechar();

  [[nodiscard]] bool fechada() const;
  [[nodiscard]] std::size_t tamanho() const;

 private:
  mutable std::mutex mutex_;
  std::condition_variable tem_coisa_;
  std::deque<std::string> fila_;
  bool fechada_ = false;
};""",
    },
    'wait-com-predicado': {
        'aula': 22,
        'lang': 'cpp',
        'legenda': 'src/fila_de_comandos.cpp · o predicado não é conveniência',
        'nota': 'Sem o predicado no `wait`, um despertar espúrio faria a thread seguir com a fila vazia. E notificar fora da região travada economiza uma ida e volta no escalonador.',
        'arquivo': 'exemplos/deriva/src/fila_de_comandos.cpp',
        'linha': 19,
        'quebrado_de_proposito': False,
        'codigo': """\
std::optional<std::string> fila_de_comandos::puxar() {
  std::unique_lock trava(mutex_);
  // O predicado no `wait` não é conveniência: sem ele, um despertar espúrio
  // faria a thread seguir com a fila vazia. Ele é reavaliado a cada despertar,
  // e é o que torna a espera correta.
  tem_coisa_.wait(trava, [this] { return !fila_.empty() || fechada_; });
  if (fila_.empty()) return std::nullopt;   // fechada e vazia: fim
  std::string c = std::move(fila_.front());
  fila_.pop_front();
  return c;
}""",
    },
    'teste-que-nao-afirma': {
        'aula': 22,
        'lang': 'cpp',
        'legenda': 'testes/test_concorrencia.cpp · o que não se pode afirmar',
        'nota': 'A primeira versão deste teste exigia que a corrida se manifestasse, e falhou no portão - oito execuções de dez não perdem nada. Teste que depende de comportamento indefinido é teste instável, e instável é pior que ausente: treina a equipe a reexecutar até passar.',
        'arquivo': 'exemplos/deriva/testes/test_concorrencia.cpp',
        'linha': 51,
        'quebrado_de_proposito': False,
        'codigo': """\
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
    }""",
    },
    'versao-primeiro': {
        'aula': 23,
        'lang': 'cpp',
        'legenda': 'src/partida.cpp · a versão é a primeira linha',
        'nota': 'Quem lê precisa saber com que regras ler antes de ler qualquer outra coisa. Ordem de linha fixa é o que permite comparar dois saves com `diff`, e é a mesma razão do replay.',
        'arquivo': 'exemplos/deriva/src/partida.cpp',
        'linha': 10,
        'quebrado_de_proposito': False,
        'codigo': """\
std::string partida::serializar() const {
  // A ordem das linhas é fixa e a versão vem primeiro. Ordem estável é o que
  // permite comparar dois saves com `diff`, e é a mesma razão do replay.
  std::ostringstream os;
  os << "deriva-partida " << versao << '\\n'
     << "setor " << setor << '\\n'
     << "sonda " << sonda.x << ' ' << sonda.y << '\\n'
     << "carga " << carga << '\\n'
     << "turno " << turno << '\\n'
     << "energia " << energia << '\\n';
  return os.str();
}""",
    },
    'compatibilidade-regressiva': {
        'aula': 23,
        'lang': 'cpp',
        'legenda': 'testes/test_partida.cpp · o padrão do membro responde pelo campo ausente',
        'nota': 'Sem esse padrão, a partida antiga carregaria com zero de energia e a sonda apareceria morta - o defeito clássico de migração de formato.',
        'arquivo': 'exemplos/deriva/testes/test_partida.cpp',
        'linha': 35,
        'quebrado_de_proposito': False,
        'codigo': """\
// Compatibilidade regressiva: um arquivo da versao 1 nao tem `energia`, e o
// leitor v2 tem de aceitar isso. O valor padrao do membro e o que responde
// por ele - sem esse padrao, a sonda carregaria com zero de energia e
// apareceria morta, que e o defeito classico de migracao de formato.
TEST_CASE("o leitor v2 abre uma partida v1") {
  const std::string v1 =
      "deriva-partida 1\\n"
      "setor estacao-01\\n"
      "sonda 4 5\\n"
      "carga 3\\n"
      "turno 10\\n";

  const auto lida = partida::desserializar(v1);
  REQUIRE(lida.has_value());
  REQUIRE(lida->versao == 1);
  REQUIRE(lida->sonda == vetor2{4, 5});
  REQUIRE(lida->energia == 100);   // o padrao, e nao zero
}""",
    },
    'most-vexing-parse': {
        'aula': 23,
        'lang': 'cpp',
        'legenda': 'src/partida.cpp · chaves, e não parênteses',
        'nota': '`std::istringstream is(std::string(texto));` é a *most vexing parse*: o compilador lê a DECLARAÇÃO de uma função. A inicialização uniforme da Aula 03 não tem essa ambiguidade, e é por isso que o material a recomenda desde o começo.',
        'arquivo': 'exemplos/deriva/src/partida.cpp',
        'linha': 24,
        'quebrado_de_proposito': False,
        'codigo': """\
// Chaves, e não parênteses. `std::istringstream is(std::string(texto));`
// é a *most vexing parse*: o compilador lê isso como a DECLARAÇÃO de uma
// função chamada `is` que devolve `istringstream` e recebe um `std::string`,
// e depois reclama que não há `operator>>` para função. A inicialização
// uniforme com `{}` da Aula 03 não tem essa ambiguidade, e é por isso que o
// material a recomenda desde o começo.
std::istringstream is{std::string(texto)};
std::string chave;
partida p;
bool tem_cabeca = false;""",
    },
    'dip-apresentacao': {
        'aula': 24,
        'lang': 'cpp',
        'legenda': 'include/deriva/apresentacao.hpp · DIP, a interface do render',
        'nota': 'O núcleo depende desta abstração, e não de terminal nem de Qt. Antes da refatoração o `mundo` escrevia direto em `std::cout`, e trocar a saída significava editá-lo.',
        'arquivo': 'exemplos/deriva/include/deriva/apresentacao.hpp',
        'linha': 18,
        'quebrado_de_proposito': False,
        'codigo': """\
// ===========================================================================
// DIP · a interface de apresentação
//
// O núcleo depende DESTA abstração, e não de terminal nem de Qt. É o que
// torna a separação demonstrável em vez de afirmada: a v2.7 acrescenta uma
// segunda implementação e o núcleo não muda uma linha.
//
// Antes da refatoração, o `mundo` escrevia direto em `std::cout` - e trocar a
// saída significava editar o `mundo`. A variante `v2.6-antes` preserva essa
// forma para comparação.
// ===========================================================================
class i_apresentacao {
 public:
  virtual ~i_apresentacao() = default;
  virtual void desenhar(const mundo& m) = 0;
  virtual void mensagem(std::string_view texto) = 0;
};""",
    },
    'god-class': {
        'aula': 24,
        'lang': 'cpp',
        'legenda': 'v2.6-antes · sete responsabilidades · CAÇA AO BUG 3',
        'nota': 'Compila sem aviso, roda, e faz tudo o que a refatorada faz. O defeito não é funcional: são sete motivos independentes para editar o mesmo arquivo. A caça não é achar o erro, é refatorar e provar pelo replay que a saída não mudou.',
        'arquivo': 'exemplos/deriva/variantes/v2.6-antes/mundo_god_class.cpp',
        'linha': 44,
        'quebrado_de_proposito': True,
        'codigo': """\
/// AS SETE RESPONSABILIDADES. Cada uma é um motivo independente para editar
/// este arquivo, e é essa contagem - não o número de linhas - que a Aula 24
/// pede para medir.
class mundo {
 public:
  mundo(int largura, int altura) : largura_(largura), altura_(altura) {
    terreno_.assign(static_cast<std::size_t>(largura * altura), '.');
    for (int x = 0; x < largura; ++x) {
      terreno_[idx({x, 0})] = '#';
      terreno_[idx({x, altura - 1})] = '#';
    }
    for (int y = 0; y < altura; ++y) {
      terreno_[idx({0, y})] = '#';
      terreno_[idx({largura - 1, y})] = '#';
    }
  }

  // (1) estado do domínio
  void acrescentar(std::unique_ptr<entidade> e) { entidades_.push_back(std::move(e)); }
  bool livre(vetor2 p) const {
    return p.x >= 0 && p.y >= 0 && p.x < largura_ && p.y < altura_ &&
           terreno_[idx(p)] != '#';
  }

  // (2) RENDER. Escreve direto em `std::cout`, e é isso que torna a troca por
  // Qt impossível sem editar esta classe. Também impede testar sem capturar a
  // saída do processo.
  void desenhar() const {
    for (int y = 0; y < altura_; ++y) {
      for (int x = 0; x < largura_; ++x) {
        char c = terreno_[idx({x, y})];
        for (const auto& e : entidades_) {
          if (e->pos == vetor2{x, y}) c = e->glifo();
        }
        std::cout << c;
      }
      std::cout << '\\n';
    }
  }

  // (3) ENTRADA. O `switch` de comandos mora aqui, e por isso não há onde
  // guardar o desfazer.
  bool comando(const std::string& c) {
    sonda* s = nullptr;
    for (const auto& e : entidades_) {
      if (auto* p = dynamic_cast<sonda*>(e.get())) s = p;
    }
    if (!s) return false;
    vetor2 alvo = s->pos;
    if (c == "norte") alvo.y -= 1;
    else if (c == "sul") alvo.y += 1;
    else if (c == "leste") alvo.x += 1;
    else if (c == "oeste") alvo.x -= 1;
    else if (c == "esperar") { /* nada */ }
    else return false;
    if (!livre(alvo)) { registrar("bloqueado"); return false; }
    s->pos = alvo;
    registrar("moveu");
    return true;
  }

  // (4) IA. O comportamento de cada tipo está codificado aqui, com
  // `dynamic_cast`, em vez de na entidade ou numa estratégia.
  void turno() {
    for (const auto& e : entidades_) {
      if (auto* d = dynamic_cast<drone*>(e.get())) {
        vetor2 alvo{d->pos.x + d->rumo.x, d->pos.y + d->rumo.y};
        if (livre(alvo)) d->pos = alvo;
        else d->rumo = {-d->rumo.x, -d->rumo.y};
      }
    }
  }

  // (5) LOG. Abre o arquivo aqui dentro, então o teste que quiser verificar o
  // log precisa mexer no sistema de arquivos.
  void registrar(const std::string& evento) {
    std::ofstream log("deriva.log", std::ios::app);
    log << evento << '\\n';
  }

  // (6) PERSISTÊNCIA. O formato do save também mora aqui.
  std::string salvar() const {
    std::string s = "antes 1\\n";
    for (const auto& e : entidades_) {
      s += e->glifo();
      s += " " + std::to_string(e->pos.x) + " " + std::to_string(e->pos.y) + "\\n";
    }
    return s;
  }

  // (7) CRIAÇÃO. A tabela de glifos, uma terceira vez com `dynamic_cast`.
  void povoar(const std::string& glifos) {
    int x = 1, y = 1;
    for (const char g : glifos) {
      if (g == '@') { auto s = std::make_unique<sonda>(); s->pos = {x, y}; acrescentar(std::move(s)); }
      else if (g == 'd') { auto d = std::make_unique<drone>(); d->pos = {x, y}; acrescentar(std::move(d)); }
      if (++x >= largura_ - 1) { x = 1; ++y; }
    }
  }

 private:
  std::size_t idx(vetor2 p) const {
    return static_cast<std::size_t>(p.y) * static_cast<std::size_t>(largura_) +
           static_cast<std::size_t>(p.x);
  }
  int largura_, altura_;
  std::vector<char> terreno_;
  std::vector<std::unique_ptr<entidade>> entidades_;
};""",
    },
    'ocp-turno-nao-conhece': {
        'aula': 24,
        'lang': 'cpp',
        'legenda': 'src/mundo.cpp · o turno não conhece as derivadas',
        'nota': 'Aberto para extensão e fechado para modificação, e a prova é negativa: acrescentar uma entidade nova não muda uma linha deste arquivo, porque o `mundo` guarda `vector<unique_ptr<entidade>>` e chama `agir` pela base. O índice em lugar do iterador não é estilo: `agir` pode acrescentar entidade, e isso invalidaria o iterador.',
        'arquivo': 'exemplos/deriva/src/mundo.cpp',
        'linha': 19,
        'quebrado_de_proposito': False,
        'codigo': """\
void mundo::turno() {
  // Índice em lugar de iterador: `agir` pode acrescentar entidade, e isso
  // invalidaria o iterador. Quem entra durante o turno age no turno seguinte,
  // e essa regra é observável no replay.
  const std::size_t n = entidades_.size();
  for (std::size_t i = 0; i < n; ++i) entidades_[i]->agir(*this);
}""",
    },
    'desfazer-prova-invariancia': {
        'aula': 24,
        'lang': 'cpp',
        'legenda': 'testes/test_padroes.cpp · o despejo byte a byte como oráculo',
        'nota': 'O mesmo critério que a caça ao bug 3 cobra: `diff` vazio é a única evidência aceita, e teste verde não basta - os testes passam nas duas versões.',
        'arquivo': 'exemplos/deriva/testes/test_padroes.cpp',
        'linha': 63,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("desfazer em cadeia volta ao estado inicial") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  historico h;
  const std::string antes = w.despejar();

  // A coluna em (3,2) e parede: a sequencia desce ANTES de chegar nela.
  REQUIRE(h.aplicar(std::make_unique<mover_sonda>(vetor2{1, 0}), w));   // (2,1)
  REQUIRE(h.aplicar(std::make_unique<mover_sonda>(vetor2{0, 1}), w));   // (2,2)
  REQUIRE(h.aplicar(std::make_unique<mover_sonda>(vetor2{0, 1}), w));   // (2,3)
  REQUIRE(h.profundidade() == 3);
  REQUIRE(w.despejar() != antes);

  while (h.desfazer_ultimo(w)) {
  }""",
    },
    'strategy-por-lambda': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'src/apresentacao.cpp · Strategy é função, não hierarquia',
        'nota': 'Uma operação e nenhum estado: é função, e `std::function` a guarda. A captura é por valor, e é obrigatório - a lambda sobrevive à chamada que a criou, e capturar por referência deixaria referência pendurada. É a armadilha do `string_view` da Aula 03 noutra roupa.',
        'arquivo': 'exemplos/deriva/src/apresentacao.cpp',
        'linha': 69,
        'quebrado_de_proposito': False,
        'codigo': """\
estrategia estrategia_de_patrulha(vetor2 rumo) {
  // A captura é por VALOR, e é obrigatório que seja: a lambda sobrevive à
  // chamada que a criou, e capturar `rumo` por referência deixaria uma
  // referência pendurada. É a mesma armadilha do `string_view` da Aula 03,
  // noutra roupa.
  return [rumo](const entidade& e, const mundo& m) {
    const vetor2 alvo = e.pos() + rumo;
    return m.livre(alvo) ? alvo : e.pos();
  };
}""",
    },
    'command-com-desfazer': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'include/deriva/apresentacao.hpp · Command guarda de onde saiu',
        'nota': 'O que se ganha não é elegância, é o desfazer - e um `switch` não tem onde guardar de onde a sonda veio.',
        'arquivo': 'exemplos/deriva/include/deriva/apresentacao.hpp',
        'linha': 64,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Mover a sonda. Guarda de onde saiu, e é por isso que sabe voltar.
class mover_sonda final : public i_comando {
 public:
  explicit mover_sonda(vetor2 delta) noexcept : delta_(delta) {}

  [[nodiscard]] bool executar(mundo& m) override;
  void desfazer(mundo& m) override;
  [[nodiscard]] std::string_view nome() const override { return "mover"; }

 private:
  vetor2 delta_;
  vetor2 de_onde_{};
  bool executou_ = false;
};""",
    },
    'factory-por-glifo': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'src/apresentacao.cpp · Factory, e a tabela num lugar só',
        'nota': 'Acrescentar entidade nova é acrescentar um caso aqui, e nada no carregador de mapa muda. Na variante `v2.6-antes` a mesma tabela aparece três vezes, com `dynamic_cast`.',
        'arquivo': 'exemplos/deriva/src/apresentacao.cpp',
        'linha': 58,
        'quebrado_de_proposito': False,
        'codigo': """\
std::unique_ptr<entidade> criar_por_glifo(char glifo, vetor2 pos) {
  // A tabela é aqui, e só aqui. Acrescentar uma entidade nova é acrescentar um
  // caso - e nada no carregador de mapa muda.
  switch (glifo) {
    case '@': return std::make_unique<sonda>(pos);
    case 'd': return std::make_unique<drone>(pos);
    case '!': return std::make_unique<item>(pos, "sucata", 3);
    default: return nullptr;   // glifo que não é entidade: o terreno cuida
  }""",
    },
    'composite-mochila': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'src/inventario.cpp · Composite, e o inventário não sabe a diferença',
        'nota': 'A mochila responde `massa` somando o que tem dentro, e o inventário a trata como qualquer peça. Cuidado com o ciclo: mochila dentro de si mesma é o vazamento da Aula 13 noutra forma.',
        'arquivo': 'exemplos/deriva/src/inventario.cpp',
        'linha': 90,
        'quebrado_de_proposito': False,
        'codigo': """\
int mochila::massa() const {
  return std::accumulate(dentro_.begin(), dentro_.end(), tara_,
                         [](int soma, const std::unique_ptr<componente>& c) {
                           return soma + c->massa();
                         });
}""",
    },
    'posse-no-qt': {
        'aula': 26,
        'lang': 'cpp',
        'legenda': 'qt/janela.hpp · posse no Qt é a exceção declarada',
        'nota': '`QObject` tem árvore de pais, e o pai destrói os filhos: passar um `QWidget*` cru ao construtor do filho ENTREGA a posse. `unique_ptr` sobre `QWidget` com pai é dupla liberação. É a exceção à regra da Aula 12, e ela é declarada, não escondida.',
        'arquivo': 'exemplos/deriva/qt/janela.hpp',
        'linha': 44,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A janela.
///
/// **Posse no Qt é diferente.** `QObject` tem árvore de pais, e o pai destrói
/// os filhos. Passar um `QWidget*` cru para o construtor do filho ENTREGA a
/// posse ao pai - e por isso `unique_ptr` sobre `QWidget` com pai é erro de
/// dupla liberação. É a exceção à regra da Aula 12, e ela é declarada e não
/// escondida.
///
/// O `Q_OBJECT` exige o MOC, um pré-processador que gera código a partir do
/// cabeçalho. É por isso que `CMAKE_AUTOMOC` existe, e é o que faz esta classe
/// precisar de um sistema de build que o Qt entenda.
class janela : public QMainWindow {
  Q_OBJECT

 public:
  explicit janela(mundo w, QWidget* pai = nullptr);
  ~janela() override;

 private slots:
  /// Um slot é um método comum que o MOC registra para poder ser chamado por
  /// nome, sem que quem chama conheça o tipo. É a versão do Qt para Observer,
  /// e o compilador não verifica a assinatura - o erro aparece em execução, na
  /// forma de uma conexão que não acontece.
  void ao_mover_norte();
  void ao_mover_sul();
  void ao_desfazer();

 private:
  void redesenhar();

  mundo mundo_;                          // o núcleo, intacto
  historico historico_;                  // Command, da v2.6
  std::unique_ptr<tela_qt> tela_;
  QPlainTextEdit* visor_ = nullptr;      // filho: o Qt é o dono
};""",
    },
    'nucleo-nao-muda': {
        'aula': 26,
        'lang': 'cpp',
        'legenda': 'qt/main_qt.cpp · o argumento inteiro da aula',
        'nota': 'Nenhuma linha do núcleo mudou para esta janela existir, e isso só é verdade porque a v2.6 extraiu `i_apresentacao`. É a diferença entre separação demonstrada e separação afirmada.',
        'arquivo': 'exemplos/deriva/qt/main_qt.cpp',
        'linha': 10,
        'quebrado_de_proposito': False,
        'codigo': """\
int main(int argc, char** argv) {
  QApplication app(argc, argv);

  auto m = deriva::mapa::carregar("mapas/estacao-01.txt");
  if (!m) return 2;
  deriva::mundo w(std::move(*m));
  w.acrescentar(std::make_unique<deriva::sonda>(w.setor().entrada()));

  // Nenhuma linha do núcleo mudou para isto existir. É o argumento inteiro da
  // Aula 26, e ele só é verdade porque a v2.6 extraiu `i_apresentacao`.
  deriva::qt::janela janela(std::move(w));
  janela.resize(900, 600);
  janela.setWindowTitle("Deriva - segundo front-end");
  janela.show();
  return app.exec();
}""",
    },
    'sorteio-deterministico': {
        'aula': 16,
        'lang': 'cpp',
        'legenda': 'src/main.cpp · o sorteio que não sorteia',
        'nota': 'Não é `std::mt19937` nem `std::random_device`: precisa ser reproduzível byte a byte em qualquer máquina, porque é sobre isso que o replay se apoia. Aleatoriedade de verdade seria pior aqui.',
        'arquivo': 'exemplos/deriva/src/main.cpp',
        'linha': 31,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Gerador congruente linear, com constantes de Numerical Recipes.
///
/// Não é `std::mt19937` nem, muito menos, `std::random_device`: precisa ser
/// reproduzível byte a byte em qualquer máquina, porque é sobre isso que o
/// replay da Aula 16 se apoia. Aleatoriedade de verdade seria pior aqui.
class sorteio {
 public:
  explicit sorteio(unsigned semente) noexcept : estado_(semente) {}

  [[nodiscard]] unsigned proximo() noexcept {
    estado_ = estado_ * 1664525u + 1013904223u;
    return estado_;
  }
  [[nodiscard]] int ate(int limite) noexcept {
    return limite <= 0 ? 0 : static_cast<int>(proximo() % static_cast<unsigned>(limite));
  }

 private:
  unsigned estado_;
};""",
    },
    'portao-replay': {
        'aula': 16,
        'lang': 'make',
        'legenda': 'Makefile · o portão de replay',
        'nota': 'Semente fixa, roteiro gravado, `diff` contra o esperado. Regravar o esperado é uma DECISÃO - numa refatoração, é justamente o que não se pode fazer.',
        'arquivo': 'exemplos/deriva/Makefile',
        'linha': 39,
        'quebrado_de_proposito': False,
        'codigo': """\
# (3) replay: despejo idêntico byte a byte. É o oráculo das Aulas 16, 24 e 25.
replay:
	@./$(BUILD)/deriva --replay roteiro.txt --semente $(SEMENTE) > $(BUILD)/replay.out
	@diff -u esperado.txt $(BUILD)/replay.out > $(BUILD)/replay.diff || \\
	  { cat $(BUILD)/replay.diff; echo "verifica: FALHA (3/4 replay) - a saida mudou"; exit 1; }
	@echo "  (3/4) replay      OK  identico byte a byte (semente $(SEMENTE))"
""",
    },
    'oo-fecha-seis': {
        'aula': 1,
        'lang': 'cpp',
        'legenda': 'testes/test_comparativo.cpp · sete contra uma',
        'nota': 'As seis maneiras de errar que somem não somem por disciplina de quem escreve: somem porque o compilador passou a impedi-las.',
        'arquivo': 'exemplos/deriva/testes/test_comparativo.cpp',
        'linha': 13,
        'quebrado_de_proposito': False,
        'codigo': """\
// A metrica da Aula 01 nao e elegancia: e quantas maneiras de errar o desenho
// permite. Sete contra uma, e as seis que somem nao somem por disciplina do
// programador - somem porque o compilador passou a impedi-las.
TEST_CASE("a versao OO fecha seis das sete maneiras de errar") {
  REQUIRE(maneiras_de_errar_em_c() == 7);
  REQUIRE(maneiras_de_errar_em_cpp() == 1);
}""",
    },
    'invariante-em-compilacao': {
        'aula': 1,
        'lang': 'cpp',
        'legenda': 'testes/test_comparativo.cpp · o campo público virou invariante',
        'nota': 'Em C, `largura` é pública e mexer nela corrompe a indexação. Aqui a garantia é de compilação, e não de lembrança.',
        'arquivo': 'exemplos/deriva/testes/test_comparativo.cpp',
        'linha': 55,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("em C++, a dimensao e invariante, e o tipo diz isso") {
  const grade g(4, 3);
  REQUIRE(g.largura() == 4);
  // `g.largura() = 2;` nao compila: o retorno e por valor, e nao ha setter.
  static_assert(!std::is_assignable_v<decltype(g.largura()), int>);
  SUCCEED("a invariante e garantida em compilacao, nao por lembranca");""",
    },
    'cmake-do-deriva': {
        'aula': 2,
        'lang': 'cmake',
        'legenda': 'CMakeLists.txt · o topo, com as quatro opções',
        'nota': '`CXX_EXTENSIONS OFF` é o que recusa `-std=gnu++17`: código que só compila com extensão não é C++17. E `DERIVA_SANITIZERS` nasce desligada, porque o laboratório não os tem.',
        'arquivo': 'exemplos/deriva/CMakeLists.txt',
        'linha': 2,
        'quebrado_de_proposito': False,
        'codigo': """\
cmake_minimum_required(VERSION 3.16)
project(deriva LANGUAGES CXX VERSION 0.3.0)

# C++17 é o teto e o foco da disciplina. `CXX_EXTENSIONS OFF` desliga as
# extensões GNU: código que só compila com -std=gnu++17 não é C++17.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Debug CACHE STRING "" FORCE)
endif()

option(DERIVA_SANITIZERS "Compilar com ASan e UBSan" OFF)
option(DERIVA_TESTES     "Compilar os testes (baixa o Catch2)" ON)
option(DERIVA_COM_FTXUI  "Camada de terminal com FTXUI v5.0.0" OFF)
option(DERIVA_COM_QT     "Segundo front-end em Qt6 (Aula 26)" OFF)""",
    },
    'lista-de-init-cpp': {
        'aula': 7,
        'lang': 'cpp',
        'legenda': 'src/grade.cpp · a lista que constrói uma vez só',
        'nota': '`celulas_` é construído com o tamanho certo de uma vez. Atribuir no corpo o construiria vazio antes e o redimensionaria depois.',
        'arquivo': 'exemplos/deriva/src/grade.cpp',
        'linha': 32,
        'quebrado_de_proposito': False,
        'codigo': """\
// `celulas_` é construído UMA vez, com o tamanho certo. Atribuir no corpo o
// construiria vazio antes e o redimensionaria depois.
grade::grade(int largura, int altura)
    : largura_(exigir_positivo(largura, "largura")),
      altura_(exigir_positivo(altura, "altura")),
      celulas_(static_cast<std::size_t>(largura_) * static_cast<std::size_t>(altura_)) {}""",
    },
    'this-em-uso': {
        'aula': 7,
        'lang': 'cpp',
        'legenda': 'src/mapa.cpp · os dois usos de `this` que o Deriva tem',
        'nota': '`this != &o` para recusar a autoatribuição, e `return *this` para encadear. São os dois únicos lugares em que `this` aparece explícito em todo o projeto - fora deles, ele é implícito e escrevê-lo é ruído.',
        'arquivo': 'exemplos/deriva/src/mapa.cpp',
        'linha': 31,
        'quebrado_de_proposito': False,
        'codigo': """\
mapa& mapa::operator=(const mapa& o) {
  if (this != &o) {
    nome_ = o.nome_;
    grade_ = o.grade_;
    entrada_ = o.entrada_;
    marca_ = o.marca_;
  }
  return *this;  // o contador não muda: nenhum objeto nasceu nem morreu""",
    },
    'par-em-declarado': {
        'aula': 7,
        'lang': 'cpp',
        'legenda': 'include/deriva/grade.hpp · o par de sobrecargas',
        'nota': '`[[nodiscard]]` nas duas, e `const` só na primeira: é a versão não-const que existe para deixar escrever, e é por isso que ela não pode ser const.',
        'arquivo': 'exemplos/deriva/include/deriva/grade.hpp',
        'linha': 33,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Sem verificação de limite: quem chama já perguntou `dentro()`.
/// O `operator[]` de `mapa` chega na v1.5 (Aula 15).
[[nodiscard]] const celula& em(vetor2 p) const;
[[nodiscard]] celula& em(vetor2 p);""",
    },
    'objeto-const': {
        'aula': 7,
        'lang': 'cpp',
        'legenda': 'testes/test_grade.cpp · o objeto const, e o que ele alcança',
        'nota': '`const grade g(20, 10)` só deixa chamar método `const`, e todas as chamadas aqui o são. Trocar uma delas pela sobrecarga não-const de `em()` faz este teste deixar de compilar - e é essa recusa, e não a palavra no cabeçalho, que é a garantia.',
        'arquivo': 'exemplos/deriva/testes/test_grade.cpp',
        'linha': 11,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("grade conhece seus limites") {
  const grade g(20, 10);
  REQUIRE(g.largura() == 20);
  REQUIRE(g.altura() == 10);
  REQUIRE(g.dentro({0, 0}));
  REQUIRE(g.dentro({19, 9}));
  REQUIRE_FALSE(g.dentro({20, 9}));
  REQUIRE_FALSE(g.dentro({-1, 0}));
}""",
    },
    'contador-em-uso': {
        'aula': 7,
        'lang': 'cpp',
        'legenda': 'src/mapa.cpp · o contador em uso',
        'nota': '`++vivos` e `++criados` no construtor, `--vivos` no destrutor. A declaração `inline static` está no cabeçalho, e é ela que dispensa a definição num .cpp.',
        'arquivo': 'exemplos/deriva/src/mapa.cpp',
        'linha': 10,
        'quebrado_de_proposito': False,
        'codigo': """\
mapa::mapa(std::string nome, int largura, int altura)
    : nome_(std::move(nome)),
      grade_(largura, altura),
      marca_("mapa:" + nome_) {
  ++contador_mapa::vivos;
  ++contador_mapa::criados;
}

mapa::~mapa() { --contador_mapa::vivos; }""",
    },
    'ordem-simples': {
        'aula': 8,
        'lang': 'cpp',
        'legenda': 'testes/test_ciclo_de_vida.cpp · a ordem, afirmada linha por linha',
        'nota': 'Dois objetos no escopo externo, um no interno, e a saída comparada texto a texto. Nenhuma linha de código pediu essa ordem.',
        'arquivo': 'exemplos/deriva/testes/test_ciclo_de_vida.cpp',
        'linha': 19,
        'quebrado_de_proposito': False,
        'codigo': """\
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
          "+a\\n"
          "+b\\n"
          "+c\\n"
          "-c\\n"   // o escopo interno fecha primeiro
          "-b\\n"   // e o externo desmonta na ordem inversa
          "-a\\n");""",
    },
    'forma-longa-copia': {
        'aula': 9,
        'lang': 'cpp',
        'legenda': 'src/mapa.cpp · a forma longa da regra do três',
        'nota': 'O incremento na cópia é obrigatório: sem ele o destrutor da cópia decrementaria algo que ninguém incrementou, e `vivos` fecharia negativo - o contador passaria a mentir na direção que ninguém desconfia.',
        'arquivo': 'exemplos/deriva/src/mapa.cpp',
        'linha': 20,
        'quebrado_de_proposito': False,
        'codigo': """\
// Destrutor declarado → a cópia precisa ser declarada também: é a regra do
// três (Aula 09). Aqui ela é rasa de propósito? Não: `grade_` é um vector, e
// copiá-lo copia as células. O que a cópia manual acrescenta é só o
// incremento do contador - sem ele, `vivos` fecharia negativo, porque o
// destrutor da cópia decrementaria algo que ninguém incrementou.
mapa::mapa(const mapa& o)
    : nome_(o.nome_), grade_(o.grade_), entrada_(o.entrada_), marca_(o.marca_) {
  ++contador_mapa::vivos;
  ++contador_mapa::criados;
}""",
    },
    'forma-curta-delete': {
        'aula': 9,
        'lang': 'cpp',
        'legenda': 'include/deriva/terminal_bruto.hpp · a forma curta',
        'nota': 'Duas linhas de `= delete`, e a regra do três está cumprida. Há exatamente um terminal, e posse de recurso único não se duplica.',
        'arquivo': 'exemplos/deriva/include/deriva/terminal_bruto.hpp',
        'linha': 9,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Põe o terminal em modo bruto no construtor e o restaura no destrutor.
///
/// É a melhor demonstração de RAII que existe, e não é metáfora: se o
/// destrutor não rodar, o terminal do estudante fica sem eco e sem Enter
/// **depois** que o programa sai. Ele descobre RAII digitando `reset` às
/// cegas.
///
/// A variante `variantes/v0.2-quebrada/` omite o destrutor de propósito.
///
/// Não é copiável nem movível: há exatamente um terminal, e posse de recurso
/// único não se duplica. Declarar as duas apagadas é a **regra do três**
/// (Aula 09) na sua forma mais curta.
class terminal_bruto {
 public:
  terminal_bruto();
  ~terminal_bruto();

  terminal_bruto(const terminal_bruto&) = delete;
  terminal_bruto& operator=(const terminal_bruto&) = delete;

  /// Verdadeiro quando havia um terminal de verdade para alterar. Em teste,
  /// em pipe ou em CI a saída não é tty: o objeto se constrói, conta como
  /// vivo, e não mexe em nada. Sem isso, `ctest` deixaria o terminal de quem
  /// roda os testes em estado imprevisível.
  [[nodiscard]] bool ativo() const noexcept { return ativo_; }

 private:
  bool ativo_ = false;
};""",
    },
    'despacho-em-tres': {
        'aula': 11,
        'lang': 'cpp',
        'legenda': 'testes/test_entidade.cpp · três objetos, um tipo de ponteiro',
        'nota': 'A saída é `@d!`, e não `eee`. Os três ponteiros são `entidade*`, e quem decidiu foi o objeto.',
        'arquivo': 'exemplos/deriva/testes/test_entidade.cpp',
        'linha': 21,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("o despacho virtual escolhe pelo tipo do OBJETO") {
  zerar_entidades();
  const sonda s({1, 1});
  const drone d({2, 2});
  const item i({3, 3}, "celula-de-energia", 5);

  const entidade* por_base[] = {&s, &d, &i};
  std::string glifos;
  for (const entidade* e : por_base) glifos.push_back(e->glifo());

  REQUIRE(glifos == "@d!");   // e nao "eee": o ponteiro e entidade* nos tres
}""",
    },
    'override-e-final': {
        'aula': 11,
        'lang': 'cpp',
        'legenda': 'include/deriva/entidade.hpp · `final` na folha, `override` nas sobrescritas',
        'nota': '`virtual` não se repete na derivada: `override` já diz que sobrescreve, e diz melhor, porque o compilador o verifica.',
        'arquivo': 'exemplos/deriva/include/deriva/entidade.hpp',
        'linha': 95,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Drone de patrulha. Anda sozinho, em linha, e inverte ao bater.
class drone final : public entidade {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  explicit drone(vetor2 pos, vetor2 rumo = {1, 0}) noexcept
      : entidade(pos), rumo_(rumo) {
    ++vivos;
    ++criados;
  }
  ~drone() override { --vivos; }

  [[nodiscard]] char glifo() const override { return 'd'; }
  [[nodiscard]] std::string_view nome() const override { return "drone"; }
  void agir(mundo& m) override;

  [[nodiscard]] vetor2 rumo() const noexcept { return rumo_; }

 private:
  vetor2 rumo_;
};""",
    },
    'abstrata-afirmada': {
        'aula': 11,
        'lang': 'cpp',
        'legenda': 'testes/test_entidade.cpp · a abstração, afirmada',
        'nota': '`is_abstract_v`, `!is_constructible_v`, `has_virtual_destructor_v` e `!is_copy_constructible_v`. Quatro decisões de projeto que o compilador guarda.',
        'arquivo': 'exemplos/deriva/testes/test_entidade.cpp',
        'linha': 12,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("entidade e abstrata, e o compilador diz isso") {
  static_assert(std::is_abstract_v<entidade>);
  static_assert(!std::is_constructible_v<entidade, vetor2>);
  static_assert(std::has_virtual_destructor_v<entidade>);
  static_assert(!std::is_copy_constructible_v<entidade>,
                "base polimorfica nao se copia por valor: fatiaria o objeto");
  SUCCEED("verificado em tempo de compilacao");
}""",
    },
    'dois-donos': {
        'aula': 13,
        'lang': 'cpp',
        'legenda': 'testes/test_estacao.cpp · o requisito que shared_ptr atende',
        'nota': 'A contagem vai a 1, sobe a 3 e volta a 1 no mesmo escopo. É o requisito que `unique_ptr` não atende: a eclusa pertence aos dois corredores, e nenhum dos dois pode destruí-la sozinho.',
        'arquivo': 'exemplos/deriva/testes/test_estacao.cpp',
        'linha': 10,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("posse compartilhada: dois donos, e nenhum destroi sozinho") {
  zerar_estacao();
  {
    auto eclusa = std::make_shared<no_estacao>("eclusa");
    REQUIRE(eclusa.use_count() == 1);
    {
      auto corredor_a = std::make_shared<no_estacao>("corredor-a");
      auto corredor_b = std::make_shared<no_estacao>("corredor-b");
      no_estacao::ligar(corredor_a, eclusa);
      no_estacao::ligar(corredor_b, eclusa);
      REQUIRE(eclusa.use_count() == 3);   // este escopo mais os dois corredores
      REQUIRE(no_estacao::vivos == 3);
    }""",
    },
    'nrvo': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'src/mapa.cpp · variável nomeada devolvida',
        'nota': 'É o caso do NRVO: o compilador pode construir `m` diretamente no lugar do retorno e não copiar nem mover. Ele **pode**, e não é obrigado - a elisão obrigatória de C++17 vale para prvalue, que este não é.',
        'arquivo': 'exemplos/deriva/src/mapa.cpp',
        'linha': 88,
        'quebrado_de_proposito': False,
        'codigo': """\
mapa m(std::move(nome), static_cast<int>(largura),
       static_cast<int>(fileiras.size()));

// Ligação estruturada sobre índice e conteúdo seria mais elegante com
// `enumerate`, que é C++23. Aqui, um laço com índice explícito.
for (int y = 0; y < static_cast<int>(fileiras.size()); ++y) {
  for (int x = 0; x < static_cast<int>(largura); ++x) {
    const char c = fileiras[static_cast<std::size_t>(y)][static_cast<std::size_t>(x)];
    celula& cel = m.grade_.em({x, y});
    cel.glifo = c;
    switch (c) {
      case '#': cel.massa = 1000; break;             // parede: não se move
      case '!': cel.massa = 3; cel.energia = 1; break;
      case '@': m.entrada_ = {x, y}; cel.glifo = '.'; break;
      default: break;
    }
  }
}
return m;""",
    },
    'parametro-por-valor': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'src/mundo.cpp · por valor, e depois `std::move`',
        'nota': 'Parâmetro por valor num tipo só-movível é o idioma: quem chama decide se move ou constrói no lugar, e a função move para dentro do vetor sem cópia nenhuma.',
        'arquivo': 'exemplos/deriva/src/mundo.cpp',
        'linha': 10,
        'quebrado_de_proposito': False,
        'codigo': """\
entidade& mundo::acrescentar(std::unique_ptr<entidade> e) {
  entidades_.push_back(std::move(e));
  return *entidades_.back();
}""",
    },
    'cinco-declaradas': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'include/deriva/mapa.hpp · as cinco, juntas',
        'nota': 'Declaradas no mesmo lugar, com a razão escrita ao lado. O comentário registra uma medição que contrariou o que ele mesmo dizia antes.',
        'arquivo': 'exemplos/deriva/include/deriva/mapa.hpp',
        'linha': 38,
        'quebrado_de_proposito': False,
        'codigo': """\
// A regra dos cinco, completa (v1.4 · Aula 14).
//
// MEDIDO, e o resultado contraria o que este comentário dizia antes. Com o
// construtor de movimento, `de_texto` custa **duas** construções; sem ele,
// custa **duas** também. O movimento não mudou número nenhum que o contador
// relate, porque o contador conta OBJETOS - e dois objetos nascem nos dois
// casos: o local e o que vai para dentro do `std::optional`.
//
// O que o movimento mudou é o CUSTO da segunda construção: com ele, o
// ponteiro de heap da grade troca de dono; sem ele, as células são copiadas
// uma a uma. `testes/test_mapa.cpp` mede a diferença por identidade de
// endereço, que é o único jeito de vê-la - e é essa a lição da Aula 14: o
// instrumento da Aula 07 não distingue cópia de movimento, e saber o que ele
// não vê vale tanto quanto saber usá-lo.
//
// `noexcept` não é decoração: `std::vector<mapa>` só usa o movimento ao
// realocar se ele for `noexcept`.
~mapa();
mapa(const mapa& o);
mapa& operator=(const mapa& o);
mapa(mapa&& o) noexcept;
mapa& operator=(mapa&& o) noexcept;""",
    },
    'move-assign': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'src/mapa.cpp · a atribuição de movimento',
        'nota': 'Ela não toca no contador, e o construtor toca: atribuir não cria nem destrói ninguém. É a assimetria que mais confunde na regra dos cinco.',
        'arquivo': 'exemplos/deriva/src/mapa.cpp',
        'linha': 56,
        'quebrado_de_proposito': False,
        'codigo': """\
mapa& mapa::operator=(mapa&& o) noexcept {
  if (this != &o) {
    nome_ = std::move(o.nome_);
    grade_ = std::move(o.grade_);
    entrada_ = o.entrada_;
    marca_ = std::move(o.marca_);
  }""",
    },
    'operadores-simetricos': {
        'aula': 15,
        'lang': 'cpp',
        'legenda': 'testes/test_operadores.cpp · simetria, medida',
        'nota': '`3 * v` e `v * 3` funcionam os dois, e é isso que função livre compra. Membro aceitaria só um dos lados.',
        'arquivo': 'exemplos/deriva/testes/test_operadores.cpp',
        'linha': 12,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("os operadores de vetor2 sao simetricos e constexpr") {
  REQUIRE(vetor2{1, 2} + vetor2{3, 4} == vetor2{4, 6});
  REQUIRE(vetor2{5, 5} - vetor2{1, 2} == vetor2{4, 3});
  REQUIRE(vetor2{2, 3} * 3 == vetor2{6, 9});
  REQUIRE(3 * vetor2{2, 3} == vetor2{6, 9});   // funcao livre: aceita os dois lados

  vetor2 v{1, 1};
  v += {2, 3};
  REQUIRE(v == vetor2{3, 4});
  v -= {1, 1};
  REQUIRE(v == vetor2{2, 3});
}""",
    },
    'compostos-membros': {
        'aula': 15,
        'lang': 'cpp',
        'legenda': 'include/deriva/vetor2.hpp · o composto é membro',
        'nota': 'Ele modifica o objeto da esquerda, e por isso é membro. O binário livre é escrito em termos dele, e assim a regra existe num lugar só.',
        'arquivo': 'exemplos/deriva/include/deriva/vetor2.hpp',
        'linha': 26,
        'quebrado_de_proposito': False,
        'codigo': """\
// v1.5 · Aula 15. Os compostos são MEMBROS porque modificam o objeto da
// esquerda; os binários são funções LIVRES, logo abaixo, porque tratam os
// dois lados igual. Escrever `+` em termos de `+=` é a forma que não
// duplica a regra.
constexpr vetor2& operator+=(const vetor2& o) noexcept {
  x += o.x;
  y += o.y;
  return *this;
}""",
    },
    'operator-saida': {
        'aula': 15,
        'lang': 'cpp',
        'legenda': 'src/mapa.cpp · `operator<<` é função livre',
        'nota': 'O lado esquerdo é o fluxo, e o fluxo não é nosso. Duas linhas sobre `despejar()`, devolvendo a referência para encadear.',
        'arquivo': 'exemplos/deriva/src/mapa.cpp',
        'linha': 138,
        'quebrado_de_proposito': False,
        'codigo': """\
std::ostream& operator<<(std::ostream& os, const mapa& m) {
  return os << m.despejar();
}""",
    },
    'catch2-system': {
        'aula': 16,
        'lang': 'cmake',
        'legenda': 'CMakeLists.txt · Catch2 como SYSTEM, com tag fixa',
        'nota': '`SYSTEM` para que o aviso da dependência não conte no portão, e `GIT_TAG` fixo para que a suíte não mude de comportamento sem que ninguém tenha mexido nela.',
        'arquivo': 'exemplos/deriva/CMakeLists.txt',
        'linha': 142,
        'quebrado_de_proposito': False,
        'codigo': """\
FetchContent_Declare(Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.5.2
  GIT_SHALLOW TRUE
  SYSTEM
)
FetchContent_MakeAvailable(Catch2)

enable_testing()
add_executable(testes
  testes/test_vetor2.cpp
  testes/test_celula.cpp
  testes/test_grade.cpp
  testes/test_mapa.cpp
  testes/test_ciclo_de_vida.cpp
  testes/test_leiaute.cpp
  testes/test_posse.cpp
  testes/test_string_view.cpp
  testes/test_move_string.cpp
  testes/test_corrida.cpp
  testes/test_entidade.cpp
  testes/test_mundo.cpp
  testes/test_estacao.cpp
  testes/test_operadores.cpp
  testes/test_fov.cpp
  testes/test_diamante.cpp
  testes/test_inspetor.cpp
  testes/test_generico.cpp
  testes/test_erro.cpp
  testes/test_inventario.cpp
  testes/test_partida.cpp
  testes/test_concorrencia.cpp
  testes/test_padroes.cpp
  testes/test_comparativo.cpp
  testes/test_revisao_ia.cpp
  testes/test_tipos.cpp
  testes/test_uml.cpp
  testes/test_encaminhamento.cpp
  testes/test_padroes_extra.cpp
  testes/test_solid.cpp
)
find_package(Threads REQUIRED)
target_link_libraries(testes PRIVATE deriva_nucleo deriva_revisao Catch2::Catch2WithMain Threads::Threads)
# o teste do codigo gerado inclui o cabecalho com o defeito plantado
target_compile_options(testes PRIVATE -Wall -Wextra -Wpedantic -Wno-non-virtual-dtor)

include(CTest)
include(Catch)
catch_discover_tests(testes)""",
    },
    'teste-como-especificacao': {
        'aula': 16,
        'lang': 'cpp',
        'legenda': 'testes/test_grade.cpp · o teste como especificação',
        'nota': 'Ele não procura defeito: ele diz o que a classe promete. Lido de cima a baixo, é a documentação de `grade` - e é executável.',
        'arquivo': 'exemplos/deriva/testes/test_grade.cpp',
        'linha': 11,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("grade conhece seus limites") {
  const grade g(20, 10);
  REQUIRE(g.largura() == 20);
  REQUIRE(g.altura() == 10);
  REQUIRE(g.dentro({0, 0}));
  REQUIRE(g.dentro({19, 9}));
  REQUIRE_FALSE(g.dentro({20, 9}));
  REQUIRE_FALSE(g.dentro({-1, 0}));
}

TEST_CASE("dimensao nao-positiva e erro de programacao") {
  REQUIRE_THROWS_AS(grade(0, 5), std::invalid_argument);
  REQUIRE_THROWS_AS(grade(5, -1), std::invalid_argument);""",
    },
    'fronteiras-optional': {
        'aula': 16,
        'lang': 'cpp',
        'legenda': 'testes/test_mapa.cpp · as três fronteiras',
        'nota': 'Vazio, torto e ausente: os três devolvem `optional` vazio. Ausência de resultado não é exceção, e o tipo diz isso.',
        'arquivo': 'exemplos/deriva/testes/test_mapa.cpp',
        'linha': 44,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("ausencia de resultado nao e excecao") {
  REQUIRE_FALSE(mapa::de_texto("", "vazio").has_value());
  REQUIRE_FALSE(mapa::de_texto("###\\n##\\n", "torto").has_value());
  REQUIRE_FALSE(mapa::carregar("nao/existe/em/lugar/algum.txt").has_value());
}""",
    },
    'section-refaz-arranjo': {
        'aula': 16,
        'lang': 'cpp',
        'legenda': 'testes/test_fov.cpp · `SECTION` refaz o arranjo em cada ramo',
        'nota': 'O corpo do `TEST_CASE` roda uma vez POR seção, e não uma vez para as duas: cada ramo entra num mapa recém-montado. É o que torna as seções independentes, e é a propriedade que se perde ao guardar estado entre elas.',
        'arquivo': 'exemplos/deriva/testes/test_fov.cpp',
        'linha': 45,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("a parede e vista e bloqueia o que esta atras") {
  const auto m = mapa::de_texto(kSala, "sala");
  const auto v = visiveis(*m, {1, 2}, 6);

  REQUIRE(v.count(vetor2{4, 2}) == 1);   // a coluna: vista, porque bloqueia
  REQUIRE(v.count(vetor2{5, 2}) == 0);   // logo atras dela: sombra

  SECTION("mas se ve em volta da coluna, por cima e por baixo") {
    REQUIRE(v.count(vetor2{4, 1}) == 1);
    REQUIRE(v.count(vetor2{4, 3}) == 1);
    REQUIRE(v.count(vetor2{6, 1}) == 1);   // na borda do raio, dist 6
  }
  SECTION("o raio e de Manhattan, e a borda e exata") {
    REQUIRE(vetor2{1, 2}.manhattan({6, 1}) == 6);
    REQUIRE(v.count(vetor2{6, 1}) == 1);
    REQUIRE(vetor2{1, 2}.manhattan({7, 1}) == 7);
    REQUIRE(v.count(vetor2{7, 1}) == 0);   // um passo alem, e ja nao se ve""",
    },
    'tres-formas-diamante': {
        'aula': 17,
        'lang': 'cpp',
        'legenda': 'include/deriva/diamante.hpp · as três formas, lado a lado',
        'nota': 'Duplicada, virtual e composta. Os tamanhos estão no fim do arquivo, afirmados, e contrariam a intuição.',
        'arquivo': 'exemplos/deriva/include/deriva/diamante.hpp',
        'linha': 15,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A base com estado. Um `int` e uma função virtual.
struct nucleo {
  virtual ~nucleo() = default;
  int leituras = 0;
};

/// Herança comum nos dois ramos: o `nucleo` é DUPLICADO na folha.
struct movel : nucleo { int passos = 0; };
struct sensor : nucleo { int alcance = 0; };
struct patrulha_duplicada : movel, sensor { int rota = 0; };

/// Herança virtual: existe UM `nucleo` na folha, e o compilador paga por isso
/// com um ponteiro extra por ramo virtual.
struct movel_v : virtual nucleo { int passos = 0; };
struct sensor_v : virtual nucleo { int alcance = 0; };
struct patrulha_unica : movel_v, sensor_v { int rota = 0; };

/// A saída que o material recomenda: composição no lugar do segundo ramo.
/// Nenhum diamante, nenhuma ambiguidade, nenhuma pergunta sobre qual
/// `leituras` é o certo. É também a MAIOR das três em bytes (56), e continua
/// sendo a recomendada: o que se está comprando é a ausência de uma pergunta
/// que não tem resposta boa.
struct patrulha_composta : movel { sensor_v olho; int rota = 0; };""",
    },
    'dois-campos': {
        'aula': 17,
        'lang': 'cpp',
        'legenda': 'testes/test_diamante.cpp · dois `leituras`, e nenhum é o certo',
        'nota': 'Escrever 7 por um ramo e 9 pelo outro, e ler os dois de volta. Não há resposta boa para "qual é o valor", e é esse o defeito - não o tamanho.',
        'arquivo': 'exemplos/deriva/testes/test_diamante.cpp',
        'linha': 29,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("com heranca comum, os dois ramos escrevem em campos diferentes") {
  patrulha_duplicada p;
  static_cast<movel&>(p).leituras = 7;
  static_cast<sensor&>(p).leituras = 9;
  REQUIRE(static_cast<movel&>(p).leituras == 7);
  REQUIRE(static_cast<sensor&>(p).leituras == 9);   // e este e o defeito
}""",
    },
    'um-campo-so': {
        'aula': 17,
        'lang': 'cpp',
        'legenda': 'testes/test_diamante.cpp · com base virtual, um campo',
        'nota': 'Escrever por um ramo e ler pelo outro devolve o mesmo valor. É isto que se compra com a indireção, e não bytes - a forma virtual é a maior das três.',
        'arquivo': 'exemplos/deriva/testes/test_diamante.cpp',
        'linha': 37,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("com heranca virtual, ha um campo so") {
  patrulha_unica p;
  static_cast<movel_v&>(p).leituras = 7;
  REQUIRE(static_cast<sensor_v&>(p).leituras == 7);
  static_cast<sensor_v&>(p).leituras = 9;
  REQUIRE(static_cast<movel_v&>(p).leituras == 9);
}""",
    },
    'ordem-das-bases': {
        'aula': 17,
        'lang': 'cpp',
        'legenda': 'src/reparadora.cpp · a ordem das bases é a da declaração',
        'nota': 'Bases antes de membros, e bases na ordem em que a lista de HERANÇA as declara - não na ordem em que a lista de inicialização as menciona. Trocar a ordem na lista de inicialização não muda a ordem de execução, e o `-Wreorder`, que o `-Wall` do portão já liga, avisa quando as duas divergem.',
        'arquivo': 'exemplos/deriva/src/reparadora.cpp',
        'linha': 5,
        'quebrado_de_proposito': False,
        'codigo': """\
sonda_reparadora::sonda_reparadora(vetor2 pos, int energia)
    : sonda(pos, energia) {
  // A ordem de construção é: entidade, sonda, i_reparavel, sonda_reparadora.
  // Bases antes de membros, e bases na ordem de DECLARAÇÃO da lista de
  // herança - não na ordem em que a lista de inicialização as menciona
  // (Aula 17).
  ++vivos;
  ++criados;
}""",
    },
    'reparadora-fecha-em-zero': {
        'aula': 17,
        'lang': 'cpp',
        'legenda': 'testes/test_diamante.cpp · a destruição percorre o inverso exato',
        'nota': 'Uma `sonda_reparadora` conta nos DOIS contadores, porque ela também é uma `sonda`, e os dois voltam a zero no fim do escopo. É a prova de que nenhum destrutor da cadeia deixou de rodar.',
        'arquivo': 'exemplos/deriva/testes/test_diamante.cpp',
        'linha': 77,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("a ordem de construcao e destruicao da reparadora fecha em zero") {
  zerar_entidades();
  {
    const sonda_reparadora r({1, 1});
    REQUIRE(sonda_reparadora::vivos == 1);
    REQUIRE(sonda::vivos == 1);   // ela TAMBEM e uma sonda, e conta nos dois
  }
  REQUIRE(sonda_reparadora::vivos == 0);
  REQUIRE(sonda::vivos == 0);""",
    },
    'laco-sem-tipo': {
        'aula': 18,
        'lang': 'cpp',
        'legenda': 'src/mundo.cpp · o laço que não nomeia tipo concreto',
        'nota': 'Nenhum `dynamic_cast`, nenhum `typeid`, nenhum `switch`. É o polimorfismo funcionando - e o contraste com o inspetor da mesma aula, onde perguntar o tipo é a tarefa.',
        'arquivo': 'exemplos/deriva/src/mundo.cpp',
        'linha': 19,
        'quebrado_de_proposito': False,
        'codigo': """\
void mundo::turno() {
  // Índice em lugar de iterador: `agir` pode acrescentar entidade, e isso
  // invalidaria o iterador. Quem entra durante o turno age no turno seguinte,
  // e essa regra é observável no replay.
  const std::size_t n = entidades_.size();
  for (std::size_t i = 0; i < n; ++i) entidades_[i]->agir(*this);
}""",
    },
    'render-polimorfico': {
        'aula': 18,
        'lang': 'cpp',
        'legenda': 'src/mundo.cpp · o render, também sem nome de tipo',
        'nota': 'Cada entidade desenha o próprio glifo por chamada virtual. Acrescentar uma entidade nova não toca nesta função.',
        'arquivo': 'exemplos/deriva/src/mundo.cpp',
        'linha': 46,
        'quebrado_de_proposito': False,
        'codigo': """\
std::string mundo::despejar() const {
  std::string s = setor_.despejar();
  // As entidades entram por cima do glifo do terreno, na ordem de inserção.
  const int largura = setor_.g().largura();
  const std::size_t cabeca = s.find('\\n', s.find('\\n') + 1) + 1;
  for (const std::unique_ptr<entidade>& e : entidades_) {
    const vetor2 p = e->pos();
    if (!setor_.g().dentro(p)) continue;
    const std::size_t i = cabeca +
        static_cast<std::size_t>(p.y) * static_cast<std::size_t>(largura + 1) +
        static_cast<std::size_t>(p.x);
    if (i < s.size()) s[i] = e->glifo();
  }""",
    },
    'grade-generica-classe': {
        'aula': 19,
        'lang': 'cpp',
        'legenda': 'include/deriva/grade_generica.hpp · a classe e as restrições',
        'nota': '`grade_de<T>` CONVIVE com a `grade` não genérica em vez de substituí-la: generalizar não é obrigação retroativa. E o `static_assert` na definição, não no uso, é o que faz a mensagem de erro ser a nossa.',
        'arquivo': 'exemplos/deriva/include/deriva/grade_generica.hpp',
        'linha': 27,
        'quebrado_de_proposito': False,
        'codigo': """\
class grade_de : public contador_de_instancias<grade_de<T>> {
  static_assert(std::is_default_constructible_v<T>,
                "grade_de<T> precisa saber criar celula vazia: T sem construtor "
                "padrao nao serve");
  static_assert(!std::is_reference_v<T>, "grade de referencias nao existe");""",
    },
    'grade-generica-acesso': {
        'aula': 19,
        'lang': 'cpp',
        'legenda': 'include/deriva/grade_generica.hpp · construtor e o par de acesso',
        'nota': 'A validação continua na lista de inicialização, como na versão não genérica - e o par const/não-const de `em()` é o mesmo padrão do Cap. 7, agora sobre `T`.',
        'arquivo': 'exemplos/deriva/include/deriva/grade_generica.hpp',
        'linha': 46,
        'quebrado_de_proposito': False,
        'codigo': """\
grade_de(int largura, int altura)
    : largura_(exigir_positivo(largura, "largura")),
      altura_(exigir_positivo(altura, "altura")),
      celulas_(static_cast<std::size_t>(largura_) *
               static_cast<std::size_t>(altura_)) {}

[[nodiscard]] int largura() const noexcept { return largura_; }
[[nodiscard]] int altura() const noexcept { return altura_; }
[[nodiscard]] bool dentro(vetor2 p) const noexcept {
  return p.x >= 0 && p.y >= 0 && p.x < largura_ && p.y < altura_;
}

[[nodiscard]] const T& em(vetor2 p) const { return celulas_[indice(p)]; }
[[nodiscard]] T& em(vetor2 p) { return celulas_[indice(p)]; }""",
    },
    'crtp-nao-cresce': {
        'aula': 19,
        'lang': 'cpp',
        'legenda': 'include/deriva/grade_generica.hpp · o CRTP não custa byte',
        'nota': 'Base vazia, e o compilador a otimiza. É a diferença entre polimorfismo estático e dinâmico, afirmada no `sizeof`.',
        'arquivo': 'exemplos/deriva/include/deriva/grade_generica.hpp',
        'linha': 113,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A grade de células continua sendo o caso comum, e ganha um nome curto.
using grade_de_celulas = grade_de<celula>;

/// Herdar do CRTP não custa byte nenhum: base vazia, e o compilador a
/// otimiza. É a diferença entre polimorfismo estático e dinâmico, medida.
static_assert(sizeof(grade_de<celula>) == sizeof(int) * 2 + sizeof(std::vector<celula>),
              "o contador por CRTP nao aumenta o objeto");""",
    },
    'raiz-de-erro': {
        'aula': 20,
        'lang': 'cpp',
        'legenda': 'include/deriva/erro.hpp · a raiz, e por que não std::exception',
        'nota': '`runtime_error` já guarda a mensagem e resolve o `what()`. Herdar de `std::exception` e guardar uma `std::string` membro esconde uma armadilha: se a cópia da exceção lançar durante o desenrolar, o programa termina.',
        'arquivo': 'exemplos/deriva/include/deriva/erro.hpp',
        'linha': 14,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A raiz da hierarquia de erros do Deriva.
///
/// Deriva de `std::runtime_error` e não de `std::exception` direto, porque
/// `runtime_error` já guarda a mensagem e resolve o `what()`. Herdar de
/// `std::exception` e reimplementar `what()` é trabalho sem retorno, e a
/// tentação de guardar um `std::string` membro esconde uma armadilha: se o
/// construtor de cópia da exceção lançar durante o desenrolar da pilha, o
/// programa termina.
class erro_de_deriva : public std::runtime_error {
 public:
  explicit erro_de_deriva(const std::string& msg) : std::runtime_error(msg) {}
};""",
    },
    'duas-folhas-de-erro': {
        'aula': 20,
        'lang': 'cpp',
        'legenda': 'src/erro.cpp · as duas folhas',
        'nota': 'Cada uma monta a mensagem na base e guarda o dado estruturado ao lado: quem trata precisa do caminho e do código, e não de uma string para reanalisar.',
        'arquivo': 'exemplos/deriva/src/erro.cpp',
        'linha': 9,
        'quebrado_de_proposito': False,
        'codigo': """\
mapa_invalido::mapa_invalido(std::filesystem::path caminho, std::string motivo)
    : erro_de_deriva("mapa invalido em '" + caminho.string() + "': " + motivo),
      caminho_(std::move(caminho)),
      motivo_(std::move(motivo)) {}

falha_de_leitura::falha_de_leitura(std::filesystem::path caminho, std::error_code ec)
    : erro_de_deriva("nao foi possivel ler '" + caminho.string() + "': " + ec.message()),
      caminho_(std::move(caminho)),
      ec_(ec) {}""",
    },
    'onde-ausencia-vira-erro': {
        'aula': 20,
        'lang': 'cpp',
        'legenda': 'src/erro.cpp · o ponto exato em que ausência deixa de ser optional',
        'nota': '`mapa::carregar` devolve `optional` para o mesmo arquivo ausente. A diferença não é capricho: esta função PROMETE devolver um mapa, e aquela promete responder se há um.',
        'arquivo': 'exemplos/deriva/src/erro.cpp',
        'linha': 63,
        'quebrado_de_proposito': False,
        'codigo': """\
mapa carregar_ou_lancar(const std::filesystem::path& caminho) {
  std::error_code ec;
  if (!std::filesystem::exists(caminho, ec)) {
    // Ausência tratada como erro AQUI, e como `optional` em `mapa::carregar`.
    // A diferença não é capricho: esta função promete devolver um mapa, e
    // aquela promete responder se há um.
    throw falha_de_leitura(caminho, std::make_error_code(std::errc::no_such_file_or_directory));
  }
  if (ec) throw falha_de_leitura(caminho, ec);""",
    },
    'accumulate-tipo-da-soma': {
        'aula': 21,
        'lang': 'cpp',
        'legenda': 'src/inventario.cpp · o zero que define o tipo da soma',
        'nota': 'Passar `0.0` daria soma em `double` sem ninguém pedir, e o truncamento apareceria três capítulos depois.',
        'arquivo': 'exemplos/deriva/src/inventario.cpp',
        'linha': 24,
        'quebrado_de_proposito': False,
        'codigo': """\
int inventario::massa_total() const {
  // `accumulate` com lambda: o zero inicial é `int`, e é ele que define o tipo
  // da soma. Passar `0.0` daria soma em double sem ninguém pedir.
  return std::accumulate(pecas_.begin(), pecas_.end(), 0,
                         [](int soma, const std::unique_ptr<componente>& c) {
                           return soma + c->massa();
                         });
}""",
    },
    'count-if-predicado': {
        'aula': 21,
        'lang': 'cpp',
        'legenda': 'src/inventario.cpp · o predicado vem de fora',
        'nota': 'A função serve sem saber o que se vai perguntar, e é isso que a torna útil - acrescentar um critério não a edita.',
        'arquivo': 'exemplos/deriva/src/inventario.cpp',
        'linha': 44,
        'quebrado_de_proposito': False,
        'codigo': """\
std::size_t inventario::contar_se(
    const std::function<bool(const componente&)>& criterio) const {
  return static_cast<std::size_t>(std::count_if(
      pecas_.begin(), pecas_.end(),
      [&criterio](const std::unique_ptr<componente>& c) { return criterio(*c); }));
}""",
    },
    'max-element-fim': {
        'aula': 21,
        'lang': 'cpp',
        'legenda': 'src/inventario.cpp · o iterador de fim não é elemento',
        'nota': '`max_element` devolve `end()` quando a faixa é vazia, e desreferenciar isso é comportamento indefinido. A comparação com `end()` não é cerimônia.',
        'arquivo': 'exemplos/deriva/src/inventario.cpp',
        'linha': 35,
        'quebrado_de_proposito': False,
        'codigo': """\
const componente* inventario::mais_pesada() const {
  const auto it = std::max_element(
      pecas_.begin(), pecas_.end(),
      [](const std::unique_ptr<componente>& a, const std::unique_ptr<componente>& b) {
        return a->massa() < b->massa();
      });
  return it == pecas_.end() ? nullptr : it->get();
}""",
    },
    'duas-threads-deterministico': {
        'aula': 22,
        'lang': 'cpp',
        'legenda': 'include/deriva/fila_de_comandos.hpp · duas threads, saída determinística',
        'nota': 'Concorrência não implica indeterminismo: a fila é FIFO e há um consumidor só. Com dois consumidores a ordem deixaria de ser garantida, e o replay não serviria mais.',
        'arquivo': 'exemplos/deriva/include/deriva/fila_de_comandos.hpp',
        'linha': 55,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Roda `quantos` comandos por uma fila, de uma thread produtora e uma
/// consumidora, e devolve a ordem em que foram consumidos.
///
/// Determinístico apesar de haver duas threads, e é isso que a Aula 22 quer
/// mostrar: concorrência não implica indeterminismo. A ordem é preservada
/// porque a fila é FIFO e há um consumidor só. Com dois consumidores, a ordem
/// deixaria de ser garantida - e aí o replay não serviria mais.
[[nodiscard]] std::string exercitar_fila(int quantos);""",
    },
    'produtora-consumidora': {
        'aula': 22,
        'lang': 'cpp',
        'legenda': 'src/fila_de_comandos.cpp · produtora e consumidora',
        'nota': 'A captura por referência é segura porque o `join` acontece antes de o escopo fechar. Sem ele, seriam referências a objetos destruídos - e o `join` esquecido é o defeito mais comum de quem começa.',
        'arquivo': 'exemplos/deriva/src/fila_de_comandos.cpp',
        'linha': 57,
        'quebrado_de_proposito': False,
        'codigo': """\
std::string exercitar_fila(int quantos) {
  fila_de_comandos fila;
  std::string consumido;

  std::thread produtora([&fila, quantos] {
    for (int i = 0; i < quantos; ++i) fila.empurrar("cmd" + std::to_string(i));
    fila.fechar();
  });

  // O consumidor é um só, e é isso que preserva a ordem. Com dois, a saída
  // deixaria de ser determinística e o replay não serviria.
  while (const std::optional<std::string> c = fila.puxar()) {
    consumido.append(*c).push_back(' ');
  }
  produtora.join();
  return consumido;""",
    },
    'notificar-fora-da-trava': {
        'aula': 22,
        'lang': 'cpp',
        'legenda': 'src/fila_de_comandos.cpp · notificar fora da região travada',
        'nota': 'Quem acorda tentaria travar de imediato, e acordar antes de destravar custa uma ida e volta a mais no escalonador. O escopo interno do `scoped_lock` existe para isso.',
        'arquivo': 'exemplos/deriva/src/fila_de_comandos.cpp',
        'linha': 8,
        'quebrado_de_proposito': False,
        'codigo': """\
void fila_de_comandos::empurrar(std::string comando) {
  {
    const std::scoped_lock trava(mutex_);
    if (fechada_) return;
    fila_.push_back(std::move(comando));
  }
  // Notificar FORA da região travada: quem acorda tentaria travar de imediato,
  // e acordar antes de destravar custa uma ida e volta a mais no escalonador.
  tem_coisa_.notify_one();
}""",
    },
    'sem-mutex': {
        'aula': 22,
        'lang': 'cpp',
        'legenda': 'include/deriva/medida_corrida.hpp · `vivos++` em duas threads',
        'nota': 'Três passos - lê, soma, escreve -, e nenhum deles atômico. É o mesmo contador da Aula 07, e é ele que perde o incremento.',
        'arquivo': 'exemplos/deriva/include/deriva/medida_corrida.hpp',
        'linha': 32,
        'quebrado_de_proposito': False,
        'codigo': """\
/// `vivos` compartilhado, sem proteção, incrementado por duas threads.
[[nodiscard]] inline int contar_sem_mutex(int por_thread) {
  int vivos = 0;
  auto somar = [&vivos, por_thread] {
    for (int i = 0; i < por_thread; ++i) {
      ++vivos;          // lê, soma, escreve: três passos, nenhum atômico
    }
  };
  std::thread a(somar), b(somar);
  a.join();
  b.join();
  return vivos;
}""",
    },
    'com-scoped-lock': {
        'aula': 22,
        'lang': 'cpp',
        'legenda': 'include/deriva/medida_corrida.hpp · a mesma conta, protegida',
        'nota': '`std::scoped_lock` é C++17 e aceita mais de um mutex, resolvendo a ordem de travamento sozinho - o que elimina uma classe inteira de impasse. Para um mutex só é equivalente ao `lock_guard`, e usar o novo é hábito.',
        'arquivo': 'exemplos/deriva/include/deriva/medida_corrida.hpp',
        'linha': 46,
        'quebrado_de_proposito': False,
        'codigo': """\
/// O mesmo, com a seção crítica serializada. `scoped_lock` é C++17 e
/// substitui `lock_guard` por aceitar mais de um mutex.
[[nodiscard]] inline int contar_com_mutex(int por_thread) {
  int vivos = 0;
  std::mutex m;
  auto somar = [&vivos, &m, por_thread] {
    for (int i = 0; i < por_thread; ++i) {
      const std::scoped_lock trava(m);
      ++vivos;
    }
  };
  std::thread a(somar), b(somar);
  a.join();
  b.join();
  return vivos;
}""",
    },
    'faixa-e-nao-numero': {
        'aula': 22,
        'lang': 'cpp',
        'legenda': 'include/deriva/medida_corrida.hpp · devolve a faixa, não um número',
        'nota': 'Corrida é comportamento indefinido, e o resultado varia entre execuções. O que se mede é a distribuição, e é ela a lição: oito execuções de dez não perderam nada.',
        'arquivo': 'exemplos/deriva/include/deriva/medida_corrida.hpp',
        'linha': 63,
        'quebrado_de_proposito': False,
        'codigo': """\
[[nodiscard]] inline corrida medir(int execucoes = 20, int por_thread = 100000) {
  corrida r;
  r.execucoes = execucoes;
  r.esperado = 2 * por_thread;
  r.perdidos_min = r.esperado;
  for (int k = 0; k < execucoes; ++k) {
    const int perdidos = r.esperado - contar_sem_mutex(por_thread);
    if (perdidos < r.perdidos_min) r.perdidos_min = perdidos;
    if (perdidos > r.perdidos_max) r.perdidos_max = perdidos;
    if (perdidos == 0) ++r.execucoes_sem_perda;
  }
  return r;
}""",
    },
    'observer-interface': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'include/deriva/apresentacao.hpp · Observer, a interface',
        'nota': 'Antes da refatoração o `mundo` chamava o log direto, abrindo arquivo, e por isso não dava para testar o log sem mexer no sistema de arquivos.',
        'arquivo': 'exemplos/deriva/include/deriva/apresentacao.hpp',
        'linha': 91,
        'quebrado_de_proposito': False,
        'codigo': """\
// ===========================================================================
// Observer · o log de eventos
//
// O `mundo` avisa que algo aconteceu e não sabe quem escuta. Antes da
// refatoração ele chamava o log direto, e por isso não dava para testar sem
// arquivo.
// ===========================================================================
class i_observador {
 public:
  virtual ~i_observador() = default;
  virtual void aconteceu(std::string_view evento) = 0;
};""",
    },
    'observer-em-memoria': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'include/deriva/apresentacao.hpp · o observador que substitui o arquivo',
        'nota': 'Vinte linhas, e é o que torna o log verificável. O `mundo` não sabe quem escuta, e é isso que Observer compra.',
        'arquivo': 'exemplos/deriva/include/deriva/apresentacao.hpp',
        'linha': 104,
        'quebrado_de_proposito': False,
        'codigo': """\
class registro_em_memoria final : public i_observador {
 public:
  void aconteceu(std::string_view evento) override;
  [[nodiscard]] const std::vector<std::string>& eventos() const noexcept {
    return eventos_;
  }

 private:
  std::vector<std::string> eventos_;
};""",
    },
    'observer-testado': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'testes/test_padroes.cpp · o log, verificado sem arquivo',
        'nota': 'Nenhum caminho, nenhuma permissão, nenhuma limpeza depois. É o teste que a versão anterior não conseguia ter.',
        'arquivo': 'exemplos/deriva/testes/test_padroes.cpp',
        'linha': 83,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("Observer permite testar o log sem arquivo") {
  registro_em_memoria log;
  i_observador& como_interface = log;
  como_interface.aconteceu("sonda entrou no setor");
  como_interface.aconteceu("item recolhido");
  REQUIRE(log.eventos().size() == 2);
  REQUIRE(log.eventos().front() == "sonda entrou no setor");
}""",
    },
    'adaptador-qt': {
        'aula': 26,
        'lang': 'cpp',
        'legenda': 'qt/janela.hpp · o adaptador, que não é QObject',
        'nota': 'Ele implementa a mesma interface que `apresentacao_em_texto`, e o núcleo não sabe qual das duas está do outro lado. O widget é guardado como ponteiro cru porque é observação: a árvore do Qt é a dona.',
        'arquivo': 'exemplos/deriva/qt/janela.hpp',
        'linha': 27,
        'quebrado_de_proposito': False,
        'codigo': """\
/// A implementação Qt de `i_apresentacao`.
///
/// Repare no que ela NÃO faz: não conhece regra de jogo, não decide o que
/// acontece num turno, não sabe o que é uma parede. Ela recebe um `mundo` e
/// desenha. É a mesma interface que `apresentacao_em_texto` implementa, e o
/// núcleo não sabe qual das duas está do outro lado.
class tela_qt final : public i_apresentacao {
 public:
  explicit tela_qt(QPlainTextEdit* alvo) : alvo_(alvo) {}

  void desenhar(const mundo& m) override;
  void mensagem(std::string_view texto) override;

 private:
  QPlainTextEdit* alvo_;   // observação, não posse: a árvore do Qt é a dona
};""",
    },
    'posse-na-arvore-do-qt': {
        'aula': 26,
        'lang': 'cpp',
        'legenda': 'qt/janela.cpp · `new` com pai ao lado de unique_ptr',
        'nota': '`new QPlainTextEdit(this)` entrega a posse ao pai, e `unique_ptr` sobre o adaptador guarda o que é nosso. As duas formas convivem na mesma função, e a diferença está em quem destrói.',
        'arquivo': 'exemplos/deriva/qt/janela.cpp',
        'linha': 20,
        'quebrado_de_proposito': False,
        'codigo': """\
janela::janela(mundo w, QWidget* pai)
    : QMainWindow(pai), mundo_(std::move(w)) {
  visor_ = new QPlainTextEdit(this);   // `this` é o pai: o Qt destrói
  visor_->setReadOnly(true);
  visor_->setFont(QFont("IBM Plex Mono", 12));
  setCentralWidget(visor_);

  tela_ = std::make_unique<tela_qt>(visor_);

  QMenu* menu = menuBar()->addMenu("Sonda");
  QAction* norte = menu->addAction("Norte");
  QAction* sul = menu->addAction("Sul");
  QAction* desfazer = menu->addAction("Desfazer");

  // A conexão por ponteiro de função é a forma verificada em compilação. A
  // forma antiga, com as macros SIGNAL e SLOT, casava strings em execução - e
  // um erro de digitação virava conexão que nunca acontece, sem aviso.
  connect(norte, &QAction::triggered, this, &janela::ao_mover_norte);
  connect(sul, &QAction::triggered, this, &janela::ao_mover_sul);
  connect(desfazer, &QAction::triggered, this, &janela::ao_desfazer);

  redesenhar();""",
    },
    'ordem-base-derivada': {
        'aula': 10,
        'lang': 'cpp',
        'legenda': 'testes/test_ciclo_de_vida.cpp · a ordem, afirmada',
        'nota': 'Base, membros na ordem de declaração, corpo da derivada - e o inverso exato ao morrer. O par instrumentado é local ao teste: poluir o despejo que o replay compara custaria a condição 3 do portão.',
        'arquivo': 'exemplos/deriva/testes/test_ciclo_de_vida.cpp',
        'linha': 116,
        'quebrado_de_proposito': False,
        'codigo': """\
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
}""",
    },
    'corpo-por-ultimo': {
        'aula': 10,
        'lang': 'cpp',
        'legenda': 'testes/test_ciclo_de_vida.cpp · a consequência da ordem',
        'nota': 'Quando o construtor da base roda, a derivada ainda não existe. É por isso que método virtual chamado dentro do construtor da base chama a versão DA BASE - o objeto ainda não é do tipo derivado.',
        'arquivo': 'exemplos/deriva/testes/test_ciclo_de_vida.cpp',
        'linha': 129,
        'quebrado_de_proposito': False,
        'codigo': """\
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
}""",
    },
    'tamanho-dos-ponteiros': {
        'aula': 12,
        'lang': 'cpp',
        'legenda': 'include/deriva/medida_posse.hpp · quanto custa cada ponteiro',
        'nota': '`unique_ptr` com deletor padrão é um ponteiro e nada mais; deletor vazio é absorvido pela otimização de base vazia; deletor com estado cobra o estado. `shared_ptr` é o dobro, porque leva o bloco de controle.',
        'arquivo': 'exemplos/deriva/include/deriva/medida_posse.hpp',
        'linha': 118,
        'quebrado_de_proposito': False,
        'codigo': """\
static_assert(sizeof(std::unique_ptr<int>) == sizeof(int*),
              "com o deletor padrao, um ponteiro e nada mais");
static_assert(sizeof(std::unique_ptr<int, deletor_sem_estado>) == sizeof(int*),
              "deletor vazio: a otimizacao de base vazia o absorve");
static_assert(sizeof(std::unique_ptr<int, deletor_com_estado>) ==
                  sizeof(int*) + sizeof(const char*),
              "deletor com estado cobra o estado dele, e o dobro e visivel");""",
    },
    'forward-preserva': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'include/deriva/encaminhamento.hpp · encaminhamento perfeito',
        'nota': '`T&&` num parâmetro dedutível não é referência a rvalue: é universal, e o colapso de referências faz a mesma assinatura servir para lvalue e rvalue. Trocar `forward` por `move` moveria SEMPRE, inclusive de um lvalue que o chamador ainda vai usar.',
        'arquivo': 'exemplos/deriva/include/deriva/encaminhamento.hpp',
        'linha': 47,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Fábrica **com** encaminhamento perfeito.
///
/// `T&&` num parâmetro de template dedutível NÃO é referência a rvalue: é
/// referência universal, e ela deduz `T` como `X&` para lvalue e como `X` para
/// rvalue. O colapso de referências faz `X& &&` virar `X&`, e é por isso que a
/// mesma assinatura serve para os dois casos.
///
/// `std::forward<T>(x)` devolve `x` na categoria de valor com que ele chegou.
/// Trocá-lo por `std::move(x)` moveria SEMPRE - inclusive de um lvalue que o
/// chamador ainda vai usar, e esse é o defeito clássico deste idioma.
template <class T, class... Args>
[[nodiscard]] std::unique_ptr<T> criar_encaminhando(Args&&... args) {
  return std::make_unique<T>(std::forward<Args>(args)...);
}""",
    },
    'forward-medido': {
        'aula': 14,
        'lang': 'cpp',
        'legenda': 'testes/test_encaminhamento.cpp · a origem segue utilizável',
        'nota': 'É este teste que `std::move` no lugar de `std::forward` quebraria, e a quebra seria silenciosa: o programa continuaria compilando.',
        'arquivo': 'exemplos/deriva/testes/test_encaminhamento.cpp',
        'linha': 31,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("e o lvalue continua chegando como lvalue") {
  como_chegou::limpar();
  carga_marcada original("peca");
  const auto p = criar_encaminhando<carga_marcada>(original);
  REQUIRE(p->rotulo() == "peca");
  REQUIRE(como_chegou::traco[1].find("COPIADA") == 0);
  // A origem continua utilizavel, e e isso que `std::move` no lugar de
  // `std::forward` teria estragado.
  REQUIRE(original.rotulo() == "peca");
}""",
    },
    'lsp-violado': {
        'aula': 24,
        'lang': 'cpp',
        'legenda': 'include/deriva/solid.hpp · a violação de LSP',
        'nota': 'Compila, e quebra a promessa da base: `mover` promete não lançar. O sintoma não aparece na parede - aparece em toda função que recebe `obstaculo&`, escrita antes de a parede existir e correta quando foi escrita.',
        'arquivo': 'exemplos/deriva/include/deriva/solid.hpp',
        'linha': 51,
        'quebrado_de_proposito': True,
        'codigo': """\
/// A VIOLAÇÃO. Compila, e quebra o contrato da base.
class parede_que_lanca final : public obstaculo {
 public:
  using obstaculo::obstaculo;
  [[nodiscard]] vetor2 mover(vetor2) override {
    throw std::logic_error("parede nao se move");
  }
};""",
    },
    'lsp-no-chamador': {
        'aula': 24,
        'lang': 'cpp',
        'legenda': 'testes/test_solid.cpp · LSP se mede no chamador',
        'nota': 'E o pior está na última linha: a caixa JÁ foi movida quando a exceção subiu. A função deixou o sistema no meio do caminho sem ter feito nada errado.',
        'arquivo': 'exemplos/deriva/testes/test_solid.cpp',
        'linha': 13,
        'quebrado_de_proposito': False,
        'codigo': """\
// ---- LSP -----------------------------------------------------------------
TEST_CASE("LSP: a violacao nao aparece na derivada, aparece no chamador") {
  caixa c({1, 1});
  parede_que_lanca p({5, 5});
  std::vector<obstaculo*> quais{&c, &p};

  // `empurrar_todos` foi escrita antes de a parede existir, e estava certa.
  REQUIRE_THROWS_AS(empurrar_todos(quais, {1, 0}), std::logic_error);

  // E o pior: a caixa JA foi movida quando a excecao subiu. A funcao deixou o
  // sistema no meio do caminho, sem ter feito nada errado.
  REQUIRE(c.pos() == vetor2{2, 1});
}""",
    },
    'isp-metodo-vazio': {
        'aula': 24,
        'lang': 'cpp',
        'legenda': 'include/deriva/solid.hpp · método vazio é a confissão',
        'nota': 'Quem só desenha é obrigado a implementar salvar e reparar, e mente em dois métodos. Método vazio numa interface é a confissão de que ela pede demais - e a métrica de ISP é contável: três obrigados contra um.',
        'arquivo': 'exemplos/deriva/include/deriva/solid.hpp',
        'linha': 89,
        'quebrado_de_proposito': True,
        'codigo': """\
/// Quem só desenha, obrigado a mentir em dois métodos.
class so_desenha_gordo final : public i_tudo {
 public:
  void desenhar() override { desenhou = true; }
  void salvar() override {}                       // vazio: a confissão
  void reparar() override {}                      // vazio: a segunda
  bool desenhou = false;
};""",
    },
    'state-transicao': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'src/padroes.cpp · State, e a transição é o retorno',
        'nota': 'Devolver a próxima tela em vez de mutar um campo é o que impede duas telas de discordarem sobre qual está ativa. A alternativa é um `switch` com vinte casos espalhados por cinco funções.',
        'arquivo': 'exemplos/deriva/src/padroes.cpp',
        'linha': 9,
        'quebrado_de_proposito': False,
        'codigo': """\
std::unique_ptr<i_tela> tela_mapa::comando(std::string_view c) {
  if (c == "i") return std::make_unique<tela_inventario>();
  if (c == "x") return std::make_unique<tela_inspecao>();
  return nullptr;   // fica onde está
}""",
    },
    'decorator-empilha': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'testes/test_padroes_extra.cpp · Decorator, empilhado',
        'nota': 'Com herança, "numerado e com moldura" exigiria uma classe para cada combinação. Com decorador, é a ordem da pilha - e a ordem é observável na saída.',
        'arquivo': 'exemplos/deriva/testes/test_padroes_extra.cpp',
        'linha': 50,
        'quebrado_de_proposito': False,
        'codigo': """\
// ---- Decorator -----------------------------------------------------------
TEST_CASE("Decorator: empilhar dois nao exige classe para cada combinacao") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{2, 1}));

  auto base = std::make_unique<apresentacao_em_texto>();
  apresentacao_em_texto* espiar = base.get();

  // numerado POR FORA da moldura: a ordem da pilha e observavel
  std::unique_ptr<i_apresentacao> tela = std::make_unique<com_numero_de_linha>(
      std::make_unique<com_moldura>(std::move(base), "SETOR"));

  tela->desenhar(w);
  const std::string saida = espiar->acumulado();

  REQUIRE(saida.find("┌─┤ SETOR ├─┐") != std::string::npos);
  REQUIRE(saida.find("[1]") != std::string::npos);
  REQUIRE(saida.find("└──┘") != std::string::npos);
}""",
    },
    'singleton-criticado': {
        'aula': 25,
        'lang': 'cpp',
        'legenda': 'include/deriva/padroes.hpp · Singleton, escrito para ser criticado',
        'nota': 'É o Singleton de Meyers, a versão correta da forma errada. Os quatro custos estão no comentário, e nenhum é opinião - o segundo deles é medido por dois casos de teste que compartilham estado de propósito.',
        'arquivo': 'exemplos/deriva/include/deriva/padroes.hpp',
        'linha': 104,
        'quebrado_de_proposito': False,
        'codigo': """\
// ===========================================================================
// Singleton · escrito para ser criticado
//
// O material recomenda NÃO usá-lo, e escrevê-lo é a forma de mostrar por quê.
// Este é o Singleton de Meyers, que é a versão correta da forma errada: a
// inicialização de estático local é garantidamente única e segura entre
// threads desde C++11.
//
// Os quatro custos, e nenhum deles é opinião:
//   1. o teste não consegue substituí-lo, porque quem o usa o pede por nome;
//   2. dois testes na mesma execução compartilham o estado dele;
//   3. a ordem de destruição entre estáticos não é controlável;
//   4. ele esconde uma dependência que a assinatura deveria declarar.
//
// O contador `vivos` da Aula 07 é estado global mutável, e este material o usa
// assim - como INSTRUMENTO, e não como projeto. A diferença vale ser dita: o
// contador não participa da lógica do jogo, e nenhuma decisão do domínio
// depende dele.
// ===========================================================================
class registro_global {
 public:
  static registro_global& instancia();

  void anotar(std::string_view evento);
  [[nodiscard]] std::size_t quantos() const noexcept { return eventos_.size(); }
  void limpar() { eventos_.clear(); }

  registro_global(const registro_global&) = delete;
  registro_global& operator=(const registro_global&) = delete;

 private:
  registro_global() = default;
  std::vector<std::string> eventos_;
};""",
    },
    'prova-do-segundo-frontend': {
        'aula': 26,
        'lang': 'cpp',
        'legenda': 'testes/test_padroes.cpp · a prova do critério da §26.1',
        'nota': 'Duas implementações da mesma interface, no mesmo processo, sobre o mesmo mundo. É o que a variante `v2.6-antes` torna impossível, e é a diferença entre separação demonstrada e separação afirmada.',
        'arquivo': 'exemplos/deriva/testes/test_padroes.cpp',
        'linha': 170,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("duas apresentacoes sobre o MESMO mundo, e ele nao sabe qual") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));

  // (2) Duas implementações independentes da mesma interface, no mesmo
  //     processo, sobre o mesmo mundo. É o que a v2.7 faz com Qt, e o que a
  //     variante `v2.6-antes` torna impossível.
  apresentacao_em_texto a;
  apresentacao_em_texto b;
  i_apresentacao& como_a = a;
  i_apresentacao& como_b = b;

  como_a.desenhar(w);
  como_b.mensagem("segunda interface");
  como_b.desenhar(w);

  REQUIRE(a.acumulado().find("entidades 1") != std::string::npos);
  REQUIRE(b.acumulado().find("> segunda interface") == 0);
  REQUIRE(b.acumulado().find("entidades 1") != std::string::npos);
}""",
    },
    'render-nao-muda-estado': {
        'aula': 26,
        'lang': 'cpp',
        'legenda': 'testes/test_padroes.cpp · desenhar não altera o mundo',
        'nota': 'Cinco renders, e o despejo byte a byte igual. Se desenhar mudasse estado, a segunda interface veria um sistema diferente da primeira.',
        'arquivo': 'exemplos/deriva/testes/test_padroes.cpp',
        'linha': 192,
        'quebrado_de_proposito': False,
        'codigo': """\
TEST_CASE("trocar a apresentacao nao muda o estado do dominio") {
  // (3) O critério mais forte: desenhar não pode alterar o mundo. Se
  //     desenhar mudasse estado, a segunda interface veria um sistema
  //     diferente da primeira.
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  const std::string antes = w.despejar();

  apresentacao_em_texto tela;
  for (int k = 0; k < 5; ++k) tela.desenhar(w);

  REQUIRE(w.despejar() == antes);   // byte a byte, depois de cinco renders
}""",
    },
    'concept-em-vez-de-assert': {
        'aula': 0,
        'lang': 'cpp',
        'legenda': 'c20/restricoes.hpp · o concept no lugar do static_assert',
        'nota': 'A diferença que se vê é a mensagem de erro: com `static_assert` o compilador aponta a linha do assert; com `concept`, aponta a CHAMADA e diz qual restrição falhou. É a razão de os concepts existirem.',
        'arquivo': 'exemplos/deriva/c20/restricoes.hpp',
        'linha': 36,
        'quebrado_de_proposito': False,
        'codigo': """\
concept guardavel = std::default_initializable<T> && !std::is_reference_v<T> &&
                    !std::same_as<T, bool>;""",
    },
    'ranges-sem-temporario': {
        'aula': 0,
        'lang': 'cpp',
        'legenda': 'c20/restricoes.hpp · ranges, sem contêiner intermediário',
        'nota': '`filter` e `transform` são vistas preguiçosas: nada é copiado até alguém iterar. Em C++17 o equivalente seria um `copy_if` para um vetor temporário e um `transform` depois - dois laços e uma alocação.',
        'arquivo': 'exemplos/deriva/c20/restricoes.hpp',
        'linha': 61,
        'quebrado_de_proposito': False,
        'codigo': """\
/// Ranges no lugar do laço, sobre as células da grade.
///
/// O que se ganha é composição sem contêiner intermediário: `filter` e
/// `transform` são vistas preguiçosas, e nada é copiado até alguém iterar. Em
/// C++17 o equivalente seria um `copy_if` para um vetor temporário e um
/// `transform` depois - dois laços e uma alocação.
[[nodiscard]] inline std::string glifos_de_parede(const grade_restrita<celula>& g) {
  std::string s;
  for (const celula& c : g.todas()
                             | std::views::filter([](const celula& x) {
                                 return x.glifo == '#';
                               })
                             | std::views::take(10)) {
    s.push_back(c.glifo);
  }""",
    },
    'optional-filesystem': {
        'aula': 20,
        'lang': 'cpp',
        'legenda': 'src/mapa.cpp · optional e filesystem',
        'nota': 'Arquivo ausente é *ausência de resultado*, não exceção - `optional` diz isso no tipo. Erro de verdade, permissão negada, é exceção, e chega na v2.2. Repare que `exists` e abrir são operações distintas: a corrida entre elas é real.',
        'arquivo': 'exemplos/deriva/src/mapa.cpp',
        'linha': 109,
        'quebrado_de_proposito': False,
        'codigo': """\
std::optional<mapa> mapa::carregar(const std::filesystem::path& caminho) {
  std::error_code ec;
  if (!std::filesystem::exists(caminho, ec) || ec) return std::nullopt;
  if (!std::filesystem::is_regular_file(caminho, ec) || ec) return std::nullopt;

  std::ifstream arq(caminho);
  if (!arq) return std::nullopt;
  std::ostringstream buf;
  buf << arq.rdbuf();
  const std::string texto = buf.str();
  return de_texto(texto, caminho.stem().string());
}""",
    },
    'uml-mapa-tem-grade': {
        'aula': 6,
        'lang': 'mermaid',
        'legenda': 'diagramas/mapa-tem-grade.mmd · mapa TEM uma grade',
        'nota': 'A seta de composição, e não de herança: `mapa` guarda uma `grade` como membro. As oito relações que este desenho afirma são as que `testes/test_uml.cpp` verifica, uma por caso.',
        'arquivo': 'exemplos/deriva/diagramas/mapa-tem-grade.mmd',
        'linha': 8,
        'quebrado_de_proposito': False,
        'codigo': """\
classDiagram
  class mapa {
    -string nome_
    -grade grade_
    -vetor2 entrada_
    -marca_de_vida marca_
    +carregar(path) optional~mapa~
    +de_texto(string_view, string) optional~mapa~
    +despejar() string
  }
  class grade {
    -int largura_
    -int altura_
    -vector~celula~ celulas_
    +dentro(vetor2) bool
    +em(vetor2) celula&
  }
  class celula {
    +int energia
    +int massa
    +char glifo
    +char sigla
  }
  class vetor2 {
    +int x
    +int y
    +manhattan(vetor2) int
  }
  class marca_de_vida {
    -string nome_
  }
  class instrumento {
    +anotar(string_view, string_view) void
    +traco() vector~string~
  }
  mapa "1" *-- "1" grade
  mapa "1" *-- "1" vetor2 : entrada
  mapa "1" *-- "1" marca_de_vida
  grade "1" *-- "largura x altura" celula
  grade ..> vetor2 : parametro""",
    },
    'uml-carregar-sequencia': {
        'aula': 6,
        'lang': 'mermaid',
        'legenda': 'diagramas/carregar-em-sequencia.mmd · carregar, passo a passo',
        'nota': 'O caminho de `mapa::carregar` com os dois desfechos: `nullopt` quando o arquivo falta, e o mapa construído quando ele existe. A ausência é resposta, e não exceção.',
        'arquivo': 'exemplos/deriva/diagramas/carregar-em-sequencia.mmd',
        'linha': 8,
        'quebrado_de_proposito': False,
        'codigo': """\
sequenceDiagram
  participant m as main()
  participant mp as mapa (estatico)
  participant g as grade
  m->>mp: carregar(caminho)
  mp->>mp: exists() e is_regular_file()
  alt arquivo ausente ou irregular
    mp-->>m: nullopt
  else arquivo lido
    mp->>mp: de_texto(texto, nome)
    mp->>mp: parte em fileiras (string_view, sem alocar)
    alt fileira de largura divergente
      mp-->>m: nullopt
    else fileiras consistentes
      mp->>g: grade(largura, altura)
      g-->>mp: grade construida
      mp->>g: em(p) para cada celula
      mp->>mp: acha a entrada '@'
      mp-->>m: optional~mapa~ com valor
    end""",
    },
    'uml-grade-sozinha': {
        'aula': 6,
        'lang': 'mermaid',
        'legenda': 'diagramas/grade-sozinha.mmd · a grade e os seus membros',
        'nota': 'A grade isolada, com o que ela declara e mais nada. É o desenho que o Cap. 6 usa para introduzir a notação antes de haver hierarquia nenhuma no sistema.',
        'arquivo': 'exemplos/deriva/diagramas/grade-sozinha.mmd',
        'linha': 8,
        'quebrado_de_proposito': False,
        'codigo': """\
classDiagram
  class grade {
    -int largura_
    -int altura_
    -vector~celula~ celulas_
    +grade(int largura, int altura)
    +largura() int
    +altura() int
    +dentro(vetor2 p) bool
    +em(vetor2 p) celula&
    +bytes_das_celulas() size_t""",
    },
    'uml-agregados': {
        'aula': 7,
        'lang': 'mermaid',
        'legenda': 'diagramas/agregados-e-leiaute.mmd · os agregados e o leiaute',
        'nota': '`vetor2` e `celula` como agregados, e a `celula_ingenua` ao lado para mostrar o que a ordem de declaração custa. O `$` marca o membro estático, que não vive dentro do objeto.',
        'arquivo': 'exemplos/deriva/diagramas/agregados-e-leiaute.mmd',
        'linha': 8,
        'quebrado_de_proposito': False,
        'codigo': """\
classDiagram
  class vetor2 {
    +int x
    +int y
    +operator==(vetor2) bool
    +manhattan(vetor2) int
  }
  class celula {
    +int energia
    +int massa
    +char glifo
    +char sigla
  }
  class celula_ingenua {
    +char glifo
    +int energia
    +char sigla
    +int massa
  }
  class contador_mapa {
    +int vivos$
    +int criados$""",
    },
}
