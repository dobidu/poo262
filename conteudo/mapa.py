# -*- coding: utf-8 -*-
"""
conteudo/mapa.py - a tabela canônica do POO v2.

Fonte: PLANO_DE_ENSINO_POO_v2.md, PLANO-MATERIAL-POO-v2.md §2 e §5,
PLANO-LIVRO-POO-v2.md §2. É a ÚNICA definição de:

  · quais são as 26 aulas e em que ordem;
  · de qual capítulo do livro v1 e de qual página do site v1 cada uma vem;
  · quais aulas se fundem, quais se partem, e em que fatia;
  · qual versão do Deriva cada aula entrega;
  · qual interativo cada aula recebe;
  · qual laboratório preparatório cai em qual semana.

A numeração de aula deixou de coincidir com a de capítulo do livro v1.
Livro v2 e site v2 usam a MESMA numeração (Aula N = Capítulo N), que é a
decisão de PLANO-LIVRO §1. Portanto: `cap_v2 == aula`.

Nada aqui é adivinhado. Onde o plano manda escrever conteúdo novo, o campo
`novo` diz o que é, e o gerador emite um marcador visível em vez de prosa
inventada.
"""

# ---------------------------------------------------------------------------
# unidades
# ---------------------------------------------------------------------------
UNIDADES = [
    {
        "n": "I",
        "rot": "Fundamentos",
        "tema": ("Da programação procedural ao objeto: infraestrutura, fundamentos de "
                 "C++17, Git e revisão de código gerado por IA, tipos, UML, classes, "
                 "ciclo de vida e as operações especiais."),
        "aulas": range(1, 10),
        "deriva": "v0.0 → v0.3",
        "paginas_livro": 40,
    },
    {
        "n": "II",
        "rot": "Hierarquias, posse e despacho",
        "tema": ("Herança antes de ponteiro inteligente: virtuais, posse exclusiva e "
                 "compartilhada, movimento e a regra dos cinco, operadores, testes com "
                 "replay, diamante e RTTI."),
        "aulas": range(10, 19),
        "deriva": "v1.0 → v1.8",
        "paginas_livro": 48,
    },
    {
        "n": "III",
        "rot": "Genericidade, robustez e projeto",
        "tema": ("Templates e CRTP com alvo concreto, erros, STL e lambdas, "
                 "concorrência, serialização, SOLID verificado por replay, padrões e "
                 "um segundo front-end sobre o mesmo núcleo."),
        "aulas": range(19, 27),
        "deriva": "v2.0 → v2.7",
        "paginas_livro": 46,
    },
]

# ---------------------------------------------------------------------------
# as 26 aulas
#
# origem_v1 : arquivo do site v1 em legado/site-v1/, sem .html
# fatia     : None = página inteira; ("1/3", "raii") = fatia identificada
# funde     : lista de origens adicionais (aula 4)
# cap_v1    : capítulo(s) do livro v1 que alimentam este capítulo v2
# ---------------------------------------------------------------------------
AULAS = [
    dict(n=1,  slug="a01", titulo="Da programação procedural à orientação a objetos",
         curto="Do procedural ao objeto", unidade="I",
         cap_v1=[1], origem_v1=["unidade-1/aula01-complexidade-oo"], fatia=None,
         interativos=["refator"], deriva=None, lab=None,
         nota_migracao="Exemplo comparativo migra de “Sistema de Alunos” para o Deriva."),

    dict(n=2,  slug="a02", titulo="Infraestrutura do programador C++",
         curto="Infraestrutura: CMake, FetchContent, gdb", unidade="I",
         cap_v1=[4], origem_v1=["unidade-1/aula04-transicao-cpp"], fatia=None,
         interativos=["expansor"], deriva="v0.0", lab="LAB-01",
         nota_migracao=("Sobe do 4º para o 2º lugar. Entra FetchContent com FTXUI e "
                        "Catch2 como dependência SYSTEM, para o portão de zero warnings "
                        "incidir só no código do estudante. Sai o bloco de sanitizers "
                        "como portão (o laboratório não os tem) e entra gdb com ponto "
                        "de parada em destrutor."),
         novo=["gdb com ponto de parada em destrutor", "portão `make verifica`"]),

    dict(n=3,  slug="a03", titulo="Fundamentos de C++17 para POO",
         curto="Fundamentos de C++17", unidade="I",
         cap_v1=[2], origem_v1=["unidade-1/aula02-conceitos-fundamentais"], fatia=None,
         interativos=["ciclo"], deriva=None, lab="LAB-02",
         nota_migracao=("O capítulo com maior déficit do livro. Entram std::string_view "
                        "com a armadilha de tempo de vida, ligações estruturadas, "
                        "[[nodiscard]] e [[maybe_unused]] - hoje com zero ocorrências "
                        "no livro inteiro."),
         novo=["std::string_view e a pendência de tempo de vida",
               "ligações estruturadas", "[[nodiscard]] e [[maybe_unused]]"]),

    dict(n=4,  slug="a04", titulo="Git, LLM como copiloto e a rubrica de revisão",
         curto="Git, LLM e a rubrica", unidade="I",
         cap_v1=[5, 6, 27], origem_v1=["unidade-1/aula05-git-github",
                                       "unidade-1/aula06-llms-copiloto",
                                       "unidade-3/aula27-qt-llms"],
         fatia=("llm", "a fatia de LLM do Cap. 27; a fatia de Qt vai para a Aula 26"),
         interativos=["revisor"], deriva=None, lab="LAB-03",
         nota_migracao=("MIGRAÇÃO DE RISCO 2/3 - fusão de três origens. A rubrica de "
                        "revisão de código OO gerado por IA sai do fim do livro e vem "
                        "para cá, porque passa a ser instrumento das três caças ao bug: "
                        "um instrumento tem de chegar antes do uso."),
         novo=["rubrica de revisão de código OO gerado por IA, publicada como artefato"]),

    dict(n=5,  slug="a05", titulo="Classificação de linguagens e sistemas de tipos",
         curto="Linguagens e sistemas de tipos", unidade="I",
         cap_v1=[3], origem_v1=["unidade-1/aula03-classificacao-linguagens"], fatia=None,
         interativos=["virtual"], deriva=None, lab=None,
         nota_migracao="Renumeração."),

    dict(n=6,  slug="a06", titulo="UML leve",
         curto="UML que serve ao código", unidade="I",
         cap_v1=[7], origem_v1=["unidade-1/aula07-uml-leve"], fatia=None,
         interativos=["uml", "revisor"], deriva=None, lab=None,
         nota_migracao="Diagramas passam a ser do Deriva."),

    dict(n=7,  slug="a07", titulo="Classes e objetos; o contador de instâncias vivas",
         curto="Classes, objetos e o contador `vivos`", unidade="I",
         cap_v1=[8], origem_v1=["unidade-1/aula08-classes-objetos"], fatia=None,
         interativos=["inspetor"], deriva="v0.1", lab="LAB-04",
         nota_migracao=("Membros estáticos ganham o exemplo canônico da disciplina: "
                        "static int vivos, incrementado no construtor e decrementado no "
                        "destrutor. É o detector de vazamento que a disciplina usa por "
                        "19 capítulos, e é o que motiva o template do Cap. 19."),
         novo=["o contador `vivos` como exemplo canônico de membro estático"]),

    dict(n=8,  slug="a08", titulo="Ciclo de vida e RAII",
         curto="Ciclo de vida e RAII", unidade="I",
         cap_v1=[9, 10], origem_v1=["unidade-1/aula09-ciclo-de-vida",
                                    "unidade-2/aula10-raii-rule-of-five"],
         fatia=("raii", "fatia 1/3 do Cap. 10 - só RAII"),
         interativos=["ciclo"], deriva="v0.2", lab="LAB-05",
         nota_migracao=("MIGRAÇÃO DE RISCO 1/3 - absorve o RAII que estava no Cap. 10. "
                        "Entra a instrumentação de ciclo de vida (construtores e "
                        "destrutores imprimindo a própria execução) e o terminal_bruto."),
         novo=["instrumentação de ciclo de vida", "terminal_bruto e o RAII com consequência física"]),

    dict(n=9,  slug="a09", titulo="Operações especiais: a regra do zero e do três",
         curto="Regra do zero e do três", unidade="I",
         cap_v1=[10], origem_v1=["unidade-2/aula10-raii-rule-of-five"],
         fatia=("zero-tres", "fatia 2/3 do Cap. 10 - cópia e atribuição; a regra dos "
                            "cinco vai para a Aula 14, já na Unidade II"),
         interativos=["ciclo"], deriva="v0.3", lab=None,
         nota_migracao=("MIGRAÇÃO DE RISCO 1/3 (continuação). Atenção: a regra dos cinco "
                        "atravessa fronteira de unidade e de prova."),
         caca_bug=("CAÇA AO BUG 1", "cópia rasa em `grade` - semana 5")),

    dict(n=10, slug="a10", titulo="Herança simples",
         curto="Herança simples", unidade="II",
         cap_v1=[15], origem_v1=["unidade-2/aula15-heranca-simples"], fatia=None,
         interativos=["inspetor"], deriva="v1.0", lab=None,
         nota_migracao="Sobe cinco posições: passa à frente dos ponteiros inteligentes."),

    dict(n=11, slug="a11", titulo="Funções virtuais e classes abstratas",
         curto="Funções virtuais e vtable", unidade="II",
         cap_v1=[17], origem_v1=["unidade-2/aula17-funcoes-virtuais"], fatia=None,
         interativos=["virtual"], deriva="v1.1", lab="LAB-06",
         nota_migracao=("O destrutor virtual ganha tratamento próprio: o vazamento que "
                        "sua ausência produz, acusado pelo contador `vivos` da Aula 7 e "
                        "lido no gdb."),
         caca_bug=("CAÇA AO BUG 2", "destrutor não virtual - semana 9")),

    dict(n=12, slug="a12", titulo="Ponteiros inteligentes I - posse exclusiva",
         curto="Posse exclusiva: unique_ptr", unidade="II",
         cap_v1=[11], origem_v1=["unidade-2/aula11-smart-pointers"],
         fatia=("unique", "fatia 1/2 do Cap. 11 - unique_ptr; a introdução comum "
                          "(por que ponteiro inteligente existe) vive AQUI e é "
                          "referenciada, não duplicada, na Aula 13"),
         interativos=["posse"], deriva="v1.2", lab=None,
         nota_migracao=("MIGRAÇÃO DE RISCO 3/3. O ponteiro cru com posse entra como "
                        "contraexemplo documentado, com menção ao tutorial de roguelike "
                        "em C++ mais difundido (RogueBasin/libtcod), criticado justamente "
                        "por isso.")),

    dict(n=13, slug="a13", titulo="Ponteiros inteligentes II - posse compartilhada",
         curto="Posse compartilhada: shared_ptr e weak_ptr", unidade="II",
         cap_v1=[11], origem_v1=["unidade-2/aula11-smart-pointers"],
         fatia=("shared", "fatia 2/2 do Cap. 11 - shared_ptr, weak_ptr, contagem de "
                          "referências, o ciclo que o contador acusa"),
         interativos=["posse"], deriva="v1.3", lab="LAB-07",
         nota_migracao="MIGRAÇÃO DE RISCO 3/3 (continuação)."),

    dict(n=14, slug="a14", titulo="Semântica de movimento e a regra dos cinco",
         curto="Movimento e a regra dos cinco", unidade="II",
         cap_v1=[12, 10], origem_v1=["unidade-2/aula12-move-semantics",
                                     "unidade-2/aula10-raii-rule-of-five"],
         fatia=("cinco", "fatia 3/3 do Cap. 10 - a regra dos cinco"),
         interativos=["move"], deriva="v1.4", lab="LAB-08",
         nota_migracao=("MIGRAÇÃO DE RISCO 1/3 (fecho). Entra std::forward e "
                        "encaminhamento perfeito como panorama - hoje zero ocorrências "
                        "num capítulo sobre movimento. E a prosa precisa ser corrigida: "
                        "std::move NÃO garante origem vazia (ver §4 do interativo)."),
         novo=["std::forward e encaminhamento perfeito",
               "correção: estado válido mas não-especificado, com SSO"]),

    dict(n=15, slug="a15", titulo="Sobrecarga de operadores",
         curto="Sobrecarga de operadores", unidade="II",
         cap_v1=[13], origem_v1=["unidade-2/aula13-sobrecarga-operadores"], fatia=None,
         interativos=["virtual"], deriva="v1.5", lab=None,
         nota_migracao="Operadores do Deriva: vetor2, operator[] de mapa, operator<<."),

    dict(n=16, slug="a16", titulo="Testes com Catch2 e replay determinístico",
         curto="Catch2 e replay determinístico", unidade="II",
         cap_v1=[14], origem_v1=["unidade-2/aula14-testes-catch2"], fatia=None,
         interativos=["refator"], deriva="v1.6", lab="LAB-09",
         nota_migracao=("O teste como especificação executável. Entra o replay: semente "
                        "fixa, roteiro gravado, despejo idêntico byte a byte. É o oráculo "
                        "das Aulas 24 e 25."),
         novo=["replay determinístico como portão de refatoração"]),

    dict(n=17, slug="a17", titulo="Herança múltipla e o diamante",
         curto="Herança múltipla e o diamante", unidade="II",
         cap_v1=[16], origem_v1=["unidade-2/aula16-heranca-multipla"], fatia=None,
         interativos=["inspetor", "uml"], deriva="v1.7", lab=None,
         nota_migracao="Renumeração."),

    dict(n=18, slug="a18", titulo="Polimorfismo dinâmico e RTTI",
         curto="Polimorfismo dinâmico e RTTI", unidade="II",
         cap_v1=[18], origem_v1=["unidade-2/aula18-polimorfismo-dinamico"], fatia=None,
         interativos=["virtual"], deriva="v1.8", lab=None,
         nota_migracao="Renumeração."),

    dict(n=19, slug="a19", titulo="Templates, polimorfismo estático e CRTP",
         curto="Templates, CRTP e contador_de_instancias<T>", unidade="III",
         cap_v1=[19, 20], origem_v1=["unidade-3/aula19-templates-crtp",
                                     "unidade-3/aula20-concepts-ranges"],
         fatia=("absorve-20", "o Cap. 20 entra comprimido em 20 minutos e rotulado "
                              "C++20; o conteúdo integral vira o Anexo A"),
         interativos=["expansor"], deriva="v2.0", lab="LAB-10",
         nota_migracao=("if constexpr no lugar de SFINAE. O CRTP ganha alvo concreto: "
                        "generalizar em contador_de_instancias<T> o que foi escrito à "
                        "mão em três classes desde a Aula 7. A repetição anterior é o "
                        "argumento do template."),
         novo=["contador_de_instancias<T> por CRTP"]),

    dict(n=20, slug="a20", titulo="Tratamento de erros",
         curto="Tratamento de erros", unidade="III",
         cap_v1=[21], origem_v1=["unidade-3/aula21-tratamento-erros"], fatia=None,
         interativos=["ciclo"], deriva="v2.2", lab="LAB-11",
         nota_migracao=("Entra std::filesystem no carregamento de mapa - hoje ausente. "
                        "Garantias de exceção e desenrolar da pilha com destrutores "
                        "ganham peso, por ligarem à Aula 8."),
         novo=["std::filesystem no carregamento de mapa"]),

    dict(n=21, slug="a21", titulo="STL panorâmica e lambdas",
         curto="STL e lambdas", unidade="III",
         cap_v1=[22], origem_v1=["unidade-3/aula22-stl"], fatia=None,
         interativos=["expansor"], deriva="v2.3", lab=None,
         nota_migracao=("Lambdas passam de UMA menção no livro inteiro a conteúdo de "
                        "capítulo. Entra std::clamp."),
         novo=["lambdas como conteúdo de capítulo", "std::clamp"]),

    dict(n=22, slug="a22", titulo="Concorrência em C++ - panorâmica",
         curto="Panorâmica de concorrência", unidade="III",
         cap_v1=[23], origem_v1=["unidade-3/aula23-concorrencia"], fatia=None,
         interativos=["corrida"], deriva="v2.4", lab=None,
         nota_migracao=("Ponte explícita com Programação Concorrente. O interativo de "
                        "race condition vem de LPII com a legenda trocada - primeiro "
                        "reaproveitamento entre as duas disciplinas.")),

    dict(n=23, slug="a23", titulo="Serialização",
         curto="Serialização e versionamento", unidade="III",
         cap_v1=[24], origem_v1=["unidade-3/aula24-serializacao"], fatia=None,
         interativos=["revisor"], deriva="v2.5", lab=None,
         nota_migracao="Salvar e carregar partida do Deriva; versionamento de formato."),

    dict(n=24, slug="a24", titulo="SOLID e invariância de comportamento",
         curto="SOLID e invariância", unidade="III",
         cap_v1=[25], origem_v1=["unidade-3/aula25-solid"], fatia=None,
         interativos=["refator"], deriva="v2.6", lab="LAB-12",
         nota_migracao=("A refatoração do `mundo` como god class, verificada por replay. "
                        "A lição é que refatoração correta é a que não muda a saída."),
         caca_bug=("CAÇA AO BUG 3", "refatoração que mudou a saída - semana 13")),

    dict(n=25, slug="a25", titulo="Padrões de projeto canônicos em C++ moderno",
         curto="Padrões de projeto", unidade="III",
         cap_v1=[26], origem_v1=["unidade-3/aula26-design-patterns"], fatia=None,
         interativos=["refator"], deriva="v2.6", lab=None,
         nota_migracao=("Strategy com lambdas, não com herança; Command, State, "
                        "Observer, Factory, Composite e Decorator sobre o Deriva; "
                        "Singleton e seus problemas.")),

    dict(n=26, slug="a26", titulo="Qt e a separação domínio/apresentação",
         curto="Qt sobre o mesmo núcleo", unidade="III",
         cap_v1=[27], origem_v1=["unidade-3/aula27-qt-llms"],
         fatia=("qt", "fatia de Qt do Cap. 27; a fatia de LLM foi para a Aula 4"),
         interativos=["refator"], deriva="v2.7", lab=None,
         nota_migracao=("MIGRAÇÃO DE RISCO 2/3 (fecho). Demonstração do docente com "
                        "esqueleto publicado - o plano v2 não exige entrega. Fica "
                        "QObject, signals/slots e o argumento do segundo front-end "
                        "sobre o mesmo núcleo.")),
]

# ---------------------------------------------------------------------------
# anexos - conteúdo que mudou de estatuto, não que se perdeu
# ---------------------------------------------------------------------------
ANEXOS = [
    dict(letra="A", slug="anexo-a", titulo="Concepts e Ranges", c20=True,
         curto="Concepts e Ranges (C++20)",
         origem_v1=["unidade-3/aula20-concepts-ranges"],
         nota=("Deixou de ser aula porque deixou de caber: são 20 minutos dentro da "
               "Aula 19. O conteúdo não foi descartado - mudou de estatuto. Nada no "
               "material obrigatório depende dele, e o alvo da disciplina segue C++17."),
         deriva="v2.1 (opcional)"),
    dict(letra="B", slug="anexo-b", titulo="Referência rápida de C++17", c20=False,
         curto="Referência rápida de C++17", origem_v1=[],
         nota=("Tabela de consulta para prova e laboratório. Cobre exatamente as "
               "construções que o livro v1 não tinha: string_view, ligações "
               "estruturadas, [[nodiscard]], if constexpr, optional/variant, "
               "filesystem, clamp, CTAD, fold expressions."),
         deriva=None),
    dict(letra="C", slug="anexo-c", titulo="O Deriva: as 20 versões", c20=False,
         curto="O Deriva: as 20 versões", origem_v1=[],
         nota=("v0.0 a v2.7, cada uma com o capítulo que a introduz e as variantes "
               "quebradas. É o mesmo conteúdo da trilha do site."),
         deriva=None),
]

# ---------------------------------------------------------------------------
# a trilha do Deriva - 20 versões obrigatórias + v2.1 opcional (C++20)
#
# quebrada: (tag, o que quebra, como se percebe)
# DIVERGÊNCIA REGISTRADA, para não ser redescoberta a cada passada: o
# PLANO_DE_ENSINO chama a Aula 20 de v2.1 e desloca todas as versões seguintes
# em um. Este mapa usa v2.2 na Aula 20 e reserva a v2.1 para o alvo OPCIONAL de
# C++20, que é a única aritmética que fecha as "20 versões (v0.0 → v2.7)" do
# PLANO-LIVRO com as 26 aulas: 4 na Unidade I, 9 na II, 7 na III obrigatórias,
# mais a v2.1 fora da conta. Se o autor preferir a numeração do plano de
# ensino, muda aqui e o site e o livro acompanham.
#
# meta:     o número de testes é PROJEÇÃO, não medição. Só a versão que existe
#           em código (`VERSAO_ATUAL`) traz número medido, e
#           `build/verifica_numeros.py` o confere contra o ctest. Sem essa
#           distinção a trilha anuncia contagem que ninguém rodou - foi o que
#           aconteceu: ela dizia 24 testes na v1.6 enquanto o portão passava 26.
# ---------------------------------------------------------------------------
VERSAO_ATUAL = "v2.7"
TRILHA = [
    dict(v="v0.0", aula=[2], entrega="esqueleto que compila: CMake, FetchContent, main vazio",
         conceitos="CMake, FetchContent, FTXUI v5.0.0 e Catch2 como SYSTEM, make verifica",
         nota_testes="só o teste de fumaça do esqueleto"),
    dict(v="v0.1", aula=[7], entrega="vetor2, celula e o contador `vivos`",
         conceitos="encapsulamento, const-correctness, static, this, [[nodiscard]]",
         nota_testes=None),
    dict(v="v0.2", aula=[8], entrega="grade e terminal_bruto",
         conceitos="construtores, destrutor, lista de inicialização, RAII, instrumentação de ciclo de vida",
         nota_testes=None,
         quebrada=("v0.2-quebrada", "terminal_bruto sem destrutor",
                   "o terminal do estudante fica inutilizável ao sair - a melhor "
                   "demonstração de RAII que existe, e não é metáfora")),
    dict(v="v0.3", aula=[9], entrega="mapa, carregamento de arquivo e o PRIMEIRO render",
         conceitos="composição, regra do zero e do três, std::optional, std::filesystem, string_view",
         nota_testes=None,
         quebrada=("v0.3-quebrada", "cópia rasa em `grade`",
                   "CAÇA AO BUG 1 (semana 5): duas grades compartilham o mesmo buffer; "
                   "o contador `vivos` não fecha e o segundo destrutor libera duas vezes")),

    dict(v="v1.0", aula=[10], entrega="hierarquia entidade → sonda / drone / item",
         conceitos="herança pública, override, final, subobjeto base",
         nota_testes=None),
    dict(v="v1.1", aula=[11], entrega="desenhar() e agir() virtuais; destrutor virtual",
         conceitos="funções virtuais, classe abstrata, vptr e vtable, destrutor virtual",
         nota_testes=None,
         quebrada=("v1.1-quebrada", "destrutor não virtual na base",
                   "CAÇA AO BUG 2 (semana 9): `vivos` nunca volta a zero e o gdb mostra "
                   "que ~sonda() nunca roda ao deletar por entidade*")),
    dict(v="v1.2", aula=[12], entrega="mundo com vector<unique_ptr<entidade>>",
         conceitos="posse exclusiva, unique_ptr, make_unique, ponteiro cru como contraexemplo",
         nota_testes=None),
    dict(v="v1.3", aula=[13], entrega="grafo de conexões da estação com shared_ptr",
         conceitos="posse compartilhada, shared_ptr, weak_ptr, contagem de referências, o ciclo que vaza",
         nota_testes=None),
    dict(v="v1.4", aula=[14], entrega="movimento em grade e mapa",
         conceitos="rvalue refs, std::move, regra dos cinco, noexcept, std::forward",
         nota_testes=None),
    dict(v="v1.5", aula=[15], entrega="operadores de vetor2 e mapa[pos]",
         conceitos="sobrecarga, funções livres, operator<<, operator[] const e não-const",
         nota_testes=None),
    dict(v="v1.6", aula=[16], entrega="testes de FOV e caminho + replay determinístico",
         conceitos="Catch2, semente fixa, roteiro gravado, despejo idêntico byte a byte",
         nota_testes="mais 3 replays comparados byte a byte"),
    dict(v="v1.7", aula=[17], entrega="sonda_reparadora: o diamante",
         conceitos="herança múltipla, interface pura, herança virtual, ordem de construção",
         nota_testes=None),
    dict(v="v1.8", aula=[18], entrega="inspetor de entidade no console",
         conceitos="RTTI, dynamic_cast, typeid, quando NÃO usar",
         nota_testes=None),

    dict(v="v2.0", aula=[19], entrega="grade<T> genérica e contador_de_instancias<T>",
         conceitos="templates, if constexpr, static_assert, CRTP",
         nota_testes=None),
    dict(v="v2.1", aula=[], entrega="restrições em grade<T> por concept", opcional=True, c20=True,
         conceitos="Concepts e Ranges - fora do padrão-alvo, alvo de compilação separado",
         nota_testes="alvo opcional de C++20, fora do portão `make verifica`"),
    dict(v="v2.2", aula=[20], entrega="erros de carregamento de mapa",
         conceitos="exceções, garantias, std::optional, std::variant, std::filesystem",
         nota_testes=None),
    dict(v="v2.3", aula=[21], entrega="FOV e inventário com algoritmos",
         conceitos="STL, lambdas, std::clamp, std::size",
         nota_testes=None),
    dict(v="v2.4", aula=[22], entrega="thread de entrada separada do render",
         conceitos="std::thread, std::mutex, corrida de dados - panorâmica",
         nota_testes=None),
    dict(v="v2.5", aula=[23], entrega="salvar e carregar partida",
         conceitos="serialização, versionamento de formato, compatibilidade regressiva",
         nota_testes=None),
    dict(v="v2.6", aula=[24, 25], entrega="refatoração do mundo + os seis padrões",
         conceitos="SOLID; Command, State, Observer, Factory, Strategy (lambda), Composite, Decorator",
         nota_testes="mais o replay idêntico byte a byte",
         quebrada=("v2.6-antes", "`mundo` como god class",
                   "CAÇA AO BUG 3 (semana 13): a refatoração ingênua muda a saída, e o "
                   "replay acusa - refatoração correta é a que não muda a saída")),
    dict(v="v2.7", aula=[26], entrega="front-end Qt sobre o mesmo núcleo",
         conceitos="QObject, signals/slots, separação domínio/apresentação",
         nota_testes="nenhum teste novo, e é esse o argumento: o núcleo não mudou",   # MEDIDO
         ),
]

# ---------------------------------------------------------------------------
# os 8 tipos canônicos de interativo (PLANO-MATERIAL §5)
# ---------------------------------------------------------------------------
INTERATIVOS = {
    "inspetor": dict(n=1, titulo="Inspetor de objeto",
        nota="leiaute em memória, ordem de declaração, padding, subobjeto base, membro estático fora do objeto",
        aulas=[7, 10, 17]),
    "ciclo": dict(n=2, titulo="Rastreador de ciclo de vida",
        nota="ordem exata de construção e destruição, escopos, desenrolar por exceção, referência pendente",
        aulas=[3, 8, 9, 20]),
    "virtual": dict(n=3, titulo="Despachante",
        nota="vptr e vtable, tipo estático versus dinâmico, resolução de sobrecarga, dynamic_cast",
        aulas=[5, 11, 15, 18]),
    "move": dict(n=4, titulo="Copiar × mover",
        nota="com o estado do objeto de origem DEPOIS da operação",
        aulas=[14]),
    "posse": dict(n=5, titulo="Grafo de posse",
        nota="unique_ptr, shared_ptr, weak_ptr, contagem de referências, o ciclo que vaza",
        aulas=[12, 13]),
    "refator": dict(n=6, titulo="Diferenciador de refatoração",
        nota="antes/depois, grafo de acoplamento, e o diff do despejo que prova invariância",
        aulas=[1, 16, 24, 25, 26]),
    "expansor": dict(n=7, titulo="Expansor de compilação e template",
        nota="pré-processador/compilação/ligação e onde cada erro aparece; instanciação; if constexpr podando ramo",
        aulas=[2, 19, 21]),
    "revisor": dict(n=8, titulo="Revisor com rubrica",
        nota="código OO gerado, plausível e defeituoso, com cada item da rubrica acendendo a falha",
        aulas=[4, 6, 23]),
    # reaproveitado de LPII, com a legenda trocada
    "corrida": dict(n=9, titulo="Corrida de dados", reaproveitado="LPII",
        nota="dois fluxos sobre o mesmo contador, com e sem mutex",
        aulas=[22]),
    # T9: não é peça do motor, tem arquivo próprio
    "uml": dict(n=0, titulo="Diagrama de classes interativo", ferramenta=True,
        nota="o estudante acrescenta classe e relação; os níveis vêm da profundidade calculada",
        aulas=[6, 17]),
}

# ---------------------------------------------------------------------------
# 12 laboratórios preparatórios - publicados COM solução (PLANO-MATERIAL §3)
# ---------------------------------------------------------------------------
LABS = [
    # Tabela transcrita de PLANO_DE_ENSINO_POO_v2.md, seção dos 12 laboratórios.
    # É ela a autoridade sobre título, aula e portão - a primeira versão deste
    # mapa trazia títulos inventados e seis das doze aulas erradas.
    dict(id="LAB-01", aula=2,  semana="1 · E2",
         titulo="Ambiente, CMake com FetchContent e portões de compilação",
         portao="compilar sem warning; o primeiro alvo do Deriva"),
    dict(id="LAB-02", aula=3,  semana="2 · E1",
         titulo="C++17 na prática: string_view, ligações estruturadas e [[nodiscard]]",
         portao="a armadilha de tempo de vida do string_view, reproduzida e explicada"),
    dict(id="LAB-03", aula=4,  semana="2 · E2",
         titulo="Git como registro de decisão",
         portao="branch, merge e mensagem que justifica"),
    dict(id="LAB-04", aula=7,  semana="4 · E1",
         titulo="UML leve do Deriva; vetor2 e celula, e o contador `vivos`",
         portao="classe antes de código; invariante que a classe protege; o que const promete"),
    dict(id="LAB-05", aula=8,  semana="4 · E2",
         titulo="Ciclo de vida e terminal_bruto: RAII com consequência",
         portao="esquecer o destrutor e ver o terminal quebrar; depois consertar"),
    dict(id="LAB-06", aula=11, semana="6 · E2",
         titulo="O destrutor não virtual, acusado pelo contador `vivos`",
         portao="provar o vazamento sem ferramenta externa; gdb no destrutor"),
    dict(id="LAB-07", aula=13, semana="7 · E2",
         titulo="Posse: unique_ptr, shared_ptr e o ciclo que vaza",
         portao="escolher a posse por requisito; provocar e desfazer o ciclo"),
    dict(id="LAB-08", aula=14, semana="8 · E1",
         titulo="Cópia versus movimento em grade, e o objeto de origem depois",
         portao="instrumentar o ciclo de vida e ler a ordem na saída"),
    dict(id="LAB-09", aula=16, semana="9 · E1",
         titulo="Catch2 e o replay determinístico como especificação",
         portao="escrever o teste que trava a refatoração antes de refatorar"),
    dict(id="LAB-10", aula=19, semana="11 · E1",
         titulo="CRTP e contador_de_instancias<T>: generalizar o próprio detector",
         portao="polimorfismo estático aplicado ao que já foi escrito três vezes à mão"),
    dict(id="LAB-11", aula=20, semana="11 · E2",
         titulo="Erros no carregamento de mapa: exceções, optional e variant",
         portao="garantia de exceção; desenrolar da pilha com destrutores"),
    dict(id="LAB-12", aula=24, semana="13 · E2",
         titulo="Refatorar o `mundo` sob SOLID sem mudar um byte da saída",
         portao="invariância de comportamento verificada por replay"),
]

# A distribuição por unidade não é livre: o plano a fixa em 5 / 4 / 3
# (PLANO-MATERIAL §7, sprints 4, 5 e 6), e `verificar()` afirma isso. O mapa
# nasceu com 5/5/2 porque um laboratório de diamante ocupava a Aula 17; ele
# saiu, a Unidade III ganhou o de STL e lambdas, e a Aula 17 ficou com os dois
# interativos e os exercícios, sem laboratório próprio.
LABS_POR_UNIDADE = {"I": 5, "II": 4, "III": 3}

# ---------------------------------------------------------------------------
# os 5 tipos de callout · `sintonia` virou `deriva`
# ---------------------------------------------------------------------------
# O repositório da disciplina.
#
# Uma linha, e uma só. O material escreve `<endereco-do-repositorio>` no
# fonte, e `build/build_site.py` o troca por isto ao gerar - então trocar de
# host, de organização ou de nome é uma edição aqui, e não vinte e sete pelas
# páginas. Voltando isto para `None`, o texto genérico reaparece.
#
# O que havia antes era pior: a Aula 04 mandava clonar
# `github.com/dobidu/sintonia.git`, que é o repositório do sistema-base
# ANTERIOR - o estudante seguiria a instrução e receberia o projeto errado.
REPOSITORIO = "https://github.com/dobidu/poo262"

CALLOUTS = {
    "warn":     dict(rot="ATENÇÃO",   glifo="▲", classe_v1="callout-warn"),
    "llm":      dict(rot="LLM",       glifo="◇", classe_v1="callout-llm"),
    "tip":      dict(rot="DICA",      glifo="✓", classe_v1="callout-tip"),
    "info":     dict(rot="NOTA",      glifo="·", classe_v1="callout-info"),
    "deriva":   dict(rot="DERIVA",    glifo="▸", classe_v1="callout-sintonia"),
}


# ---------------------------------------------------------------------------
# A rubrica de revisão de código OO gerado por IA (Aula 04)
#
# Ela existia em TRÊS lugares com numerações diferentes: a tabela do Cap. 04 do
# livro, a lista da página do site, e os rótulos `R1`..`R7` nos comentários do
# código com defeitos plantados. Um material que numera o próprio instrumento
# de três maneiras não é rigoroso, é amador - e a numeração é justamente o que
# se cita em prova.
#
# Esta é a única definição. O site a lê daqui, e
# `build/verifica_numeros.py` recusa o build se os rótulos usados em
# `poo/js/pecas-extra.js` ou em `exemplos/deriva/revisao_ia/` divergirem.
#
# A ordem é a da tabela do livro, que é a mais útil: cada item tem uma
# PERGUNTA, que se responde por leitura, e um INSTRUMENTO, que confirma a
# resposta sem depender de sanitizer.
# ---------------------------------------------------------------------------
RUBRICA = [
    dict(id="R1", titulo="Posse",
         pergunta="Quem possui cada recurso, e em que linha ele é liberado? Há um "
                  "`delete[]` para cada `new[]` - ou, melhor, nenhum dos dois?",
         instrumento="O contador `vivos` fecha em zero no fim de `main`",
         capitulos=[7, 12, 13],
         costuma_aparecer="contêiner público com posse; `delete` no código do "
                          "estudante; `shared_ptr` onde bastava `unique_ptr`"),
    dict(id="R2", titulo="Operações especiais",
         pergunta="Se há destrutor, há também cópia e atribuição, ou as duas estão "
                  "`= delete`? A regra do zero não resolveria melhor?",
         instrumento="Traço de ciclo de vida: a cópia que ninguém pediu aparece nele, "
                     "e o contador acusa a que sobrou",
         capitulos=[8, 9, 14],
         costuma_aparecer="destrutor declarado e cópia esquecida - cópia rasa silenciosa"),
    dict(id="R3", titulo="const-correctness",
         pergunta="Todo método que não altera o objeto é `const`? Todo parâmetro só de "
                  "leitura é `const&` ou `string_view`? Nenhum acesso devolve "
                  "referência não-const a membro privado?",
         instrumento="O compilador: chame o método num objeto `const` e veja se recusa",
         capitulos=[3, 7],
         costuma_aparecer="getter não-const; retorno ignorado sem `[[nodiscard]]`"),
    dict(id="R4", titulo="Limites e ausência",
         pergunta="Todo índice é verificado, ou a pré-condição está escrita e quem "
                  "chama a cumpre? Ausência de resultado é `std::optional`, e não "
                  "valor mágico?",
         instrumento="Teste que passa índice de fronteira; `optional` no lugar de -1",
         capitulos=[3, 20],
         costuma_aparecer="índice sem verificação e sem pré-condição escrita; -1 como "
                          "\"não achei\""),
    dict(id="R5", titulo="Hierarquia",
         pergunta="Base com método virtual tem destrutor virtual? Toda sobrescrita "
                  "está marcada `override`?",
         instrumento="`gdb` com ponto de parada no destrutor da derivada: sem "
                     "`virtual`, ele não é alcançado",
         capitulos=[2, 11],
         costuma_aparecer="hierarquia sem `~base()` virtual - o teste passa e o objeto "
                          "vaza, e com `unique_ptr` nem aviso aparece"),
    dict(id="R6", titulo="Invariante e estado",
         pergunta="O construtor estabelece a invariante, e nenhum método público a "
                  "deixa quebrada no retorno? Nada lê o objeto de origem depois de um "
                  "`std::move`?",
         instrumento="Um caso que viola a invariante por fora e um que lê a origem "
                     "movida: os dois têm de ser impossíveis ou recusados",
         capitulos=[7, 14],
         costuma_aparecer="campo público mutável; `assert(origem.empty())` depois do move"),
    dict(id="R7", titulo="Prova e justificativa",
         pergunta="O teste falha se o comportamento mudar - e não se a implementação "
                  "mudar? Cada função de biblioteca chamada existe, com essa "
                  "assinatura, em C++17? Para cada decisão aceita há uma frase que a "
                  "sustenta, escrita por quem entrega?",
         instrumento="`DECISAO.md` na entrega, e o `make verifica` verde antes dela",
         capitulos=[16, 24],
         costuma_aparecer="teste que afirma detalhe interno; função de C++20 chamada "
                          "como se fosse C++17; nenhuma justificativa escrita"),
]

# Qual item pega cada defeito plantado em `exemplos/deriva/revisao_ia/`.
# O código carrega estes rótulos nos comentários, e o portão os confere.
DEFEITOS_PLANTADOS = {
    1: "R1",   # vetor público com posse: a invariante fica contornável de fora
    2: "R5",   # destrutor não virtual na base polimórfica
    3: "R3",   # nome() sem const, sem [[nodiscard]], devolvendo cópia
}
# E o item que o teste que veio com o código gerado deixa de cobrir.
DEFEITO_DO_TESTE = "R7"


def rubrica(item_id):
    for r in RUBRICA:
        if r["id"] == item_id:
            return r
    raise KeyError(item_id)


SEMESTRE = "2026.2"
AUTOR = "Carlos Eduardo C. F. Batista"
EMAIL = "bidu@ci.ufpb.br"
PADRAO = "C++17"

# A extensão do livro composto. Estava digitada à mão na capa do site ("As
# 299 páginas") e desencontrada no PRODUCT.md (283, de antes da composição
# final). Aqui ela é declarada uma vez, e `build/verifica_pdf.py` recusa o
# PDF que não tiver este número - a mesma regra dos outros números do
# material: declarado na tabela, conferido contra o artefato.
PAGINAS_LIVRO = 299


def aula(n):
    for a in AULAS:
        if a["n"] == n:
            return a
    raise KeyError(n)


def por_unidade(u):
    return [a for a in AULAS if a["unidade"] == u]


def unidade(u):
    for x in UNIDADES:
        if x["n"] == u:
            return x
    raise KeyError(u)


def versoes_da_aula(n):
    return [t for t in TRILHA if n in t.get("aula", [])]


def quebradas():
    return [(t["v"], t["quebrada"]) for t in TRILHA if t.get("quebrada")]


def verificar():
    """Invariantes do mapa. Roda no build: mapa quebrado não gera site."""
    erros = []
    if len(AULAS) != 26:
        erros.append(f"esperadas 26 aulas, há {len(AULAS)}")
    ns = [a["n"] for a in AULAS]
    if ns != list(range(1, 27)):
        erros.append("numeração de aula não é 1..26 contígua")
    for a in AULAS:
        u = a["unidade"]
        if a["n"] not in unidade(u)["aulas"]:
            erros.append(f"aula {a['n']} fora da faixa da unidade {u}")
        for i in a["interativos"]:
            if i not in INTERATIVOS:
                erros.append(f"aula {a['n']}: interativo desconhecido {i!r}")
            elif a["n"] not in INTERATIVOS[i]["aulas"]:
                erros.append(f"aula {a['n']}: {i} não a lista em INTERATIVOS")
    for k, d in INTERATIVOS.items():
        for n in d["aulas"]:
            if k not in aula(n)["interativos"]:
                erros.append(f"INTERATIVOS[{k!r}] cita aula {n}, que não o lista")
    obrig = [t for t in TRILHA if not t.get("opcional")]
    if len(obrig) != 20:
        erros.append(f"a trilha deve ter 20 versões obrigatórias, tem {len(obrig)}")
    for t in TRILHA:
        for n in t.get("aula", []):
            if aula(n)["deriva"] != t["v"]:
                erros.append(f"trilha {t['v']} ↔ aula {n} discordam")
    if len(RUBRICA) != 7:
        erros.append(f"a rubrica tem {len(RUBRICA)} itens, e o material diz sete")
    if [r["id"] for r in RUBRICA] != [f"R{i}" for i in range(1, 8)]:
        erros.append("os identificadores da rubrica não são R1..R7 em ordem")
    for n, rid in DEFEITOS_PLANTADOS.items():
        try:
            rubrica(rid)
        except KeyError:
            erros.append(f"defeito plantado {n} aponta para {rid}, que não existe")
    for r in RUBRICA:
        for c in r["capitulos"]:
            if not 1 <= c <= 26:
                erros.append(f"rubrica {r['id']}: capítulo {c} fora de 1..26")

    if len(LABS) != 12:
        erros.append(f"esperados 12 laboratórios, há {len(LABS)}")
    for l in LABS:
        if aula(l["aula"])["lab"] != l["id"]:
            erros.append(f"{l['id']} ↔ aula {l['aula']} discordam")
    conta = {}
    for l in LABS:
        u = aula(l["aula"])["unidade"]
        conta[u] = conta.get(u, 0) + 1
    if conta != LABS_POR_UNIDADE:
        erros.append(f"distribuição de laboratórios {conta} não bate com a do "
                     f"plano {LABS_POR_UNIDADE}")
    ids = [l["id"] for l in LABS]
    if ids != sorted(ids):
        erros.append("os laboratórios não estão em ordem crescente de aula")
    caps = sorted({c for a in AULAS for c in a["cap_v1"]})
    faltam = [c for c in range(1, 28) if c not in caps and c != 20]
    if faltam:
        erros.append(f"capítulos do v1 sem destino: {faltam}")
    return erros


if __name__ == "__main__":
    import sys
    e = verificar()
    for x in e:
        print("ERRO:", x)
    canonicos = [k for k, d in INTERATIVOS.items()
                 if not d.get("ferramenta") and not d.get("reaproveitado")]
    print(f"{len(AULAS)} aulas · {len(ANEXOS)} anexos · "
          f"{len([t for t in TRILHA if not t.get('opcional')])} versões (+1 opcional) · "
          f"{len(LABS)} laboratórios ({'/'.join(str(LABS_POR_UNIDADE[u['n']]) for u in UNIDADES)}) · "
          f"{len(canonicos)} tipos canônicos de interativo + corrida (LPII) + UML")
    sys.exit(1 if e else 0)
