# -*- coding: utf-8 -*-
"""Reescrito à mão sobre o Deriva - não rode build/extrair_v1.py aqui.

Origem no site v1: unidade-2/aula16-heranca-multipla
Página inteira.
Este arquivo é a fonte de verdade do site v2 e do livro v2. O extrator do v1
sobrescreve o que está aqui; se precisar reextrair, faça em branch.
"""

AULA = {
    'n': 17,
    'slug': 'a17',
    'titulo': 'Herança múltipla e o diamante',
    'curto': 'Herança múltipla e o diamante',
    'unidade': 'II',
    'cap_v1': [
        16,
    ],
    'origem_v1': [
        'unidade-2/aula16-heranca-multipla',
    ],
    'fatia': None,
    'deriva': 'v1.7',
    'lab': None,
    'interativos': [
        'inspetor',
        'uml',
    ],
    'nota_migracao': 'Renumeração, e uma correção de fundo: a herança virtual NÃO economiza memória. Os três tamanhos estão medidos em `include/deriva/diamante.hpp`, e a primeira versão daquele cabeçalho trazia um `static_assert` invertido afirmando o contrário - o compilador o recusou. O que a herança virtual compra é correção, e é assim que o site passa a dizer.',
    'objetivos': [
        'Usar herança múltipla de interfaces puras sem ambiguidade',
        'Explicar o diamante pelo que ele faz ao estado, e não pelo que faz ao tamanho',
        'Resolver o diamante com herança <code>virtual</code>, e dizer o que ela custa',
        'Contrastar com Java e C#, que proíbem o caso e permitem as interfaces',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Herança múltipla e o problema do diamante',
            'origem': 'unidade-2/aula16-heranca-multipla',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v1.7 · a sonda_reparadora, e o diamante ao lado dela',
                    'paragrafos': [
                        'A v1.7 introduz <code>sonda_reparadora</code>, que herda de <code>sonda</code>, que é uma <code>entidade</code>, e da interface pura <code>i_reparavel</code>. É o caso fácil: <code>i_reparavel</code> não tem estado, então não há o que duplicar.',
                        'O caso difícil vive em <code>include/deriva/diamante.hpp</code>, que não entra no jogo e existe só para ser medido. Ele traz o diamante com estado nas três formas possíveis, lado a lado, para que os números sejam os que o compilador produz e não os que a intuição sugere.',
                        'Foi esta versão que obrigou <code>sonda</code> a deixar de ser <code>final</code>: o compilador recusou a derivação com "cannot derive from final base", e a palavra saiu.',
                    ],
                },
            ],
        },
        {
            'id': 'problema',
            'titulo': 'O problema do diamante, e o que ele faz ao estado',
            'origem': 'unidade-2/aula16-heranca-multipla',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'O diamante aparece quando uma classe herda de duas classes que já herdam de uma ancestral comum. Sem <code>virtual</code>, a folha recebe <strong>duas cópias</strong> do subobjeto ancestral, uma por ramo, e passa a ter dois campos com o mesmo nome, endereços diferentes e nenhuma relação entre eles.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'No cabeçalho de medida, a base do meio é <code>nucleo</code>, com um <code>int leituras</code> e uma função virtual; os ramos são <code>movel</code> e <code>sensor</code>; a folha é <code>patrulha_duplicada</code>. O diagrama manipulável desta forma, e das outras duas, está no interativo de diagrama de classes desta página, e o leiaute em memória, com os dois subobjetos, está no inspetor de objeto.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O defeito é a pergunta sem resposta, e não a ambiguidade de nome',
                    'paragrafos': [
                        'Escrever <code>p.leituras</code> na forma duplicada é erro de compilação, e erro de compilação é o caso <em>bom</em>: ele obriga a qualificar o ramo. O caso ruim é o programa que qualifica os dois e roda: escrever 7 por um ramo e 9 pelo outro deixa os dois valores lá, e a pergunta "quantas leituras esta patrulha fez" passa a não ter resposta boa. É esse o defeito, e o teste extraído desta aula o mede exatamente assim.',
                    ],
                },
            ],
        },
        {
            'id': 'solucao',
            'titulo': 'Herança virtual: um subobjeto só, e o que ela cobra por isso',
            'origem': 'unidade-2/aula16-heranca-multipla',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Escrevendo <code>virtual</code> na herança dos dois ramos, a ancestral passa a existir <strong>uma única vez</strong> na folha, por quantas rotas de herança houver. Escrever por um ramo e ler pelo outro devolve o mesmo valor, e a pergunta volta a ter resposta. O preço é uma indireção: cada ramo virtual carrega um ponteiro para localizar a base compartilhada, porque o deslocamento dela deixa de ser fixo no tipo do ramo.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Aqui está a correção que este material teve de fazer duas vezes, e que contraria a intuição de todo mundo: a herança virtual é <strong>maior</strong>, e não menor. Na medição do Deriva, <code>patrulha_duplicada</code> tem 40 bytes e <code>patrulha_unica</code>, que é a forma virtual, tem 48. O ponteiro que cada ramo passa a carregar custa mais do que duplicar a base que ele evita. Escrever que herança virtual "economiza memória" seria mentir, e a primeira versão daquele cabeçalho trazia um <code>static_assert</code> invertido afirmando isso - o compilador o recusou.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Forma',
                        'Subobjetos da base',
                        'Tamanho medido',
                        'O que se ganha',
                    ],
                    'linhas': [
                        [
                            '<code>patrulha_duplicada</code>',
                            '2, com endereços diferentes',
                            '40 bytes',
                            'nada: a pergunta fica sem resposta',
                        ],
                        [
                            '<code>patrulha_unica</code> (virtual)',
                            '1, compartilhado',
                            '48 bytes',
                            'um campo só, e correção',
                        ],
                        [
                            '<code>patrulha_composta</code>',
                            'não há diamante',
                            '56 bytes',
                            'nem a pergunta existe; é a recomendada',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'A base virtual é responsabilidade da classe mais derivada',
                    'paragrafos': [
                        'Com herança virtual, quem inicializa a base compartilhada é a folha, e não os ramos, mesmo que a folha não a declare na lista de herança. Os construtores dos ramos deixam de inicializá-la, porque nenhum dos dois pode saber se é o único. É a regra que mais surpreende, e a que mais aparece em código gerado por modelo de linguagem.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'A saída que o material recomenda é a terceira',
                    'paragrafos': [
                        '<code>patrulha_composta</code> troca o segundo ramo por um membro: nenhum diamante, nenhuma ambiguidade, e nenhuma pergunta sobre qual campo é o certo. Ela é a <strong>maior</strong> das três, com 56 bytes, e continua sendo a recomendada, porque o que se compra não é tamanho: é a ausência de uma pergunta que não tem resposta boa.',
                    ],
                },
            ],
        },
        {
            'id': 'ordem',
            'titulo': 'Ordem de construção e de destruição',
            'origem': 'unidade-2/aula16-heranca-multipla',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A ordem é: bases virtuais primeiro, depois as bases não virtuais na ordem em que a lista de herança as declara, depois os membros na ordem de declaração, e por último o corpo do construtor. A destruição percorre o inverso exato. A base virtual roda uma vez, e é isso que a distingue da forma duplicada, onde ela roda duas.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O que decide a ordem é a <strong>lista de herança</strong>, e não a lista de inicialização: escrever os inicializadores em outra ordem não muda nada na execução, e o <code>-Wreorder</code>, que o <code>-Wall</code> do portão já liga, avisa quando as duas divergem. No construtor de <code>sonda_reparadora</code> a ordem está escrita como comentário ao lado do código, e o trecho extraído abaixo a mostra.',
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'Como se prova que nenhum destrutor da cadeia faltou',
                    'paragrafos': [
                        'Uma <code>sonda_reparadora</code> conta em dois contadores, o dela e o de <code>sonda</code>, porque ela também é uma sonda. Os dois voltam a zero no fim do escopo, e é essa a prova, feita sem sanitizer e sem Valgrind. Se o destrutor de <code>sonda</code> deixasse de rodar, o contador dela ficaria em um, e nenhum aviso apareceria.',
                    ],
                },
            ],
        },
        {
            'id': 'contraste',
            'titulo': 'Contraste com Java e C#, e o único uso sem ressalva',
            'origem': 'unidade-2/aula16-heranca-multipla',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Java e C# eliminam o problema proibindo a causa: uma classe herda de uma só classe, e implementa quantas interfaces quiser. A interface daquelas linguagens corresponde à classe puramente abstrata de C++, e a razão de a proibição não doer é que interface não tem estado: sem estado, não há o que duplicar, e o diamante que ela formaria é inofensivo.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'É por isso que interface pura é o único uso de herança múltipla que este material recomenda sem ressalva, e é a forma de <code>i_reparavel</code>: nenhum dado, nenhum construtor, destrutor virtual, e funções puramente virtuais. Herança múltipla de classes <em>com estado</em> exige a pergunta do diamante, e a resposta preferida continua sendo composição.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Aspecto',
                        'Sem virtual',
                        'Com virtual',
                    ],
                    'linhas': [
                        [
                            'Subobjetos da base do meio',
                            '2, um por rota',
                            '1, compartilhado',
                        ],
                        [
                            'Acesso sem qualificar o ramo',
                            'ambíguo: erro de compilação',
                            'sem ambiguidade',
                        ],
                        [
                            'Quem inicializa a base',
                            'cada ramo, uma vez cada',
                            'a classe mais derivada, uma vez',
                        ],
                        [
                            'Tamanho da folha, medido',
                            '40 bytes',
                            '48 bytes',
                        ],
                        [
                            'O que se paga',
                            'estado duplicado, e a pergunta sem resposta',
                            'um ponteiro por ramo virtual',
                        ],
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs e herança múltipla',
            'origem': 'unidade-2/aula16-heranca-multipla',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'O que o LLM costuma errar aqui',
                    'paragrafos': [
                        'Pedido um diamante, o modelo erra em três lugares com frequência: esquece o <code>virtual</code> na herança dos ramos intermediários; não inicializa a base virtual no construtor da folha, e deixa o compilador escolher o construtor padrão dela quando existe um; e afirma, na explicação que vem junto, que a herança virtual economiza memória.',
                        'A terceira é a mais perigosa das três, porque o código compila, roda e passa nos testes, e a afirmação falsa embarca na sua cabeça e não no programa. Meça: <code>sizeof</code> das três formas responde em tempo de compilação, e o Deriva o afirma em <code>static_assert</code>.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Prompt para testar o LLM',
                    'paragrafos': [
                        '<em>"Em C++17, snake_case: escreva um diamante com estado na base do meio, nas três formas - duplicada, com herança virtual e com composição no lugar do segundo ramo. Para cada uma, afirme <code>sizeof</code> em <code>static_assert</code> e diga qual campo é lido quando se escreve por um ramo e se lê pelo outro. Não me diga qual é a menor: mostre."</em>',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Antes de compilar, escreva a ordem completa de construção e de destruição de uma <code>sonda_reparadora</code>. Depois confira contra o teste extraído desta aula, e explique por que a ordem não muda se você reordenar a lista de inicialização do construtor.',
            'origem': 'unidade-2/aula16-heranca-multipla',
        },
        {
            'n': '02',
            'html': 'Retire <code>virtual</code> das heranças de <code>movel_v</code> e <code>sensor_v</code> e tente compilar. Que <code>static_assert</code> falha primeiro, e o que a mensagem dele diz? Depois escreva, sem rodar, quantos subobjetos <code>nucleo</code> a folha passa a ter.',
            'origem': 'unidade-2/aula16-heranca-multipla',
        },
        {
            'n': '03',
            'html': 'Acrescente um segundo campo a <code>nucleo</code> e preveja, antes de compilar, o novo tamanho das três formas. Depois meça, e explique cada diferença entre a sua previsão e o medido. A forma virtual continua sendo a maior das duas com diamante?',
            'origem': 'unidade-2/aula16-heranca-multipla',
        },
        {
            'n': '04',
            'html': 'Acrescente uma segunda interface pura ao Deriva, com uma capacidade que só algumas entidades têm, e faça uma classe implementar as duas. Rode <code>make verifica</code>: as quatro condições têm de continuar verdes, e nenhuma herança virtual deve ter sido necessária. Explique por quê.',
            'origem': 'unidade-2/aula16-heranca-multipla',
        },
    ],
    'pendencias': [],
}
