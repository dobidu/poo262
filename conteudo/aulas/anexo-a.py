# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-3/aula20-concepts-ranges
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Reescrito sobre o Deriva. O código de C++20 vive em `exemplos/deriva/c20/`,
num alvo separado e opcional, e FORA de `make verifica` - por isso o anexo
descreve o mecanismo e aponta o arquivo, em vez de exibir bloco com o selo do
portão, que valeria para C++17 e não vale aqui.
"""

AULA = {
    'n': 0,
    'slug': 'anexo-a',
    'titulo': 'Concepts e Ranges',
    'curto': 'Concepts e Ranges (C++20)',
    'unidade': 'anexo',
    'cap_v1': [
        20,
    ],
    'origem_v1': [
        'unidade-3/aula20-concepts-ranges',
    ],
    'fatia': None,
    'deriva': 'v2.1 (opcional)',
    'lab': None,
    'interativos': [],
    'nota_migracao': 'Deixou de ser aula porque deixou de caber: são 20 minutos dentro da Aula 19. O conteúdo não foi descartado - mudou de estatuto. Nada no material obrigatório depende dele, e o alvo da disciplina segue C++17.',
    'objetivos': [],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Concepts e Ranges: o que vem depois do padrão-alvo',
            'origem': 'unidade-3/aula20-concepts-ranges',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Este anexo existe para dizer para onde a linguagem foi, sem que nenhum exemplo da disciplina passe a exigir C++20. A restrição é <strong>pedagógica</strong>, e não técnica: o laboratório tem g++ 13, que suporta os dois padrões, e o teto é C++17 porque quem está aprendendo objeto pela primeira vez não precisa de duas gramáticas de restrição de template ao mesmo tempo.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O código deste anexo está em <code>exemplos/deriva/c20/restricoes.hpp</code>, compila num alvo próprio com <code>-DDERIVA_COM_CPP20=ON</code>, e o arquivo recusa a compilação com um <code>#error</code> se o padrão for menor que C++20. Ele fica <strong>fora</strong> das quatro condições de <code>make verifica</code>, que são de C++17 - de forma que nada aqui está sob o portão, e é bom que se saiba.',
                },
            ],
        },
        {
            'id': 'concepts',
            'titulo': 'Concepts - a restrição com nome',
            'origem': 'unidade-3/aula20-concepts-ranges',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Um <code>concept</code> é um predicado sobre tipos, com nome, avaliado em compilação. O do anexo se chama <code>guardavel</code> e diz o que a <code>grade_de&lt;T&gt;</code> da Aula 19 já exigia por três <code>static_assert</code>: que <code>T</code> seja construível por padrão, que não seja referência, e que não seja <code>bool</code>. A <code>grade_restrita&lt;T&gt;</code> o usa na própria declaração do template, no lugar onde a versão de C++17 escreveria <code>enable_if</code> no tipo de retorno.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A diferença que se <strong>vê</strong> é a mensagem de erro, e é ela o argumento inteiro dos concepts. Com <code>static_assert</code>, o compilador aponta a linha do assert, dentro da definição do template, e o estudante lê a frase que o autor da classe escreveu. Com <code>concept</code>, ele aponta a <strong>chamada</strong> e diz qual restrição falhou, pelo nome dela - <code>guardavel</code>, e não uma expressão de <code>type_traits</code> desdobrada.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A restrição é verificável no próprio arquivo, por quatro <code>static_assert</code> que afirmam o que o <code>concept</code> aceita e o que ele recusa: <code>celula</code> e <code>int</code> passam, <code>bool</code> e <code>int&amp;</code> não. É a mesma técnica das Aulas 7 e 12 - a afirmação vive no código, e não na prosa.',
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'Concept não substitui static_assert em todo lugar',
                    'paragrafos': [
                        'Os dois respondem perguntas diferentes. <code>concept</code> restringe <strong>quem pode instanciar</strong> o template, e participa da resolução de sobrecarga: um tipo que não satisfaz o concept faz a sobrecarga sair da lista, em silêncio, o que é o que substitui SFINAE. <code>static_assert</code> afirma uma condição e <strong>quebra a compilação</strong> quando ela é falsa, o que é outro efeito.',
                        'É por isso que a Aula 19 continua com <code>static_assert</code> sem prejuízo: ela não precisa de sobrecarga condicional, precisa de mensagem de erro própria. Trocar por concept ali seria trocar de padrão para ganhar nada.',
                    ],
                },
            ],
        },
        {
            'id': 'ranges',
            'titulo': 'Ranges e views - composição sem contêiner intermediário',
            'origem': 'unidade-3/aula20-concepts-ranges',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Uma <em>view</em> não é contêiner: é uma vista sobre uma sequência, que não possui os elementos e não os copia. <code>std::views::filter</code> e <code>std::views::transform</code> devolvem vistas preguiçosas, e nada é calculado até alguém iterar - o que muda o custo do encadeamento inteiro.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A função <code>glifos_de_parede</code>, no arquivo do anexo, percorre as células de uma grade filtrando as de parede e tomando as primeiras, e o resultado sai de uma expressão só, com <code>|</code> ligando as vistas. Em C++17 o equivalente seria um <code>std::copy_if</code> para um vetor temporário e um percurso depois: dois laços e uma alocação, para o mesmo resultado.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Vista preguiçosa e tempo de vida',
                    'paragrafos': [
                        'A vista não possui os elementos, e é exatamente a armadilha do <code>std::string_view</code> da Aula 3 outra vez: guardar uma vista sobre um contêiner temporário deixa a vista pendurada sobre memória que já foi devolvida. A regra prática é a mesma - consuma a vista na mesma expressão em que a criou, ou garanta que a origem viva mais que ela.',
                    ],
                },
            ],
        },
        {
            'id': 'suporte',
            'titulo': 'Suporte de compiladores',
            'origem': 'unidade-3/aula20-concepts-ranges',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Recurso',
                        'GCC',
                        'Clang',
                        'MSVC',
                        'Estado',
                    ],
                    'linhas': [
                        [
                            'Concepts básicos',
                            '11+',
                            '12+',
                            '19.28+',
                            '✓ Estável',
                        ],
                        [
                            'Ranges e views',
                            '12+',
                            '13+',
                            '19.29+',
                            '✓ Estável',
                        ],
                        [
                            '<code>std::expected</code> (C++23)',
                            '12+',
                            '16+',
                            '19.34+',
                            '▲ Parcial',
                        ],
                        [
                            '<code>std::mdspan</code> (C++23)',
                            '13+',
                            '17+',
                            '-',
                            '▲ Parcial',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'O Deriva é C++17, e é teto',
                    'paragrafos': [
                        'O repositório declara <code>CXX_EXTENSIONS OFF</code> e alvo C++17, e código que só compila com <code>-std=gnu++17</code> não é C++17. Nenhuma das vinte versões da trilha depende deste anexo, e a v2.1, que seria a dele, é a única versão sem código obrigatório - de propósito.',
                        'Para estudar o que está aqui, configure o alvo opcional com <code>-DDERIVA_COM_CPP20=ON</code>. Ele compila com <code>-std=c++20</code>, e o que ele afirma vale para C++20, não para o portão da disciplina.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-3/aula20-concepts-ranges',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Esta classe é <code>grade_de&lt;T&gt;</code> em C++17, restrita por três <code>static_assert</code>. Converta as restrições para um <code>concept</code> de C++20 com nome, mantendo o comportamento, e mostre lado a lado a mensagem de erro que cada versão produz quando instanciada com <code>bool</code>."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o modelo costuma errar',
                    'paragrafos': [
                        'Modelos confundem os três mecanismos com frequência, e o pedido de C++17 é o teste mais rápido disso: SFINAE serve à seleção de sobrecarga, <code>concept</code> nomeia a restrição e participa da resolução, e <code>static_assert</code> afirma e quebra. Pedir código de C++17 e receber <code>concept</code> é o erro mais comum de todos neste tópico, e ele passa despercebido porque o código parece bom.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [],
    'pendencias': [],
    'c20': True,
}
