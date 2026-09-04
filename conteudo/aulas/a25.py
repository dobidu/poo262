# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-3/aula26-design-patterns
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Reescrito sobre o Deriva: os padrões saem de `include/deriva/apresentacao.hpp`,
`src/apresentacao.cpp`, `include/deriva/padroes.hpp`, `src/padroes.cpp` e
`src/inventario.cpp`.
"""

AULA = {
    'n': 25,
    'slug': 'a25',
    'titulo': 'Padrões de projeto canônicos em C++ moderno',
    'curto': 'Padrões de projeto',
    'unidade': 'III',
    'cap_v1': [
        26,
    ],
    'origem_v1': [
        'unidade-3/aula26-design-patterns',
    ],
    'fatia': None,
    'deriva': 'v2.6',
    'lab': None,
    'interativos': [
        'refator',
    ],
    'nota_migracao': 'Strategy com lambdas, não com herança; Command, State, Observer, Factory, Composite e Decorator sobre o Deriva; Singleton e seus problemas.',
    'objetivos': [
        'Reconhecer Command, State, Observer, Strategy, Factory Method, Composite, Decorator e Singleton em código que compila',
        'Dizer que problema cada padrão resolve, e o que ele cobra em troca',
        'Escrever Strategy como função em C++ moderno, e saber quando ela volta a ser classe',
        'Argumentar contra o Singleton com os custos dele, e não com preferência',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Padrões de projeto no Deriva',
            'origem': 'unidade-3/aula26-design-patterns',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v2.6 - os padrões que a refatoração produziu',
                    'paragrafos': [
                        'Nenhum padrão desta aula foi escolhido antes do problema. Todos saíram da refatoração da Aula 24: as sete responsabilidades do god class saíram uma por uma, e o que ficou no lugar de cada uma tem nome na literatura. Command está em <code>include/deriva/apresentacao.hpp</code>, junto com Observer e a interface de apresentação; State, Decorator e Singleton estão em <code>include/deriva/padroes.hpp</code>; Factory e Strategy, em <code>src/apresentacao.cpp</code>; Composite, em <code>src/inventario.cpp</code>.',
                        'A ordem importa para o argumento: padrão aplicado sem o problema na frente é <em>overengineering</em>, e o material mostra o problema primeiro em todos os oito casos.',
                    ],
                },
            ],
        },
        {
            'id': 'creacionais',
            'titulo': 'Factory Method e Singleton',
            'origem': 'unidade-3/aula26-design-patterns',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A fábrica do Deriva é <code>criar_por_glifo</code>, e o problema que ela resolve é o da terceira tabela: no god class, a tradução de glifo em classe concreta aparecia em três lugares, com <code>dynamic_cast</code>, e acrescentar uma entidade obrigava a editar os três. Com a fábrica, a tabela fica num lugar só, quem lê o mapa não conhece as classes concretas, e o glifo desconhecido devolve <code>nullptr</code>, porque glifo que não é entidade é terreno e o mapa cuida dele.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Repare no que a fábrica devolve: <code>std::unique_ptr&lt;entidade&gt;</code>, e não ponteiro cru. A posse vem declarada no tipo de retorno, de forma que quem chama recebe o dono e não uma dúvida - é a mesma decisão da Aula 12, agora num ponto onde a alternativa seria devolver <code>new</code> e escrever na documentação quem apaga.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O Singleton está no material para ser criticado, e a forma escrita é a de Meyers, que é a <strong>versão correta da forma errada</strong>: estático local dentro da função de acesso, cuja inicialização é garantidamente única e segura entre threads desde C++11. Escrever a versão correta é o que permite atacar o padrão, e não a implementação dele.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'O custo do Singleton',
                        'Como ele aparece',
                    ],
                    'linhas': [
                        [
                            'O teste não consegue substituí-lo',
                            'Quem o usa o pede por nome, e não há onde injetar outro',
                        ],
                        [
                            'Dois testes compartilham o estado dele',
                            'A ordem de execução passa a importar, e o segundo teste falha sozinho',
                        ],
                        [
                            'A ordem de destruição entre estáticos não se controla',
                            'Destrutor que usa outro estático global pode encontrá-lo já morto',
                        ],
                        [
                            'Esconde uma dependência que a assinatura deveria declarar',
                            'A função parece pura e não é; ninguém sabe disso lendo a chamada',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'A alternativa, e ela é de duas linhas',
                    'paragrafos': [
                        'A recomendação do material é <code>anotar_em(i_observador&amp; onde, std::string_view evento)</code>: a dependência entra por parâmetro, a chamada fica um argumento mais longa, e o teste substitui o destino sem cerimônia.',
                        'O contador <code>vivos</code> das Aulas 7 a 19 é estado global mutável, e este material o usa assim de propósito - como <strong>instrumento</strong>, e não como projeto. A diferença vale ser dita: o contador não participa da lógica do jogo, e nenhuma decisão do domínio depende dele.',
                    ],
                },
            ],
        },
        {
            'id': 'estruturais',
            'titulo': 'Decorator e Composite',
            'origem': 'unidade-3/aula26-design-patterns',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Um decorador implementa a <strong>mesma</strong> interface que decora e guarda um ponteiro para ela. No Deriva são dois, <code>com_numero_de_linha</code> e <code>com_moldura</code>, os dois implementando <code>i_apresentacao</code> e envolvendo outra <code>i_apresentacao</code> por <code>std::unique_ptr</code>. Empilhar os dois é empilhar comportamento sem herdar de nenhum deles, e a ordem da pilha é observável na saída.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A comparação com herança é o argumento inteiro: com herança, "numerado e com moldura" exigiria uma classe para cada combinação, e o número de classes cresce como o de subconjuntos das decorações. Com decorador, é a ordem em que se envolve, decidida em tempo de execução.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O Composite é a <code>mochila</code>, que é um <code>componente</code> que contém <code>componente</code>. Ela responde <code>massa</code> somando a tara com o que tem dentro, e responde <code>pecas</code> somando as peças de dentro, de forma que o <code>inventario</code> a trata como trata qualquer peça e não sabe a diferença. É por isso que <code>massa</code> é virtual na base desde a Aula 21, antes de o padrão ter nome nesta aula.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Composite e o ciclo',
                    'paragrafos': [
                        'Mochila dentro de si mesma é o vazamento da Aula 13 noutra forma: a soma de <code>massa</code> recorre para sempre, e o programa morre por pilha estourada em vez de por vazamento. A posse por <code>std::unique_ptr</code> torna o ciclo mais difícil de montar do que com <code>shared_ptr</code>, porque entregar a mochila para dentro dela mesma exige mover a única posse que existe, mas não o torna impossível.',
                        'Se o desenho precisar de referência de volta ao pai, ela é observação e não posse, e o tipo tem de dizer isso: ponteiro cru, ou <code>weak_ptr</code> quando o pai for compartilhado. É a mesma decisão do grafo da estação, na Aula 13.',
                    ],
                },
            ],
        },
        {
            'id': 'comportamentais',
            'titulo': 'Command, State, Observer e Strategy',
            'origem': 'unidade-3/aula26-design-patterns',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Command transforma a entrada em objeto: <code>i_comando</code> tem <code>executar</code>, <code>desfazer</code> e <code>nome</code>, e <code>mover_sonda</code> guarda de onde a sonda saiu, que é por isso que ela sabe voltar. O que se ganha não é elegância - é o desfazer, e um <code>switch</code> não tem onde guardar de onde a sonda veio. O <code>historico</code> é a pilha dos comandos aplicados, e o que não deu certo não entra nela.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'State é o par <code>i_tela</code> e <code>console</code>: cada tela responde ao comando por si, e <strong>a transição é o valor de retorno</strong>, um <code>std::unique_ptr&lt;i_tela&gt;</code> com a próxima tela, ou <code>nullptr</code> para ficar onde está. Devolver a próxima em vez de mutar um campo é o que impede duas telas de discordarem sobre qual está ativa. A alternativa é um enumerado mais um <code>switch</code> em cada função que reage a comando, e com quatro telas e cinco comandos são vinte casos espalhados que uma tela nova obriga a visitar.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Observer é <code>i_observador</code>, com um método só, <code>aconteceu</code>. O <code>mundo</code> avisa que algo aconteceu e não sabe quem escuta, e no god class ele chamava o log direto, abrindo arquivo, o que tornava o log intestável. <code>registro_em_memoria</code> é o observador que substitui o arquivo, e <code>testes/test_padroes.cpp</code> verifica o log sem caminho, sem permissão e sem limpeza depois.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Strategy é o caso em que C++ moderno se afasta do catálogo: a forma clássica é uma hierarquia <code>i_estrategia</code> com uma classe por comportamento, e aqui a estratégia é <strong>uma função</strong>, guardada em <code>std::function&lt;vetor2(const entidade&amp;, const mundo&amp;)&gt;</code>. As três que existem - patrulha, perseguição e parada - são lambdas devolvidas por função, e a regra para voltar a ser classe é objetiva: duas operações, ou estado próprio que precise sobreviver entre chamadas.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'A lambda devolvida captura por valor, e é obrigatório',
                    'paragrafos': [
                        '<code>estrategia_de_patrulha</code> captura o rumo <strong>por valor</strong>, e não é preferência de estilo: a lambda sobrevive à chamada que a criou, e capturar por referência deixaria uma referência a um parâmetro que já saiu de escopo. É a armadilha de tempo de vida do <code>std::string_view</code> da Aula 3, noutra roupa.',
                        'A regra prática que atravessa o semestre: lambda que morre na mesma expressão pode capturar por referência; lambda que é guardada, devolvida ou passada a outra thread captura por valor, e o que ela precisa guardar tem de ser copiável.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-3/aula26-design-patterns',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Implemente Chain of Responsibility sobre <code>i_comando</code>: cada tratador decide se executa o comando ou o passa adiante. Depois explique em que ele difere do Composite da <code>mochila</code> e do Decorator de <code>i_apresentacao</code>, e diga qual dos três eu deveria usar se o objetivo for registrar quanto tempo cada comando levou."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o modelo costuma errar',
                    'paragrafos': [
                        'Modelos confundem padrões parecidos com frequência: Decorator com Proxy, Composite com Facade, Factory Method com Abstract Factory. Peça a diferença entre dois deles <strong>antes</strong> de pedir a implementação, e a resposta já indica se vale seguir.',
                        'O segundo erro é mais específico de C++: eles produzem Strategy por hierarquia mesmo quando a estratégia é uma operação sem estado, porque o catálogo que aprenderam é de 1994 e não tinha <code>std::function</code>. E o terceiro é o Singleton oferecido como solução para "acesso global conveniente", sem nenhum dos quatro custos declarado.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Acrescente um segundo comando, <code>pegar_item</code>, implementando <code>i_comando</code> com desfazer que devolve o item ao chão. Prove por replay que executar e desfazer em cadeia devolve o despejo byte a byte ao estado inicial, como <code>testes/test_padroes.cpp</code> faz para <code>mover_sonda</code>.',
            'origem': 'unidade-3/aula26-design-patterns',
        },
        {
            'n': '02',
            'html': 'O <code>registro_global</code> de <code>padroes.hpp</code> usa estático local. Por que essa inicialização é segura entre threads a partir de C++11, e o que era necessário fazer antes disso? Em seguida escreva dois casos de teste que falham por compartilharem o estado dele, e reescreva-os com <code>anotar_em</code>.',
            'origem': 'unidade-3/aula26-design-patterns',
        },
        {
            'n': '03',
            'html': 'Escreva um terceiro decorador de <code>i_apresentacao</code> que registre quantas vezes <code>desenhar</code> foi chamado, sem modificar nenhuma classe existente. Depois empilhe os três em duas ordens diferentes e mostre na saída que a ordem é observável.',
            'origem': 'unidade-3/aula26-design-patterns',
        },
        {
            'n': '04',
            'html': 'O Template Method aparece em <code>entidade::descrever</code>, que é não-virtual e chama o virtual <code>glifo</code>. Identifique quem é a moldura e quem é o passo variável, e diga o que aconteceria se <code>descrever</code> fosse virtual também.',
            'origem': 'unidade-3/aula26-design-patterns',
        },
    ],
    'pendencias': [],
}
