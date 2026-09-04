# -*- coding: utf-8 -*-
"""
conteudo/trechos.py - quais trechos do Deriva entram em qual aula.

Regra do handoff §5, e é dura: *todo trecho de código do site e do livro é
extraído de arquivo que compila, nunca digitado no material. Trecho literal
solto é dívida.*

Cada entrada aponta para um arquivo real de `exemplos/deriva/`, delimitado por
duas âncoras de texto. Se o código mudar de forma que a âncora não exista
mais, `build/extrair_codigo.py` **falha** - e é para isso que serve: material
que aponta para código que já não existe é pior que material sem código.

Campos:
  id        identificador estável
  aula      em que aula o trecho aparece
  arquivo   caminho a partir da raiz do repositório
  de        primeira linha a incluir (casamento por substring)
  ate       última linha a incluir (casamento pela linha inteira, sem espaço)
  comentario  incluir o bloco de comentário imediatamente acima do `de`
  legenda   o que vai no cabeçalho do bloco
  nota      uma frase dizendo por que este trecho está aqui
  quebrado  este trecho é de variante deliberadamente quebrada
  inline    o material o renderiza NO LUGAR (é o caso dos diagramas, que vivem
            dentro do slide que os explica) e por isso ele NÃO entra na seção
            "O código, extraído do Deriva" do fim - senão apareceria duas vezes
"""

TRECHOS = [
    # ---- Aula 01 · do procedural ao objeto ---------------------------------
    dict(id="grade-em-c", aula=1,
         arquivo="exemplos/deriva/comparativo/grade_procedural.hpp",
         de="struct grade_c {", ate="};", comentario=True,
         legenda="comparativo/grade_procedural.hpp · a grade em estilo C",
         nota="Cinco regras que só existem na cabeça de quem chama, e nenhuma delas "
              "está escrita no código. A métrica da Aula 01 não é elegância: é quantas "
              "maneiras de errar o desenho permite - sete aqui, uma na versão OO."),
    dict(id="copia-que-nao-copia", aula=1,
         arquivo="exemplos/deriva/testes/test_comparativo.cpp",
         de='TEST_CASE("em C, a copia da struct compartilha o buffer', ate="}",
         comentario=True, quebrado=True,
         legenda="testes/test_comparativo.cpp · a cópia que não copia",
         nota="Copiar a struct leva o ponteiro, não os dados, e ninguém avisa. A versão "
              "C++ faz a cópia profunda pela regra do zero, sem escrever uma linha - e "
              "é essa diferença, e não a sintaxe, que o capítulo defende."),
    dict(id="vazamento-sem-sintoma", aula=1,
         arquivo="exemplos/deriva/testes/test_comparativo.cpp",
         de='TEST_CASE("em C, esquecer destruir nao produz sintoma', ate="}",
         comentario=True, quebrado=True,
         legenda="testes/test_comparativo.cpp · o vazamento que passa no teste",
         nota="Dez quilobytes vazam e o teste passa, porque o vazamento não tem "
              "sintoma. É o argumento inteiro do contador de instâncias da Aula 07."),

    # ---- Aula 04 · a rubrica aplicada -------------------------------------
    dict(id="codigo-gerado", aula=4,
         arquivo="exemplos/deriva/revisao_ia/gerado.hpp",
         de="struct sensor_base {", ate="};", comentario=True, quebrado=True,
         legenda="revisao_ia/gerado.hpp · o que um modelo produz",
         nota="Compila sem um aviso e passa no teste que o próprio modelo escreveu. Tem "
              "três defeitos plantados, um por item da rubrica, e nenhum é erro de "
              "digitação: os três são decisões plausíveis, e é isso que os torna caros."),
    dict(id="teste-que-nao-prova", aula=4,
         arquivo="exemplos/deriva/testes/test_revisao_ia.cpp",
         de='TEST_CASE("o teste que veio com o codigo gerado passa")', ate="}",
         comentario=True,
         legenda="testes/test_revisao_ia.cpp · o teste que o modelo escreveu",
         nota="Ele passa, e não prova nada do que importa. É o item R7 da rubrica: o "
              "teste tem de falhar se o comportamento mudar, e não se a implementação "
              "mudar."),
    dict(id="defeito-invariante", aula=4,
         arquivo="exemplos/deriva/testes/test_revisao_ia.cpp",
         de='TEST_CASE("R1: o vetor publico anula a invariante', ate="}",
         legenda="testes/test_revisao_ia.cpp · R1, medido nos dois lados",
         nota="Com o vetor público, `registrar` protege uma invariante que qualquer um "
              "contorna de fora - e a média passa a mentir. A versão revisada recusa o "
              "valor e mantém o vetor privado."),

    # ---- Aula 05 · linguagens e sistemas de tipos --------------------------
    dict(id="despacho-simples", aula=5, arquivo="exemplos/deriva/tipos/despacho.cpp",
         de="std::string resolver(const colisao& a, const colisao& b) {", ate="}",
         comentario=True,
         legenda="tipos/despacho.cpp · C++ tem despacho simples",
         nota="Duas perguntas de tipo, uma por operando, porque `virtual` resolve por "
              "um só. Com N tipos esta função cresce com N², e é esse crescimento que "
              "faz o Visitor existir. Se houvesse despacho múltiplo, a função não "
              "existiria."),
    dict(id="explicit-recusa", aula=5, arquivo="exemplos/deriva/tipos/despacho.hpp",
         de="struct fahrenheit {", ate="};", comentario=True,
         legenda="tipos/despacho.hpp · forte por padrão, fraco por convite",
         nota="Sem `explicit`, trinta graus Celsius viraria trinta Fahrenheit em "
              "silêncio. Com ele, o compilador exige a conversão escrita - e é aí que "
              "o sistema de tipos fica forte."),
    dict(id="trait-a-mao", aula=5, arquivo="exemplos/deriva/tipos/despacho.hpp",
         de="struct tem_glifo : std::false_type {};", ate="",
         comentario=True,
         legenda="tipos/despacho.hpp · trait em C++ é template, não construção",
         nota="Em Rust ou Scala o trait é construção da linguagem; aqui é um template "
              "que responde sobre um tipo. O teste o aplica a `sonda` e a `mapa`, e a "
              "resposta vem sem executar nada."),

    # ---- Aula 06 · UML leve ------------------------------------------------
    dict(id="uml-conferida", aula=6, arquivo="exemplos/deriva/testes/test_uml.cpp",
         de='TEST_CASE("relacao 3: composicao, e nao heranca")', ate="}",
         comentario=True,
         legenda="testes/test_uml.cpp · o diagrama, conferido",
         nota="`mapa` TEM uma grade, e o desenho usa losango e não triângulo. Diagrama "
              "que ninguém confere envelhece calado, e a versão desenhada passa a "
              "descrever um sistema que já não existe."),
    dict(id="uml-final-retirado", aula=6, arquivo="exemplos/deriva/testes/test_uml.cpp",
         de='TEST_CASE("sonda NAO e final', ate="}", comentario=True,
         legenda="testes/test_uml.cpp · o que o desenho não pode afirmar",
         nota="`sonda` era `final` na v1.0 e deixou de ser na v1.7. Este teste protege "
              "contra a tentação de o diagrama continuar dizendo que é - foi um "
              "diagrama envelhecido que motivou escrever este arquivo."),

    # ---- Aula 02 · infraestrutura ------------------------------------------
    dict(id="cmake-nucleo", aula=2, arquivo="exemplos/deriva/CMakeLists.txt",
         de="add_library(deriva_nucleo", ate=")", comentario=True,
         legenda="CMakeLists.txt · a biblioteca do núcleo",
         nota="O núcleo não conhece UI nenhuma. É esta separação, e não uma "
              "promessa, que faz o argumento do segundo front-end da Aula 26 fechar."),
    dict(id="cmake-warnings", aula=2, arquivo="exemplos/deriva/CMakeLists.txt",
         de="target_compile_options(deriva_nucleo PRIVATE", ate=")", comentario=True,
         legenda="CMakeLists.txt · o portão de warning",
         nota="Os avisos incidem no núcleo e só nele. FTXUI e Catch2 entram como "
              "SYSTEM logo abaixo - para que o aviso deles não conte, e para que "
              "ninguém se esconda atrás deles."),
    dict(id="cmake-ftxui", aula=2, arquivo="exemplos/deriva/CMakeLists.txt",
         de="  FetchContent_Declare(ftxui", ate="  )", comentario=True,
         legenda="CMakeLists.txt · FTXUI com tag fixa",
         nota="A tag não flutua. A v5.0.0 declara cxx_std_17; as v6/v7 podem "
              "elevar o padrão exigido e derrubar o alvo da disciplina."),

    dict(id="gdb-no-destrutor", aula=2, arquivo="exemplos/deriva/Makefile",
         de="gdb-dtor:", ate="", comentario=True,
         legenda="Makefile · gdb com ponto de parada em destrutor",
         nota="A terceira das três técnicas que substituem o sanitizer ausente. É "
              "ela que mostra, na Aula 11, o destrutor da derivada nunca sendo "
              "alcançado quando se deleta por ponteiro da base."),

    dict(id="fora-de-limite", aula=2,
         arquivo="exemplos/deriva/sanitizers/defeitos_de_memoria.cpp",
         de="[[nodiscard]] celula& em(int x, int y) {", ate="}", comentario=True,
         quebrado=True,
         legenda="sanitizers/defeitos_de_memoria.cpp · sem `dentro()` ao lado",
         nota="O `operator[]` do `vector` não confere limite - `at()` conferiria, e é "
              "a escolha que a versão boa deixa explícita para quem chama. O ASan "
              "aponta a linha da escrita E a linha da alocação, que é a informação "
              "que faltava."),
    dict(id="estouro-com-sinal", aula=2,
         arquivo="exemplos/deriva/sanitizers/defeitos_de_memoria.cpp",
         de="const int largura = std::atoi(", ate='std::puts("   a versao boa converte CADA fator ANTES de multiplicar.");',
         comentario=True, quebrado=True,
         legenda="sanitizers/defeitos_de_memoria.cpp · o estouro que não avisa",
         nota="Com literais, o g++ dobra a conta, vê o estouro e avisa por "
              "`-Woverflow`. Com os valores vindo de fora ele não tem o que dobrar, o "
              "aviso desaparece, e o estouro passa a acontecer em execução. O "
              "compilador pega o que consegue ver, e é por isso que o defeito real "
              "nunca chega com número escrito no código."),

    # ---- Aula 03 · fundamentos de C++17 ------------------------------------
    dict(id="string-view-vida", aula=3, arquivo="exemplos/deriva/src/mapa.cpp",
         de="std::optional<mapa> mapa::de_texto", ate="  if (fileiras.empty()) return std::nullopt;",
         legenda="src/mapa.cpp · string_view e tempo de vida",
         nota="`string_view` não possui os bytes. As fileiras apontam para dentro "
              "de `texto`, e nada disso é guardado depois - se fosse, seriam "
              "referências penduradas no instante em que a função retornasse."),
    dict(id="ligacao-estruturada", aula=3, arquivo="exemplos/deriva/src/main.cpp",
         de="    static const std::pair<std::string_view, deriva::vetor2> tabela[]",
         ate="    }", comentario=True,
         legenda="src/main.cpp · ligação estruturada",
         nota="`for (const auto& [nome, delta] : tabela)` - por referência, e "
              "`const` porque só se lê. Copiar por valor aqui seria copiar a "
              "tabela inteira a cada volta."),
    dict(id="string-view-sem-nul", aula=3,
         arquivo="exemplos/deriva/testes/test_string_view.cpp",
         de='TEST_CASE("caso 3', ate="}", comentario=True,
         legenda="testes/test_string_view.cpp · a vista não termina em nul",
         nota="É o caso que mais morde: `strlen(vista.data())` devolve o tamanho da "
              "string de origem, não o da vista. Para uma API de C o caminho é "
              "`std::string(vista)`, que copia de propósito - e aí o custo está "
              "declarado."),
    dict(id="maybe-unused", aula=3,
         arquivo="exemplos/deriva/testes/test_ciclo_de_vida.cpp",
         de="[[maybe_unused]] const marca_de_vida a(", ate="}", comentario=True,
         legenda="testes/test_ciclo_de_vida.cpp · [[maybe_unused]]",
         nota="O atributo diz ao compilador o que `(void)x` dizia por gesto: o objeto "
              "existe pelo efeito do construtor e do destrutor, não pelo valor."),
    dict(id="nodiscard-vetor2", aula=3,
         arquivo="exemplos/deriva/include/deriva/vetor2.hpp",
         de="struct vetor2 {", ate="};",
         legenda="include/deriva/vetor2.hpp · v0.1",
         nota="`[[nodiscard]]` numa comparação: chamar `a == b` e jogar o "
              "resultado fora é sempre erro, e agora o compilador diz isso."),

    # ---- Aula 07 · classes, objetos, o contador ----------------------------
    dict(id="celula-boa", aula=7, arquivo="exemplos/deriva/include/deriva/celula.hpp",
         de="struct celula {", ate="};", comentario=True,
         legenda="include/deriva/celula.hpp · 12 bytes",
         nota="Agrupada por tamanho. Os offsets no comentário não são estimativa: "
              "os `static_assert` no fim do arquivo os afirmam, e o build falha se "
              "mudarem."),
    dict(id="celula-ingenua", aula=7, arquivo="exemplos/deriva/include/deriva/celula.hpp",
         de="struct celula_ingenua {", ate="};", comentario=True,
         legenda="include/deriva/celula.hpp · 16 bytes",
         nota="A MESMA célula, na ordem em que se pensa nela. Quatro bytes a mais "
              "por célula, 7,5 KB numa grade de 80×24, e nada em troca."),
    dict(id="static-assert-leiaute", aula=7,
         arquivo="exemplos/deriva/include/deriva/celula.hpp",
         de="static_assert(sizeof(celula) == 12", ate="",
         legenda="include/deriva/celula.hpp · os números, aferidos",
         nota="É esta linha que impede o material de mentir. Se o leiaute mudar, "
              "o Deriva não compila - e o interativo da Aula 07 não passa a "
              "exibir número errado em silêncio."),
    dict(id="contador-vivos", aula=7,
         arquivo="exemplos/deriva/include/deriva/contador.hpp",
         de="struct contador_mapa {", ate="};", comentario=True,
         legenda="include/deriva/contador.hpp · o detector de vazamento",
         nota="`inline static` é variável inline, C++17: dispensa a definição num "
              ".cpp. A repetição em cada classe é deliberada - é ela que motiva o "
              "`contador_de_instancias<T>` da Aula 19."),

    # ---- Aula 08 · ciclo de vida e RAII ------------------------------------
    dict(id="lista-de-inicializacao", aula=8, arquivo="exemplos/deriva/src/grade.cpp",
         de="[[nodiscard]] int exigir_positivo", ate="}", comentario=True,
         legenda="src/grade.cpp · validar NA lista de inicialização",
         nota="A primeira versão validava no corpo, e um teste pegou: com "
              "`grade(5, -1)` o vector lançava `length_error` antes de o corpo "
              "rodar. A lista de inicialização acontece inteira antes da primeira "
              "linha do corpo."),
    dict(id="marca-de-vida", aula=8, arquivo="exemplos/deriva/src/instrumento.cpp",
         de="marca_de_vida::marca_de_vida(std::string nome)",
         ate="marca_de_vida& marca_de_vida::operator=(const marca_de_vida& o) {",
         comentario=True,
         legenda="src/instrumento.cpp · instrumentação de ciclo de vida",
         nota="Construtor e destrutor imprimindo a própria execução. Substitui o "
              "sanitizer que o laboratório não tem: o estudante LÊ o traço e o "
              "compara com o roteiro."),
    dict(id="terminal-raii", aula=8, arquivo="exemplos/deriva/src/terminal_bruto.cpp",
         de="terminal_bruto::terminal_bruto() {", ate="}", comentario=True,
         legenda="src/terminal_bruto.cpp · o construtor adquire",
         nota="`isatty` primeiro: em pipe, em teste ou em CI não há modo bruto a "
              "alterar. Sem essa guarda, `ctest` deixaria o terminal de quem roda "
              "os testes em estado imprevisível."),
    dict(id="terminal-dtor", aula=8, arquivo="exemplos/deriva/src/terminal_bruto.cpp",
         de="terminal_bruto::~terminal_bruto() {", ate="}", comentario=True,
         legenda="src/terminal_bruto.cpp · o destrutor libera",
         nota="Duas linhas. São elas que separam “o terminal volta ao normal” de "
              "“o estudante digita `reset` às cegas” - e o recurso aqui sobrevive "
              "ao processo, então ninguém vai desfazer isso por ele."),
    dict(id="traco-excecao", aula=8,
         arquivo="exemplos/deriva/testes/test_ciclo_de_vida.cpp",
         de='TEST_CASE("a excecao nao pula destrutor', ate="}", comentario=True,
         legenda="testes/test_ciclo_de_vida.cpp · o desenrolar da pilha",
         nota="O teste afirma a ordem exata, linha por linha. A exceção não pula "
              "os destrutores: ela os chama, de dentro para fora. É essa garantia, "
              "e nada mais, que faz RAII funcionar."),

    # ---- Aula 09 · regra do zero e do três --------------------------------
    dict(id="grade-regra-do-zero", aula=9,
         arquivo="exemplos/deriva/include/deriva/grade.hpp",
         de="class grade {", ate="};", comentario=True,
         legenda="include/deriva/grade.hpp · regra do zero",
         nota="Nenhuma das cinco operações especiais é declarada. O único membro "
              "que gerencia recurso é o `std::vector`, e as operações que o "
              "compilador gera são melhores que as que escreveríamos - e não ficam "
              "desatualizadas quando um membro novo aparecer."),
    dict(id="grade-quebrada", aula=9,
         arquivo="exemplos/deriva/variantes/v0.3-quebrada/grade_quebrada.cpp",
         de="class grade {", ate="};", comentario=True, quebrado=True,
         legenda="v0.3-quebrada · cópia rasa · CAÇA AO BUG 1",
         nota="Destrutor declarado, cópia esquecida: a violação mais barata da "
              "regra do três, e a que mais sobrevive à revisão. `-Wall -Wextra "
              "-Wpedantic` não emite uma palavra sobre isto."),
    dict(id="copia-nao-pedida", aula=9,
         arquivo="exemplos/deriva/testes/test_mapa.cpp",
         de='TEST_CASE("o contador de instancias vivas fecha em zero")', ate="}",
         legenda="testes/test_mapa.cpp · o contador como portão",
         nota="Três objetos nascem para um `carregar`, e o contador soma os três. "
              "Repare no que ele NÃO distingue: depois de a Aula 14 acrescentar o "
              "construtor de movimento, o número continua três, porque continuam "
              "sendo três nascimentos - o que mudou foi o custo de cada um. O "
              "contador conta objetos, não alocações, e saber o que o instrumento "
              "não vê vale tanto quanto saber usá-lo."),

    # ---- Aula 13 · posse compartilhada ------------------------------------
    dict(id="ciclo-medido", aula=13,
         arquivo="exemplos/deriva/include/deriva/medida_posse.hpp",
         de="template <class Aloc>", ate="}", comentario=True,
         legenda="include/deriva/medida_posse.hpp · o ciclo, medido",
         nota="O vazamento do ciclo não dá para travar em `static_assert`: o tamanho "
              "do bloco de controle é escolha da implementação. Então ele é medido, "
              "por um alocador que conta exatamente o que o `shared_ptr` pede."),
    dict(id="alocador-que-conta", aula=13,
         arquivo="exemplos/deriva/include/deriva/medida_posse.hpp",
         de="struct contagem {", ate="};", comentario=True,
         legenda="include/deriva/medida_posse.hpp · a armadilha do rebind",
         nota="`std::allocate_shared` não usa o alocador que você passa: ele o "
              "rebinda para o tipo interno do bloco de controle. Contador "
              "`inline static` dentro do template conta na instanciação errada, e a "
              "primeira versão desta medida deu zero byte vazado por isso."),

    # ---- Aula 10 · herança simples ----------------------------------------
    dict(id="hierarquia-entidade", aula=10,
         arquivo="exemplos/deriva/include/deriva/entidade.hpp",
         de="class entidade {", ate="};", comentario=True,
         legenda="include/deriva/entidade.hpp · a base que o domínio pediu",
         nota="A hierarquia é a que o domínio pede: sonda, drone e item são coisas "
              "diferentes que ocupam posição e desenham um glifo. O contador de "
              "instâncias mora em cada classe concreta, não na base - o da base "
              "contaria objetos e não tipos."),
    dict(id="final-retirado", aula=10,
         arquivo="exemplos/deriva/include/deriva/entidade.hpp",
         de="class sonda : public entidade {", ate="int energia_;", comentario=True,
         legenda="include/deriva/entidade.hpp · o `final` que teve de sair",
         nota="Na v1.0 esta classe era `final`. A v1.7 introduziu a "
              "`sonda_reparadora` e o compilador recusou: \"cannot derive from final "
              "base\". A palavra saiu, e a lição fica - `final` é promessa, e "
              "retirá-la é admitir que a hierarquia mudou de forma."),
    dict(id="template-method", aula=10, arquivo="exemplos/deriva/src/entidade.cpp",
         de="std::string entidade::descrever() const {", ate="}", comentario=True,
         legenda="src/entidade.cpp · Template Method na forma mais curta",
         nota="Não-virtual chamando virtual: a moldura do texto é da base, o glifo e "
              "o nome são da derivada, e nenhuma derivada reescreve o formato."),

    # ---- Aula 11 · virtuais e destrutor virtual ----------------------------
    dict(id="destrutor-virtual-provado", aula=11,
         arquivo="exemplos/deriva/testes/test_entidade.cpp",
         de='TEST_CASE("deletar por entidade* destroi a derivada")', ate="}",
         comentario=True,
         legenda="testes/test_entidade.cpp · a prova do destrutor virtual",
         nota="O contador de cada classe concreta é o que acusa. Sem `virtual` no "
              "destrutor da base, `sonda::vivos` ficaria em 1 no fim do escopo - e "
              "nenhum aviso apareceria, porque o `delete` mora dentro do `unique_ptr`."),
    dict(id="tres-avisos", aula=11,
         arquivo="exemplos/deriva/variantes/v1.1-quebrada/destrutor_quebrado.cpp",
         de="struct entidade {", ate="};", comentario=True, quebrado=True,
         legenda="v1.1-quebrada · destrutor não virtual · CAÇA AO BUG 2",
         nota="Medido em g++ 13.3: `delete` textual dá 1 aviso; o mesmo `delete` "
              "dentro de `unique_ptr` dá ZERO, porque passou a morar num cabeçalho "
              "do sistema; com `-Wnon-virtual-dtor` são 3, e nas declarações. C++ "
              "moderno, correto em tudo o mais, silenciou o único diagnóstico."),

    # ---- Aula 12 · posse exclusiva ----------------------------------------
    dict(id="posse-no-tipo", aula=12, arquivo="exemplos/deriva/include/deriva/mundo.hpp",
         de="class mundo {", ate="};", comentario=True,
         legenda="include/deriva/mundo.hpp · a posse declarada no tipo",
         nota="`vector<unique_ptr<entidade>>` diz quem é o dono sem precisar de "
              "comentário, e não há um `delete` em todo o Deriva. O par com o "
              "destrutor virtual é o que amarra as Aulas 11 e 12."),
    dict(id="transferir-posse", aula=12, arquivo="exemplos/deriva/src/mundo.cpp",
         de="std::unique_ptr<entidade> mundo::retirar_de", ate="}",
         legenda="src/mundo.cpp · devolver posse é devolver o ponteiro",
         nota="O retorno é `[[nodiscard]]` porque ignorá-lo destrói o objeto na hora. "
              "Compare com `primeira_com`, que devolve ponteiro cru: ali é observação, "
              "e o tipo tem de dizer a diferença."),

    # ---- Aula 13 · posse compartilhada ------------------------------------
    dict(id="shared-e-weak", aula=13, arquivo="exemplos/deriva/src/estacao.cpp",
         de="void no_estacao::ligar", ate="}", comentario=True,
         legenda="src/estacao.cpp · a assimetria que impede o ciclo",
         nota="Duas linhas, e é nelas que está a lição: a ligação para frente possui "
              "e a de volta observa. Trocar `volta_` por `shared_ptr` fecha o ciclo e "
              "prende 160 bytes por par de nós."),
    dict(id="weak-obriga-perguntar", aula=13,
         arquivo="exemplos/deriva/testes/test_estacao.cpp",
         de='TEST_CASE("weak_ptr obriga a perguntar', ate="}", comentario=True,
         legenda="testes/test_estacao.cpp · weak_ptr não pendura",
         nota="`lock()` devolve `nullptr` quando o objeto morreu. É a pergunta "
              "obrigatória que torna o ponteiro pendurado impossível - e é o que "
              "`shared_ptr` na volta impediria de acontecer, porque o objeto nunca "
              "morreria."),

    # ---- Aula 14 · movimento e a regra dos cinco --------------------------
    dict(id="origem-esvazia", aula=14,
         arquivo="exemplos/deriva/testes/test_move_string.cpp",
         de='TEST_CASE("nesta implementacao a origem esvazia nos quatro casos")',
         ate="}", comentario=True,
         legenda="testes/test_move_string.cpp · a origem, nos quatro casos",
         nota="Curta e longa, construção e atribuição: a origem esvazia nos quatro. É "
              "justamente porque `REQUIRE(origem.empty())` PASSA aqui que o folclore "
              "sobrevive e o erro embarca - o padrão promete estado válido, não vazio."),
    dict(id="copia-ou-ponteiro", aula=14,
         arquivo="exemplos/deriva/testes/test_move_string.cpp",
         de='TEST_CASE("move de string curta COPIA bytes; de string longa transfere ponteiro")',
         ate="}", comentario=True,
         legenda="testes/test_move_string.cpp · a diferença que se reproduz",
         nota="Curta: o endereço do destino é NOVO, porque oito bytes foram copiados - "
              "não havia ponteiro a roubar. Longa: o mesmo ponteiro de heap troca de "
              "dono, e nenhum byte de conteúdo se move."),
    dict(id="move-de-mapa", aula=14, arquivo="exemplos/deriva/src/mapa.cpp",
         de="mapa::mapa(mapa&& o) noexcept", ate="}", comentario=True,
         legenda="src/mapa.cpp · o construtor de movimento",
         nota="`noexcept` não é decoração: `std::vector<mapa>` só usa o movimento ao "
              "realocar se ele for `noexcept`; sem a palavra, copia."),
    dict(id="move-transfere-buffer", aula=14,
         arquivo="exemplos/deriva/testes/test_mapa.cpp",
         de='TEST_CASE("mover um mapa transfere o buffer', ate="}", comentario=True,
         legenda="testes/test_mapa.cpp · o que o movimento muda",
         nota="Mover devolve o MESMO endereço de buffer; copiar devolve um novo. E o "
              "contador não distingue os dois, porque conta objetos e não alocações."),

    # ---- Aula 15 · operadores ---------------------------------------------
    dict(id="operadores-livres", aula=15,
         arquivo="exemplos/deriva/include/deriva/vetor2.hpp",
         de="[[nodiscard]] constexpr vetor2 operator+(", ate="}", comentario=True,
         legenda="include/deriva/vetor2.hpp · binário é função livre",
         nota="O composto é membro porque modifica o objeto da esquerda; o binário é "
              "livre porque trata os dois lados igual. Escrever `+` em termos de `+=` "
              "é a forma que não duplica a regra."),
    dict(id="par-const-nao-const", aula=15,
         arquivo="exemplos/deriva/include/deriva/mapa.hpp",
         de="[[nodiscard]] const celula& operator[](vetor2 p) const",
         ate="[[nodiscard]] celula& operator[](vetor2 p) { return grade_.em(p); }",
         comentario=True,
         legenda="include/deriva/mapa.hpp · o par que existe por uma razão",
         nota="Uma sobrecarga só, devolvendo referência não-const, permitiria escrever "
              "através de um mapa constante; devolvendo referência const, impediria "
              "escrever em qualquer um."),

    # ---- Aula 16 · testes e replay ----------------------------------------
    dict(id="fov-puro", aula=16, arquivo="exemplos/deriva/src/fov.cpp",
         de="std::vector<vetor2> linha(vetor2 a, vetor2 b) {", ate="}",
         comentario=True,
         legenda="src/fov.cpp · Bresenham em inteiros",
         nota="Nenhum ponto flutuante, nenhum arredondamento dependente de "
              "plataforma. É essa propriedade que o replay compra, e é por isso que o "
              "campo de visão é o PRIMEIRO alvo dos testes e não o último: função "
              "pura se testa sem montar o mundo."),

    # ---- Aula 17 · o diamante ---------------------------------------------
    dict(id="diamante-medido", aula=17,
         arquivo="exemplos/deriva/include/deriva/diamante.hpp",
         de="static_assert(sizeof(nucleo) == 16", ate="", comentario=True,
         legenda="include/deriva/diamante.hpp · os números do diamante",
         nota="Contraria a intuição, e por isso está medido: a herança virtual é a "
              "MAIOR das três formas, 48 bytes contra 40 da duplicada. O que ela "
              "compra não é tamanho, é correção - um campo em vez de dois ambíguos."),
    dict(id="interface-pura", aula=17,
         arquivo="exemplos/deriva/include/deriva/reparadora.hpp",
         de="class i_reparavel {", ate="};", comentario=True,
         legenda="include/deriva/reparadora.hpp · o caso fácil",
         nota="Interface pura é o único uso de herança múltipla que este material "
              "recomenda sem ressalva: nenhum dado, então não há o que duplicar, e o "
              "diamante que ela formaria é inofensivo."),

    # ---- Aula 18 · RTTI ---------------------------------------------------
    dict(id="cadeia-dynamic-cast", aula=18, arquivo="exemplos/deriva/src/inspetor.cpp",
         de="std::string inspecionar(const entidade& e) {", ate="}", comentario=True,
         legenda="src/inspetor.cpp · a ordem da cadeia é obrigatória",
         nota="A `sonda_reparadora` também É `sonda`, então testá-la depois nunca "
              "aconteceria. Perguntar pelo tipo mais derivado primeiro é a armadilha "
              "número um - e é o argumento de que essa cadeia deveria ser uma função "
              "virtual."),
    dict(id="cast-para-interface", aula=18, arquivo="exemplos/deriva/src/inspetor.cpp",
         de="std::string listar_reparadoras(const mundo& m) {", ate="}",
         legenda="src/inspetor.cpp · perguntar por capacidade, não por tipo",
         nota="`dynamic_cast` para a interface, e não para a classe concreta: é a "
              "pergunta certa, porque o que interessa é a capacidade. Este é o único "
              "lugar do Deriva onde `dynamic_cast` é a resposta e não o sintoma."),

    # ---- Aula 11 · o custo do vptr ---------------------------------------
    dict(id="custo-do-vptr", aula=11,
         arquivo="exemplos/deriva/include/deriva/leiaute.hpp",
         de="struct entidade_simples {", ate="static_assert(sizeof(drone_com_carga) == 24",
         comentario=True,
         legenda="include/deriva/leiaute.hpp · quanto custa o vptr",
         nota="8 bytes por OBJETO, não por classe. E o custo não desaparece quando "
              "a derivada acrescenta dado: ele se soma - 8 do vptr, 8 da posição, "
              "4 da carga, 4 de padding."),

    # ---- Aula 19 · templates, if constexpr e CRTP -------------------------
    dict(id="crtp-contador", aula=19,
         arquivo="exemplos/deriva/include/deriva/contador_crtp.hpp",
         de="class contador_de_instancias {", ate="};",
         comentario=True,
         legenda="include/deriva/contador_crtp.hpp · o contador generalizado",
         nota="O parâmetro `T` é o truque: cada instanciação é um TIPO diferente, "
              "logo tem os seus próprios `vivos`. Herança comum compartilharia um "
              "contador só entre todas as derivadas, que é exatamente o erro que o "
              "contador na base cometeria."),
    dict(id="if-constexpr-poda", aula=19,
         arquivo="exemplos/deriva/include/deriva/grade_generica.hpp",
         de="[[nodiscard]] std::string despejar() const {", ate="}",
         comentario=True,
         legenda="include/deriva/grade_generica.hpp · if constexpr no despejo",
         nota="Com `if` comum os três ramos teriam de ser válidos para todo `T`, e "
              "`c.glifo` não existe em `int` - não compilaria. É a diferença que "
              "`if constexpr` faz, e o motivo pelo qual ele substitui SFINAE."),
    dict(id="static-assert-proprio", aula=19,
         arquivo="exemplos/deriva/include/deriva/grade_generica.hpp",
         de="static_assert(!std::is_same_v<T, bool>", ate="",
         comentario=True,
         legenda="include/deriva/grade_generica.hpp · a mensagem é a nossa",
         nota="`std::vector<bool>` empacota bits e devolve proxy, não `bool&`. Sem "
              "este `static_assert`, o estudante leria \"cannot bind non-const lvalue "
              "reference to an rvalue\" vindo de dentro da biblioteca."),

    # ---- Aula 20 · erros --------------------------------------------------
    dict(id="tres-formas-de-erro", aula=20, arquivo="exemplos/deriva/include/deriva/erro.hpp",
         de="using resultado_de_mapa", ate="", comentario=True,
         legenda="include/deriva/erro.hpp · optional, variant ou exceção",
         nota="Três formas de dizer que algo não deu certo, e a escolha está no tipo: "
              "`optional` para ausência, `variant` para erro esperado com informação, "
              "exceção para o que rompe a operação."),
    dict(id="garantia-forte-barata", aula=20, arquivo="exemplos/deriva/src/erro.cpp",
         de="resultado_de_mapa interpretar(", ate="}", comentario=True,
         legenda="src/erro.cpp · validar antes de construir",
         nota="A garantia forte é barata aqui porque nada é alocado até se saber que o "
              "texto serve - não há o que desfazer. É por isso que a leitura é "
              "separada da aplicação."),

    # ---- Aula 21 · STL e lambdas ------------------------------------------
    dict(id="clamp-no-lugar", aula=21, arquivo="exemplos/deriva/src/inventario.cpp",
         de="inventario::inventario(int capacidade) noexcept",
         ate=": capacidade_(std::clamp(capacidade, 0, 999)) {}",
         comentario=True,
         legenda="src/inventario.cpp · std::clamp em vez de min/max aninhado",
         nota="`clamp` devolve **referência**, e é a armadilha dele: não o alimente "
              "com temporário guardando o resultado por referência. Aqui o valor é "
              "copiado para um `int`, e é isso que o torna seguro."),
    dict(id="erase-remove", aula=21, arquivo="exemplos/deriva/src/inventario.cpp",
         de="std::size_t inventario::descartar_se(", ate="}", comentario=True,
         legenda="src/inventario.cpp · erase-remove",
         nota="`remove_if` empurra para o fim e devolve o novo fim; `erase` corta. Em "
              "C++20 seria `std::erase_if`, uma chamada só - e é por isso que o "
              "material nomeia o idioma antigo em vez de fingir que ele é natural."),
    dict(id="sort-deterministico", aula=21, arquivo="exemplos/deriva/src/inventario.cpp",
         de="void inventario::ordenar_por_massa()", ate="}",
         legenda="src/inventario.cpp · o desempate que o replay exige",
         nota="`std::sort` é instável. Sem o desempate pelo rótulo, a ordem entre "
              "massas iguais seria a que o algoritmo quisesse, e o despejo deixaria de "
              "ser determinístico."),

    # ---- Aula 22 · concorrência -------------------------------------------
    dict(id="o-que-se-compartilha", aula=22,
         arquivo="exemplos/deriva/include/deriva/fila_de_comandos.hpp",
         de="class fila_de_comandos {", ate="};", comentario=True,
         legenda="include/deriva/fila_de_comandos.hpp · a fila é a única fronteira",
         nota="O `mundo` continua sendo de uma thread só. O que atravessa a fronteira "
              "são comandos, um por vez, protegidos - e é o oposto da tentação de "
              "deixar as duas threads mexerem no mundo."),
    dict(id="wait-com-predicado", aula=22,
         arquivo="exemplos/deriva/src/fila_de_comandos.cpp",
         de="std::optional<std::string> fila_de_comandos::puxar()", ate="}",
         legenda="src/fila_de_comandos.cpp · o predicado não é conveniência",
         nota="Sem o predicado no `wait`, um despertar espúrio faria a thread seguir "
              "com a fila vazia. E notificar fora da região travada economiza uma ida "
              "e volta no escalonador."),
    dict(id="teste-que-nao-afirma", aula=22,
         arquivo="exemplos/deriva/testes/test_concorrencia.cpp",
         de='TEST_CASE("com scoped_lock a conta fecha sempre', ate="}",
         comentario=True,
         legenda="testes/test_concorrencia.cpp · o que não se pode afirmar",
         nota="A primeira versão deste teste exigia que a corrida se manifestasse, e "
              "falhou no portão - oito execuções de dez não perdem nada. Teste que "
              "depende de comportamento indefinido é teste instável, e instável é pior "
              "que ausente: treina a equipe a reexecutar até passar."),

    # ---- Aula 23 · serialização -------------------------------------------
    dict(id="versao-primeiro", aula=23, arquivo="exemplos/deriva/src/partida.cpp",
         de="std::string partida::serializar() const {", ate="}", comentario=True,
         legenda="src/partida.cpp · a versão é a primeira linha",
         nota="Quem lê precisa saber com que regras ler antes de ler qualquer outra "
              "coisa. Ordem de linha fixa é o que permite comparar dois saves com "
              "`diff`, e é a mesma razão do replay."),
    dict(id="compatibilidade-regressiva", aula=23,
         arquivo="exemplos/deriva/testes/test_partida.cpp",
         de='TEST_CASE("o leitor v2 abre uma partida v1")', ate="}", comentario=True,
         legenda="testes/test_partida.cpp · o padrão do membro responde pelo campo ausente",
         nota="Sem esse padrão, a partida antiga carregaria com zero de energia e a "
              "sonda apareceria morta - o defeito clássico de migração de formato."),
    dict(id="most-vexing-parse", aula=23, arquivo="exemplos/deriva/src/partida.cpp",
         de="std::istringstream is{std::string(texto)};", ate="",
         comentario=True,
         legenda="src/partida.cpp · chaves, e não parênteses",
         nota="`std::istringstream is(std::string(texto));` é a *most vexing parse*: o "
              "compilador lê a DECLARAÇÃO de uma função. A inicialização uniforme da "
              "Aula 03 não tem essa ambiguidade, e é por isso que o material a "
              "recomenda desde o começo."),

    # ---- Aula 24 · SOLID --------------------------------------------------
    dict(id="dip-apresentacao", aula=24,
         arquivo="exemplos/deriva/include/deriva/apresentacao.hpp",
         de="class i_apresentacao {", ate="};", comentario=True,
         legenda="include/deriva/apresentacao.hpp · DIP, a interface do render",
         nota="O núcleo depende desta abstração, e não de terminal nem de Qt. Antes da "
              "refatoração o `mundo` escrevia direto em `std::cout`, e trocar a saída "
              "significava editá-lo."),
    dict(id="god-class", aula=24,
         arquivo="exemplos/deriva/variantes/v2.6-antes/mundo_god_class.cpp",
         de="class mundo {", ate="};", comentario=True, quebrado=True,
         legenda="v2.6-antes · sete responsabilidades · CAÇA AO BUG 3",
         nota="Compila sem aviso, roda, e faz tudo o que a refatorada faz. O defeito "
              "não é funcional: são sete motivos independentes para editar o mesmo "
              "arquivo. A caça não é achar o erro, é refatorar e provar pelo replay "
              "que a saída não mudou."),
    dict(id="ocp-turno-nao-conhece", aula=24,
         arquivo="exemplos/deriva/src/mundo.cpp",
         de="void mundo::turno() {", ate="}", comentario=True,
         legenda="src/mundo.cpp · o turno não conhece as derivadas",
         nota="Aberto para extensão e fechado para modificação, e a prova é negativa: "
              "acrescentar uma entidade nova não muda uma linha deste arquivo, porque "
              "o `mundo` guarda `vector<unique_ptr<entidade>>` e chama `agir` pela "
              "base. O índice em lugar do iterador não é estilo: `agir` pode "
              "acrescentar entidade, e isso invalidaria o iterador."),
    dict(id="desfazer-prova-invariancia", aula=24,
         arquivo="exemplos/deriva/testes/test_padroes.cpp",
         de='TEST_CASE("desfazer em cadeia volta ao estado inicial")', ate="}",
         comentario=True,
         legenda="testes/test_padroes.cpp · o despejo byte a byte como oráculo",
         nota="O mesmo critério que a caça ao bug 3 cobra: `diff` vazio é a única "
              "evidência aceita, e teste verde não basta - os testes passam nas duas "
              "versões."),

    # ---- Aula 25 · padrões ------------------------------------------------
    dict(id="strategy-por-lambda", aula=25, arquivo="exemplos/deriva/src/apresentacao.cpp",
         de="estrategia estrategia_de_patrulha(vetor2 rumo) {", ate="}",
         comentario=True,
         legenda="src/apresentacao.cpp · Strategy é função, não hierarquia",
         nota="Uma operação e nenhum estado: é função, e `std::function` a guarda. A "
              "captura é por valor, e é obrigatório - a lambda sobrevive à chamada que "
              "a criou, e capturar por referência deixaria referência pendurada. É a "
              "armadilha do `string_view` da Aula 03 noutra roupa."),
    dict(id="command-com-desfazer", aula=25,
         arquivo="exemplos/deriva/include/deriva/apresentacao.hpp",
         de="class mover_sonda final : public i_comando {", ate="};", comentario=True,
         legenda="include/deriva/apresentacao.hpp · Command guarda de onde saiu",
         nota="O que se ganha não é elegância, é o desfazer - e um `switch` não tem "
              "onde guardar de onde a sonda veio."),
    dict(id="factory-por-glifo", aula=25, arquivo="exemplos/deriva/src/apresentacao.cpp",
         de="std::unique_ptr<entidade> criar_por_glifo(", ate="}", comentario=True,
         legenda="src/apresentacao.cpp · Factory, e a tabela num lugar só",
         nota="Acrescentar entidade nova é acrescentar um caso aqui, e nada no "
              "carregador de mapa muda. Na variante `v2.6-antes` a mesma tabela "
              "aparece três vezes, com `dynamic_cast`."),
    dict(id="composite-mochila", aula=25, arquivo="exemplos/deriva/src/inventario.cpp",
         de="int mochila::massa() const {", ate="}",
         legenda="src/inventario.cpp · Composite, e o inventário não sabe a diferença",
         nota="A mochila responde `massa` somando o que tem dentro, e o inventário a "
              "trata como qualquer peça. Cuidado com o ciclo: mochila dentro de si "
              "mesma é o vazamento da Aula 13 noutra forma."),

    # ---- Aula 26 · Qt ------------------------------------------------------
    dict(id="posse-no-qt", aula=26, arquivo="exemplos/deriva/qt/janela.hpp",
         de="class janela : public QMainWindow {", ate="};", comentario=True,
         legenda="qt/janela.hpp · posse no Qt é a exceção declarada",
         nota="`QObject` tem árvore de pais, e o pai destrói os filhos: passar um "
              "`QWidget*` cru ao construtor do filho ENTREGA a posse. `unique_ptr` "
              "sobre `QWidget` com pai é dupla liberação. É a exceção à regra da Aula "
              "12, e ela é declarada, não escondida."),
    dict(id="nucleo-nao-muda", aula=26, arquivo="exemplos/deriva/qt/main_qt.cpp",
         de="int main(int argc, char** argv) {", ate="}", comentario=True,
         legenda="qt/main_qt.cpp · o argumento inteiro da aula",
         nota="Nenhuma linha do núcleo mudou para esta janela existir, e isso só é "
              "verdade porque a v2.6 extraiu `i_apresentacao`. É a diferença entre "
              "separação demonstrada e separação afirmada."),

    # ---- Aula 16 · replay --------------------------------------------------
    dict(id="sorteio-deterministico", aula=16, arquivo="exemplos/deriva/src/main.cpp",
         de="class sorteio {", ate="};", comentario=True,
         legenda="src/main.cpp · o sorteio que não sorteia",
         nota="Não é `std::mt19937` nem `std::random_device`: precisa ser "
              "reproduzível byte a byte em qualquer máquina, porque é sobre isso "
              "que o replay se apoia. Aleatoriedade de verdade seria pior aqui."),
    dict(id="portao-replay", aula=16, arquivo="exemplos/deriva/Makefile",
         de="replay:", ate="", comentario=True,
         legenda="Makefile · o portão de replay",
         nota="Semente fixa, roteiro gravado, `diff` contra o esperado. Regravar o "
              "esperado é uma DECISÃO - numa refatoração, é justamente o que não "
              "se pode fazer."),

    # ---- declarados a partir do levantamento dos escribas -----------------
    # As âncoras abaixo foram conferidas contra o arquivo antes de entrarem.

    dict(id="oo-fecha-seis", aula=1,
         arquivo="exemplos/deriva/testes/test_comparativo.cpp",
         de='TEST_CASE("a versao OO fecha seis das sete maneiras de errar")', ate="}",
         comentario=True,
         legenda="testes/test_comparativo.cpp · sete contra uma",
         nota="As seis maneiras de errar que somem não somem por disciplina de quem "
              "escreve: somem porque o compilador passou a impedi-las."),
    dict(id="invariante-em-compilacao", aula=1,
         arquivo="exemplos/deriva/testes/test_comparativo.cpp",
         de='TEST_CASE("em C++, a dimensao e invariante, e o tipo diz isso")',
         ate='SUCCEED("a invariante e garantida em compilacao, nao por lembranca");',
         legenda="testes/test_comparativo.cpp · o campo público virou invariante",
         nota="Em C, `largura` é pública e mexer nela corrompe a indexação. Aqui a "
              "garantia é de compilação, e não de lembrança."),
    dict(id="cmake-do-deriva", aula=2, arquivo="exemplos/deriva/CMakeLists.txt",
         de="cmake_minimum_required(VERSION 3.16)",
         ate='option(DERIVA_COM_QT     "Segundo front-end em Qt6 (Aula 26)" OFF)',
         legenda="CMakeLists.txt · o topo, com as quatro opções",
         nota="`CXX_EXTENSIONS OFF` é o que recusa `-std=gnu++17`: código que só "
              "compila com extensão não é C++17. E `DERIVA_SANITIZERS` nasce "
              "desligada, porque o laboratório não os tem."),
    dict(id="lista-de-init-cpp", aula=7, arquivo="exemplos/deriva/src/grade.cpp",
         de="grade::grade(int largura, int altura)",
         ate="celulas_(static_cast<std::size_t>(largura_) * static_cast<std::size_t>(altura_)) {}",
         comentario=True,
         legenda="src/grade.cpp · a lista que constrói uma vez só",
         nota="`celulas_` é construído com o tamanho certo de uma vez. Atribuir no "
              "corpo o construiria vazio antes e o redimensionaria depois."),
    dict(id="this-em-uso", aula=7, arquivo="exemplos/deriva/src/mapa.cpp",
         de="mapa& mapa::operator=(const mapa& o) {",
         ate="return *this;  // o contador não muda: nenhum objeto nasceu nem morreu",
         legenda="src/mapa.cpp · os dois usos de `this` que o Deriva tem",
         nota="`this != &o` para recusar a autoatribuição, e `return *this` para "
              "encadear. São os dois únicos lugares em que `this` aparece explícito "
              "em todo o projeto - fora deles, ele é implícito e escrevê-lo é ruído."),
    dict(id="par-em-declarado", aula=7,
         arquivo="exemplos/deriva/include/deriva/grade.hpp",
         de="[[nodiscard]] const celula& em(vetor2 p) const;",
         ate="[[nodiscard]] celula& em(vetor2 p);", comentario=True,
         legenda="include/deriva/grade.hpp · o par de sobrecargas",
         nota="`[[nodiscard]]` nas duas, e `const` só na primeira: é a versão "
              "não-const que existe para deixar escrever, e é por isso que ela não "
              "pode ser const."),
    # A quarta forma de `const` - o OBJETO const - não aparecia em trecho
    # nenhum da Aula 07: `par-em-declarado` mostra as duas assinaturas, e
    # nada mostrava a constância do objeto escolhendo entre elas. O site
    # tinha aí um bloco digitado, do sistema-base antigo, com quatro formas
    # de `const` que ninguém compilava. Esta é a forma que o ctest roda.
    dict(id="objeto-const", aula=7,
         arquivo="exemplos/deriva/testes/test_grade.cpp",
         de='TEST_CASE("grade conhece seus limites")', ate="}",
         legenda="testes/test_grade.cpp · o objeto const, e o que ele alcança",
         nota="`const grade g(20, 10)` só deixa chamar método `const`, e todas as "
              "chamadas aqui o são. Trocar uma delas pela sobrecarga "
              "não-const de `em()` faz este teste deixar de compilar - e é essa "
              "recusa, e não a palavra no cabeçalho, que é a garantia."),
    dict(id="contador-em-uso", aula=7, arquivo="exemplos/deriva/src/mapa.cpp",
         de="mapa::mapa(std::string nome, int largura, int altura)",
         ate="mapa::~mapa() { --contador_mapa::vivos; }",
         legenda="src/mapa.cpp · o contador em uso",
         nota="`++vivos` e `++criados` no construtor, `--vivos` no destrutor. A "
              "declaração `inline static` está no cabeçalho, e é ela que dispensa a "
              "definição num .cpp."),
    dict(id="ordem-simples", aula=8,
         arquivo="exemplos/deriva/testes/test_ciclo_de_vida.cpp",
         de='TEST_CASE("a ordem de destruicao e a inversa da de construcao")',
         ate='"-a\\n");',
         legenda="testes/test_ciclo_de_vida.cpp · a ordem, afirmada linha por linha",
         nota="Dois objetos no escopo externo, um no interno, e a saída comparada "
              "texto a texto. Nenhuma linha de código pediu essa ordem."),
    dict(id="forma-longa-copia", aula=9, arquivo="exemplos/deriva/src/mapa.cpp",
         de="mapa::mapa(const mapa& o)", ate="}", comentario=True,
         legenda="src/mapa.cpp · a forma longa da regra do três",
         nota="O incremento na cópia é obrigatório: sem ele o destrutor da cópia "
              "decrementaria algo que ninguém incrementou, e `vivos` fecharia "
              "negativo - o contador passaria a mentir na direção que ninguém "
              "desconfia."),
    dict(id="forma-curta-delete", aula=9,
         arquivo="exemplos/deriva/include/deriva/terminal_bruto.hpp",
         de="class terminal_bruto {", ate="};", comentario=True,
         legenda="include/deriva/terminal_bruto.hpp · a forma curta",
         nota="Duas linhas de `= delete`, e a regra do três está cumprida. Há "
              "exatamente um terminal, e posse de recurso único não se duplica."),

    dict(id="despacho-em-tres", aula=11,
         arquivo="exemplos/deriva/testes/test_entidade.cpp",
         de='TEST_CASE("o despacho virtual escolhe pelo tipo do OBJETO")', ate="}",
         comentario=True,
         legenda="testes/test_entidade.cpp · três objetos, um tipo de ponteiro",
         nota="A saída é `@d!`, e não `eee`. Os três ponteiros são `entidade*`, e "
              "quem decidiu foi o objeto."),
    dict(id="override-e-final", aula=11,
         arquivo="exemplos/deriva/include/deriva/entidade.hpp",
         de="class drone final : public entidade {", ate="};", comentario=True,
         legenda="include/deriva/entidade.hpp · `final` na folha, `override` nas sobrescritas",
         nota="`virtual` não se repete na derivada: `override` já diz que sobrescreve, "
              "e diz melhor, porque o compilador o verifica."),
    dict(id="abstrata-afirmada", aula=11,
         arquivo="exemplos/deriva/testes/test_entidade.cpp",
         de='TEST_CASE("entidade e abstrata, e o compilador diz isso")', ate="}",
         comentario=True,
         legenda="testes/test_entidade.cpp · a abstração, afirmada",
         nota="`is_abstract_v`, `!is_constructible_v`, `has_virtual_destructor_v` e "
              "`!is_copy_constructible_v`. Quatro decisões de projeto que o "
              "compilador guarda."),
    dict(id="dois-donos", aula=13, arquivo="exemplos/deriva/testes/test_estacao.cpp",
         de='TEST_CASE("posse compartilhada: dois donos, e nenhum destroi sozinho")',
         ate="}", comentario=True,
         legenda="testes/test_estacao.cpp · o requisito que shared_ptr atende",
         nota="A contagem vai a 1, sobe a 3 e volta a 1 no mesmo escopo. É o requisito "
              "que `unique_ptr` não atende: a eclusa pertence aos dois corredores, e "
              "nenhum dos dois pode destruí-la sozinho."),
    dict(id="nrvo", aula=14, arquivo="exemplos/deriva/src/mapa.cpp",
         de="mapa m(std::move(nome), static_cast<int>(largura),", ate="return m;",
         legenda="src/mapa.cpp · variável nomeada devolvida",
         nota="É o caso do NRVO: o compilador pode construir `m` diretamente no lugar "
              "do retorno e não copiar nem mover. Ele **pode**, e não é obrigado - a "
              "elisão obrigatória de C++17 vale para prvalue, que este não é."),
    dict(id="parametro-por-valor", aula=14, arquivo="exemplos/deriva/src/mundo.cpp",
         de="entidade& mundo::acrescentar(std::unique_ptr<entidade> e) {", ate="}",
         legenda="src/mundo.cpp · por valor, e depois `std::move`",
         nota="Parâmetro por valor num tipo só-movível é o idioma: quem chama decide "
              "se move ou constrói no lugar, e a função move para dentro do vetor sem "
              "cópia nenhuma."),
    dict(id="cinco-declaradas", aula=14,
         arquivo="exemplos/deriva/include/deriva/mapa.hpp",
         de="// A regra dos cinco, completa (v1.4 · Aula 14).",
         ate="mapa& operator=(mapa&& o) noexcept;",
         legenda="include/deriva/mapa.hpp · as cinco, juntas",
         nota="Declaradas no mesmo lugar, com a razão escrita ao lado. O comentário "
              "registra uma medição que contrariou o que ele mesmo dizia antes."),
    dict(id="move-assign", aula=14, arquivo="exemplos/deriva/src/mapa.cpp",
         de="mapa& mapa::operator=(mapa&& o) noexcept {", ate="}",
         legenda="src/mapa.cpp · a atribuição de movimento",
         nota="Ela não toca no contador, e o construtor toca: atribuir não cria nem "
              "destrói ninguém. É a assimetria que mais confunde na regra dos cinco."),
    dict(id="operadores-simetricos", aula=15,
         arquivo="exemplos/deriva/testes/test_operadores.cpp",
         de='TEST_CASE("os operadores de vetor2 sao simetricos e constexpr")', ate="}",
         legenda="testes/test_operadores.cpp · simetria, medida",
         nota="`3 * v` e `v * 3` funcionam os dois, e é isso que função livre compra. "
              "Membro aceitaria só um dos lados."),
    dict(id="compostos-membros", aula=15,
         arquivo="exemplos/deriva/include/deriva/vetor2.hpp",
         de="constexpr vetor2& operator+=(const vetor2& o) noexcept {", ate="}",
         comentario=True,
         legenda="include/deriva/vetor2.hpp · o composto é membro",
         nota="Ele modifica o objeto da esquerda, e por isso é membro. O binário livre "
              "é escrito em termos dele, e assim a regra existe num lugar só."),
    dict(id="operator-saida", aula=15, arquivo="exemplos/deriva/src/mapa.cpp",
         de="std::ostream& operator<<(std::ostream& os, const mapa& m) {", ate="}",
         legenda="src/mapa.cpp · `operator<<` é função livre",
         nota="O lado esquerdo é o fluxo, e o fluxo não é nosso. Duas linhas sobre "
              "`despejar()`, devolvendo a referência para encadear."),
    dict(id="catch2-system", aula=16, arquivo="exemplos/deriva/CMakeLists.txt",
         de="  FetchContent_Declare(Catch2", ate="  catch_discover_tests(testes)",
         legenda="CMakeLists.txt · Catch2 como SYSTEM, com tag fixa",
         nota="`SYSTEM` para que o aviso da dependência não conte no portão, e "
              "`GIT_TAG` fixo para que a suíte não mude de comportamento sem que "
              "ninguém tenha mexido nela."),
    dict(id="teste-como-especificacao", aula=16,
         arquivo="exemplos/deriva/testes/test_grade.cpp",
         de='TEST_CASE("grade conhece seus limites")',
         ate='REQUIRE_THROWS_AS(grade(5, -1), std::invalid_argument);',
         legenda="testes/test_grade.cpp · o teste como especificação",
         nota="Ele não procura defeito: ele diz o que a classe promete. Lido de cima a "
              "baixo, é a documentação de `grade` - e é executável."),
    dict(id="fronteiras-optional", aula=16,
         arquivo="exemplos/deriva/testes/test_mapa.cpp",
         de='TEST_CASE("ausencia de resultado nao e excecao")', ate="}",
         legenda="testes/test_mapa.cpp · as três fronteiras",
         nota="Vazio, torto e ausente: os três devolvem `optional` vazio. Ausência de "
              "resultado não é exceção, e o tipo diz isso."),
    dict(id="section-refaz-arranjo", aula=16,
         arquivo="exemplos/deriva/testes/test_fov.cpp",
         de='TEST_CASE("a parede e vista e bloqueia o que esta atras")',
         ate="REQUIRE(v.count(vetor2{7, 1}) == 0);",
         legenda="testes/test_fov.cpp · `SECTION` refaz o arranjo em cada ramo",
         nota="O corpo do `TEST_CASE` roda uma vez POR seção, e não uma vez para as "
              "duas: cada ramo entra num mapa recém-montado. É o que torna as seções "
              "independentes, e é a propriedade que se perde ao guardar estado entre "
              "elas."),
    dict(id="tres-formas-diamante", aula=17,
         arquivo="exemplos/deriva/include/deriva/diamante.hpp",
         de="struct nucleo {",
         ate="struct patrulha_composta : movel { sensor_v olho; int rota = 0; };",
         comentario=True,
         legenda="include/deriva/diamante.hpp · as três formas, lado a lado",
         nota="Duplicada, virtual e composta. Os tamanhos estão no fim do arquivo, "
              "afirmados, e contrariam a intuição."),
    dict(id="dois-campos", aula=17, arquivo="exemplos/deriva/testes/test_diamante.cpp",
         de='TEST_CASE("com heranca comum, os dois ramos escrevem em campos diferentes")',
         ate="}", comentario=True,
         legenda="testes/test_diamante.cpp · dois `leituras`, e nenhum é o certo",
         nota="Escrever 7 por um ramo e 9 pelo outro, e ler os dois de volta. Não há "
              "resposta boa para \"qual é o valor\", e é esse o defeito - não o "
              "tamanho."),
    dict(id="um-campo-so", aula=17, arquivo="exemplos/deriva/testes/test_diamante.cpp",
         de='TEST_CASE("com heranca virtual, ha um campo so")', ate="}",
         legenda="testes/test_diamante.cpp · com base virtual, um campo",
         nota="Escrever por um ramo e ler pelo outro devolve o mesmo valor. É isto que "
              "se compra com a indireção, e não bytes - a forma virtual é a maior das "
              "três."),
    dict(id="ordem-das-bases", aula=17,
         arquivo="exemplos/deriva/src/reparadora.cpp",
         de="sonda_reparadora::sonda_reparadora(vetor2 pos, int energia)", ate="}",
         legenda="src/reparadora.cpp · a ordem das bases é a da declaração",
         nota="Bases antes de membros, e bases na ordem em que a lista de HERANÇA as "
              "declara - não na ordem em que a lista de inicialização as menciona. "
              "Trocar a ordem na lista de inicialização não muda a ordem de execução, e "
              "o `-Wreorder`, que o `-Wall` do portão já liga, avisa quando as duas "
              "divergem."),
    dict(id="reparadora-fecha-em-zero", aula=17,
         arquivo="exemplos/deriva/testes/test_diamante.cpp",
         de='TEST_CASE("a ordem de construcao e destruicao da reparadora fecha em zero")',
         ate="REQUIRE(sonda::vivos == 0);",
         legenda="testes/test_diamante.cpp · a destruição percorre o inverso exato",
         nota="Uma `sonda_reparadora` conta nos DOIS contadores, porque ela também é "
              "uma `sonda`, e os dois voltam a zero no fim do escopo. É a prova de que "
              "nenhum destrutor da cadeia deixou de rodar."),
    dict(id="laco-sem-tipo", aula=18, arquivo="exemplos/deriva/src/mundo.cpp",
         de="void mundo::turno() {", ate="}", comentario=True,
         legenda="src/mundo.cpp · o laço que não nomeia tipo concreto",
         nota="Nenhum `dynamic_cast`, nenhum `typeid`, nenhum `switch`. É o "
              "polimorfismo funcionando - e o contraste com o inspetor da mesma aula, "
              "onde perguntar o tipo é a tarefa."),
    dict(id="render-polimorfico", aula=18, arquivo="exemplos/deriva/src/mundo.cpp",
         de="std::string mundo::despejar() const {", ate="}",
         legenda="src/mundo.cpp · o render, também sem nome de tipo",
         nota="Cada entidade desenha o próprio glifo por chamada virtual. Acrescentar "
              "uma entidade nova não toca nesta função."),

    # ---- levantamento da Unidade III --------------------------------------
    dict(id="grade-generica-classe", aula=19,
         arquivo="exemplos/deriva/include/deriva/grade_generica.hpp",
         de="class grade_de : public contador_de_instancias<grade_de<T>> {",
         ate='static_assert(!std::is_reference_v<T>, "grade de referencias nao existe");',
         comentario=True,
         legenda="include/deriva/grade_generica.hpp · a classe e as restrições",
         nota="`grade_de<T>` CONVIVE com a `grade` não genérica em vez de substituí-la: "
              "generalizar não é obrigação retroativa. E o `static_assert` na "
              "definição, não no uso, é o que faz a mensagem de erro ser a nossa."),
    dict(id="grade-generica-acesso", aula=19,
         arquivo="exemplos/deriva/include/deriva/grade_generica.hpp",
         de="grade_de(int largura, int altura)",
         ate="[[nodiscard]] T& em(vetor2 p) { return celulas_[indice(p)]; }",
         legenda="include/deriva/grade_generica.hpp · construtor e o par de acesso",
         nota="A validação continua na lista de inicialização, como na versão não "
              "genérica - e o par const/não-const de `em()` é o mesmo padrão do Cap. 7, "
              "agora sobre `T`."),
    dict(id="crtp-nao-cresce", aula=19,
         arquivo="exemplos/deriva/include/deriva/grade_generica.hpp",
         de="using grade_de_celulas",
         ate='"o contador por CRTP nao aumenta o objeto");', comentario=True,
         legenda="include/deriva/grade_generica.hpp · o CRTP não custa byte",
         nota="Base vazia, e o compilador a otimiza. É a diferença entre polimorfismo "
              "estático e dinâmico, afirmada no `sizeof`."),
    dict(id="raiz-de-erro", aula=20, arquivo="exemplos/deriva/include/deriva/erro.hpp",
         de="class erro_de_deriva : public std::runtime_error {", ate="};",
         comentario=True,
         legenda="include/deriva/erro.hpp · a raiz, e por que não std::exception",
         nota="`runtime_error` já guarda a mensagem e resolve o `what()`. Herdar de "
              "`std::exception` e guardar uma `std::string` membro esconde uma "
              "armadilha: se a cópia da exceção lançar durante o desenrolar, o "
              "programa termina."),
    dict(id="duas-folhas-de-erro", aula=20, arquivo="exemplos/deriva/src/erro.cpp",
         de="mapa_invalido::mapa_invalido(", ate="ec_(ec) {}",
         legenda="src/erro.cpp · as duas folhas",
         nota="Cada uma monta a mensagem na base e guarda o dado estruturado ao lado: "
              "quem trata precisa do caminho e do código, e não de uma string para "
              "reanalisar."),
    dict(id="onde-ausencia-vira-erro", aula=20, arquivo="exemplos/deriva/src/erro.cpp",
         de="mapa carregar_ou_lancar(const std::filesystem::path& caminho) {",
         ate="if (ec) throw falha_de_leitura(caminho, ec);", comentario=True,
         legenda="src/erro.cpp · o ponto exato em que ausência deixa de ser optional",
         nota="`mapa::carregar` devolve `optional` para o mesmo arquivo ausente. A "
              "diferença não é capricho: esta função PROMETE devolver um mapa, e "
              "aquela promete responder se há um."),
    dict(id="accumulate-tipo-da-soma", aula=21,
         arquivo="exemplos/deriva/src/inventario.cpp",
         de="int inventario::massa_total() const {", ate="}", comentario=True,
         legenda="src/inventario.cpp · o zero que define o tipo da soma",
         nota="Passar `0.0` daria soma em `double` sem ninguém pedir, e o truncamento "
              "apareceria três capítulos depois."),
    dict(id="count-if-predicado", aula=21, arquivo="exemplos/deriva/src/inventario.cpp",
         de="std::size_t inventario::contar_se(", ate="}",
         legenda="src/inventario.cpp · o predicado vem de fora",
         nota="A função serve sem saber o que se vai perguntar, e é isso que a torna "
              "útil - acrescentar um critério não a edita."),
    dict(id="max-element-fim", aula=21, arquivo="exemplos/deriva/src/inventario.cpp",
         de="const componente* inventario::mais_pesada() const {", ate="}",
         legenda="src/inventario.cpp · o iterador de fim não é elemento",
         nota="`max_element` devolve `end()` quando a faixa é vazia, e desreferenciar "
              "isso é comportamento indefinido. A comparação com `end()` não é "
              "cerimônia."),
    dict(id="duas-threads-deterministico", aula=22,
         arquivo="exemplos/deriva/include/deriva/fila_de_comandos.hpp",
         de="[[nodiscard]] std::string exercitar_fila(int quantos);", ate="",
         comentario=True,
         legenda="include/deriva/fila_de_comandos.hpp · duas threads, saída determinística",
         nota="Concorrência não implica indeterminismo: a fila é FIFO e há um "
              "consumidor só. Com dois consumidores a ordem deixaria de ser garantida, "
              "e o replay não serviria mais."),
    dict(id="produtora-consumidora", aula=22,
         arquivo="exemplos/deriva/src/fila_de_comandos.cpp",
         de="std::string exercitar_fila(int quantos) {", ate="return consumido;",
         legenda="src/fila_de_comandos.cpp · produtora e consumidora",
         nota="A captura por referência é segura porque o `join` acontece antes de o "
              "escopo fechar. Sem ele, seriam referências a objetos destruídos - e o "
              "`join` esquecido é o defeito mais comum de quem começa."),
    dict(id="notificar-fora-da-trava", aula=22,
         arquivo="exemplos/deriva/src/fila_de_comandos.cpp",
         de="void fila_de_comandos::empurrar(std::string comando) {", ate="",
         legenda="src/fila_de_comandos.cpp · notificar fora da região travada",
         nota="Quem acorda tentaria travar de imediato, e acordar antes de destravar "
              "custa uma ida e volta a mais no escalonador. O escopo interno do "
              "`scoped_lock` existe para isso."),
    dict(id="sem-mutex", aula=22,
         arquivo="exemplos/deriva/include/deriva/medida_corrida.hpp",
         de="[[nodiscard]] inline int contar_sem_mutex(int por_thread) {", ate="",
         comentario=True,
         legenda="include/deriva/medida_corrida.hpp · `vivos++` em duas threads",
         nota="Três passos - lê, soma, escreve -, e nenhum deles atômico. É o mesmo "
              "contador da Aula 07, e é ele que perde o incremento."),
    dict(id="com-scoped-lock", aula=22,
         arquivo="exemplos/deriva/include/deriva/medida_corrida.hpp",
         de="[[nodiscard]] inline int contar_com_mutex(int por_thread) {", ate="",
         comentario=True,
         legenda="include/deriva/medida_corrida.hpp · a mesma conta, protegida",
         nota="`std::scoped_lock` é C++17 e aceita mais de um mutex, resolvendo a ordem "
              "de travamento sozinho - o que elimina uma classe inteira de impasse. "
              "Para um mutex só é equivalente ao `lock_guard`, e usar o novo é hábito."),
    dict(id="faixa-e-nao-numero", aula=22,
         arquivo="exemplos/deriva/include/deriva/medida_corrida.hpp",
         de="[[nodiscard]] inline corrida medir(", ate="",
         legenda="include/deriva/medida_corrida.hpp · devolve a faixa, não um número",
         nota="Corrida é comportamento indefinido, e o resultado varia entre execuções. "
              "O que se mede é a distribuição, e é ela a lição: oito execuções de dez "
              "não perderam nada."),
    dict(id="observer-interface", aula=25,
         arquivo="exemplos/deriva/include/deriva/apresentacao.hpp",
         de="class i_observador {", ate="};", comentario=True,
         legenda="include/deriva/apresentacao.hpp · Observer, a interface",
         nota="Antes da refatoração o `mundo` chamava o log direto, abrindo arquivo, e "
              "por isso não dava para testar o log sem mexer no sistema de arquivos."),
    dict(id="observer-em-memoria", aula=25,
         arquivo="exemplos/deriva/include/deriva/apresentacao.hpp",
         de="class registro_em_memoria final : public i_observador {", ate="};",
         legenda="include/deriva/apresentacao.hpp · o observador que substitui o arquivo",
         nota="Vinte linhas, e é o que torna o log verificável. O `mundo` não sabe "
              "quem escuta, e é isso que Observer compra."),
    dict(id="observer-testado", aula=25,
         arquivo="exemplos/deriva/testes/test_padroes.cpp",
         de='TEST_CASE("Observer permite testar o log sem arquivo")', ate="}",
         legenda="testes/test_padroes.cpp · o log, verificado sem arquivo",
         nota="Nenhum caminho, nenhuma permissão, nenhuma limpeza depois. É o teste que "
              "a versão anterior não conseguia ter."),
    dict(id="adaptador-qt", aula=26, arquivo="exemplos/deriva/qt/janela.hpp",
         de="class tela_qt final : public i_apresentacao {", ate="};", comentario=True,
         legenda="qt/janela.hpp · o adaptador, que não é QObject",
         nota="Ele implementa a mesma interface que `apresentacao_em_texto`, e o núcleo "
              "não sabe qual das duas está do outro lado. O widget é guardado como "
              "ponteiro cru porque é observação: a árvore do Qt é a dona."),
    dict(id="posse-na-arvore-do-qt", aula=26, arquivo="exemplos/deriva/qt/janela.cpp",
         de="janela::janela(mundo w, QWidget* pai)", ate="redesenhar();",
         legenda="qt/janela.cpp · `new` com pai ao lado de unique_ptr",
         nota="`new QPlainTextEdit(this)` entrega a posse ao pai, e `unique_ptr` sobre "
              "o adaptador guarda o que é nosso. As duas formas convivem na mesma "
              "função, e a diferença está em quem destrói."),

    # ---- código escrito para fechar os últimos marcadores ------------------
    dict(id="ordem-base-derivada", aula=10,
         arquivo="exemplos/deriva/testes/test_ciclo_de_vida.cpp",
         de='TEST_CASE("a ordem e base, membros, corpo da derivada', ate="}",
         comentario=True,
         legenda="testes/test_ciclo_de_vida.cpp · a ordem, afirmada",
         nota="Base, membros na ordem de declaração, corpo da derivada - e o inverso "
              "exato ao morrer. O par instrumentado é local ao teste: poluir o despejo "
              "que o replay compara custaria a condição 3 do portão."),
    dict(id="corpo-por-ultimo", aula=10,
         arquivo="exemplos/deriva/testes/test_ciclo_de_vida.cpp",
         de='TEST_CASE("o corpo da derivada roda por ultimo', ate="}", comentario=True,
         legenda="testes/test_ciclo_de_vida.cpp · a consequência da ordem",
         nota="Quando o construtor da base roda, a derivada ainda não existe. É por "
              "isso que método virtual chamado dentro do construtor da base chama a "
              "versão DA BASE - o objeto ainda não é do tipo derivado."),
    dict(id="tamanho-dos-ponteiros", aula=12,
         arquivo="exemplos/deriva/include/deriva/medida_posse.hpp",
         de="static_assert(sizeof(std::unique_ptr<int>) == sizeof(int*),", ate="",
         comentario=True,
         legenda="include/deriva/medida_posse.hpp · quanto custa cada ponteiro",
         nota="`unique_ptr` com deletor padrão é um ponteiro e nada mais; deletor vazio "
              "é absorvido pela otimização de base vazia; deletor com estado cobra o "
              "estado. `shared_ptr` é o dobro, porque leva o bloco de controle."),
    dict(id="forward-preserva", aula=14,
         arquivo="exemplos/deriva/include/deriva/encaminhamento.hpp",
         de="template <class T, class... Args>", ate="}", comentario=True,
         legenda="include/deriva/encaminhamento.hpp · encaminhamento perfeito",
         nota="`T&&` num parâmetro dedutível não é referência a rvalue: é universal, e "
              "o colapso de referências faz a mesma assinatura servir para lvalue e "
              "rvalue. Trocar `forward` por `move` moveria SEMPRE, inclusive de um "
              "lvalue que o chamador ainda vai usar."),
    dict(id="forward-medido", aula=14,
         arquivo="exemplos/deriva/testes/test_encaminhamento.cpp",
         de='TEST_CASE("e o lvalue continua chegando como lvalue")', ate="}",
         comentario=True,
         legenda="testes/test_encaminhamento.cpp · a origem segue utilizável",
         nota="É este teste que `std::move` no lugar de `std::forward` quebraria, e a "
              "quebra seria silenciosa: o programa continuaria compilando."),
    dict(id="lsp-violado", aula=24, arquivo="exemplos/deriva/include/deriva/solid.hpp",
         de="class parede_que_lanca final : public obstaculo {", ate="};",
         comentario=True, quebrado=True,
         legenda="include/deriva/solid.hpp · a violação de LSP",
         nota="Compila, e quebra a promessa da base: `mover` promete não lançar. O "
              "sintoma não aparece na parede - aparece em toda função que recebe "
              "`obstaculo&`, escrita antes de a parede existir e correta quando foi "
              "escrita."),
    dict(id="lsp-no-chamador", aula=24,
         arquivo="exemplos/deriva/testes/test_solid.cpp",
         de='TEST_CASE("LSP: a violacao nao aparece na derivada', ate="}",
         comentario=True,
         legenda="testes/test_solid.cpp · LSP se mede no chamador",
         nota="E o pior está na última linha: a caixa JÁ foi movida quando a exceção "
              "subiu. A função deixou o sistema no meio do caminho sem ter feito nada "
              "errado."),
    dict(id="isp-metodo-vazio", aula=24,
         arquivo="exemplos/deriva/include/deriva/solid.hpp",
         de="class so_desenha_gordo final : public i_tudo {", ate="};", comentario=True,
         quebrado=True,
         legenda="include/deriva/solid.hpp · método vazio é a confissão",
         nota="Quem só desenha é obrigado a implementar salvar e reparar, e mente em "
              "dois métodos. Método vazio numa interface é a confissão de que ela pede "
              "demais - e a métrica de ISP é contável: três obrigados contra um."),
    dict(id="state-transicao", aula=25, arquivo="exemplos/deriva/src/padroes.cpp",
         de="std::unique_ptr<i_tela> tela_mapa::comando(std::string_view c) {",
         ate="}", comentario=True,
         legenda="src/padroes.cpp · State, e a transição é o retorno",
         nota="Devolver a próxima tela em vez de mutar um campo é o que impede duas "
              "telas de discordarem sobre qual está ativa. A alternativa é um `switch` "
              "com vinte casos espalhados por cinco funções."),
    dict(id="decorator-empilha", aula=25,
         arquivo="exemplos/deriva/testes/test_padroes_extra.cpp",
         de='TEST_CASE("Decorator: empilhar dois nao exige classe', ate="}",
         comentario=True,
         legenda="testes/test_padroes_extra.cpp · Decorator, empilhado",
         nota="Com herança, \"numerado e com moldura\" exigiria uma classe para cada "
              "combinação. Com decorador, é a ordem da pilha - e a ordem é observável "
              "na saída."),
    dict(id="singleton-criticado", aula=25,
         arquivo="exemplos/deriva/include/deriva/padroes.hpp",
         de="class registro_global {", ate="};", comentario=True,
         legenda="include/deriva/padroes.hpp · Singleton, escrito para ser criticado",
         nota="É o Singleton de Meyers, a versão correta da forma errada. Os quatro "
              "custos estão no comentário, e nenhum é opinião - o segundo deles é "
              "medido por dois casos de teste que compartilham estado de propósito."),
    dict(id="prova-do-segundo-frontend", aula=26,
         arquivo="exemplos/deriva/testes/test_padroes.cpp",
         de='TEST_CASE("duas apresentacoes sobre o MESMO mundo', ate="}",
         comentario=True,
         legenda="testes/test_padroes.cpp · a prova do critério da §26.1",
         nota="Duas implementações da mesma interface, no mesmo processo, sobre o mesmo "
              "mundo. É o que a variante `v2.6-antes` torna impossível, e é a diferença "
              "entre separação demonstrada e separação afirmada."),
    dict(id="render-nao-muda-estado", aula=26,
         arquivo="exemplos/deriva/testes/test_padroes.cpp",
         de='TEST_CASE("trocar a apresentacao nao muda o estado do dominio")', ate="}",
         comentario=True,
         legenda="testes/test_padroes.cpp · desenhar não altera o mundo",
         nota="Cinco renders, e o despejo byte a byte igual. Se desenhar mudasse "
              "estado, a segunda interface veria um sistema diferente da primeira."),

    # ---- Anexo A · o alvo opcional de C++20 (aula=0) -----------------------
    dict(id="concept-em-vez-de-assert", aula=0,
         arquivo="exemplos/deriva/c20/restricoes.hpp",
         de="concept guardavel", ate="", comentario=True,
         legenda="c20/restricoes.hpp · o concept no lugar do static_assert",
         nota="A diferença que se vê é a mensagem de erro: com `static_assert` o "
              "compilador aponta a linha do assert; com `concept`, aponta a CHAMADA e "
              "diz qual restrição falhou. É a razão de os concepts existirem."),
    dict(id="ranges-sem-temporario", aula=0,
         arquivo="exemplos/deriva/c20/restricoes.hpp",
         de="[[nodiscard]] inline std::string glifos_de_parede(", ate="}",
         comentario=True,
         legenda="c20/restricoes.hpp · ranges, sem contêiner intermediário",
         nota="`filter` e `transform` são vistas preguiçosas: nada é copiado até alguém "
              "iterar. Em C++17 o equivalente seria um `copy_if` para um vetor "
              "temporário e um `transform` depois - dois laços e uma alocação."),

    # ---- Aula 20 · erros ---------------------------------------------------
    dict(id="optional-filesystem", aula=20, arquivo="exemplos/deriva/src/mapa.cpp",
         de="std::optional<mapa> mapa::carregar", ate="}",
         legenda="src/mapa.cpp · optional e filesystem",
         nota="Arquivo ausente é *ausência de resultado*, não exceção - `optional` "
              "diz isso no tipo. Erro de verdade, permissão negada, é exceção, e "
              "chega na v2.2. Repare que `exists` e abrir são operações distintas: "
              "a corrida entre elas é real."),

    # ---- diagramas · a notação também vem de arquivo -----------------------
    #
    # Os quatro diagramas eram digitados no material, e eram a última coisa
    # que contrariava a regra do handoff §5. Diagrama digitado é pior que
    # código digitado: ele pode afirmar uma hierarquia que o código não tem,
    # e nada o denuncia. Agora vêm por âncora, e `test_uml.cpp` afirma as
    # relações que eles desenham.
    dict(id="uml-mapa-tem-grade", inline=True, aula=6,
         arquivo="exemplos/deriva/diagramas/mapa-tem-grade.mmd",
         de="classDiagram", ate="grade ..> vetor2 : parametro",
         legenda="diagramas/mapa-tem-grade.mmd · mapa TEM uma grade",
         nota="A seta de composição, e não de herança: `mapa` guarda uma `grade` "
              "como membro. As oito relações que este desenho afirma são as que "
              "`testes/test_uml.cpp` verifica, uma por caso."),
    dict(id="uml-carregar-sequencia", inline=True, aula=6,
         arquivo="exemplos/deriva/diagramas/carregar-em-sequencia.mmd",
         de="sequenceDiagram", ate="end",
         legenda="diagramas/carregar-em-sequencia.mmd · carregar, passo a passo",
         nota="O caminho de `mapa::carregar` com os dois desfechos: `nullopt` "
              "quando o arquivo falta, e o mapa construído quando ele existe. "
              "A ausência é resposta, e não exceção."),
    dict(id="uml-grade-sozinha", inline=True, aula=6,
         arquivo="exemplos/deriva/diagramas/grade-sozinha.mmd",
         de="classDiagram", ate="+bytes_das_celulas() size_t",
         legenda="diagramas/grade-sozinha.mmd · a grade e os seus membros",
         nota="A grade isolada, com o que ela declara e mais nada. É o desenho "
              "que o Cap. 6 usa para introduzir a notação antes de haver "
              "hierarquia nenhuma no sistema."),
    dict(id="uml-agregados", inline=True, aula=7,
         arquivo="exemplos/deriva/diagramas/agregados-e-leiaute.mmd",
         de="classDiagram", ate="+int criados$",
         legenda="diagramas/agregados-e-leiaute.mmd · os agregados e o leiaute",
         nota="`vetor2` e `celula` como agregados, e a `celula_ingenua` ao lado "
              "para mostrar o que a ordem de declaração custa. O `$` marca o "
              "membro estático, que não vive dentro do objeto."),
]


def por_aula(n):
    """Os trechos de uma aula, na ordem em que TRECHOS os declara.

    A ordem é a da declaração de propósito: ela é a ordem em que o material
    apresenta os trechos, e trocá-la por ordem de arquivo faria o texto
    referir-se a um bloco que ainda não apareceu.
    """
    return [t for t in TRECHOS if t["aula"] == n]
