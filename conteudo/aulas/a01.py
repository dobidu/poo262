# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-1/aula01-complexidade-oo
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Pendências desta aula: 0 (ver conteudo/PENDENCIAS.md)
"""

AULA = {
    'n': 1,
    'slug': 'a01',
    'titulo': 'Da programação procedural à orientação a objetos',
    'curto': 'Do procedural ao objeto',
    'unidade': 'I',
    'cap_v1': [
        1,
    ],
    'origem_v1': [
        'unidade-1/aula01-complexidade-oo',
    ],
    'fatia': None,
    'deriva': None,
    'lab': None,
    'interativos': [
        'refator',
    ],
    'nota_migracao': 'Exemplo comparativo migra de “Sistema de Alunos” para o Deriva.',
    'objetivos': [
        'Entender por que o software precisa de mecanismos para controlar complexidade',
        'Contrastar programação procedural com OO',
        'Identificar os quatro pilares da OO: encapsulamento, abstração, herança, polimorfismo',
        'Situar C++ no cenário de linguagens OO',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Gerenciamento de Complexidade e o Paradigma OO',
            'origem': 'unidade-1/aula01-complexidade-oo',
            'compartilhado': False,
            'blocos': [],
        },
        {
            'id': 'complexidade',
            'titulo': 'Por que Complexidade é o Problema Central',
            'origem': 'unidade-1/aula01-complexidade-oo',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Software é a atividade humana com maior número de estados possíveis por unidade de volume. Um programa com 300 variáveis booleanas tem mais estados do que átomos no universo observável. Gerenciar essa complexidade é o problema central da engenharia de software.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Sintomas de complexidade descontrolada',
                    'paragrafos': [
                        'Código que ninguém entende sem o autor; módulos que quebram quando você toca em outro módulo; bugs que surgem em partes não modificadas; medo de alterar código existente.',
                    ],
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Técnica',
                        'Como reduz complexidade',
                        'Limitação',
                    ],
                    'linhas': [
                        [
                            'Decomposição procedural',
                            'Divide em funções',
                            'Estado global, acoplamento',
                        ],
                        [
                            'Módulos (C)',
                            'Agrupa funções relacionadas',
                            'Difícil representar estado por instância',
                        ],
                        [
                            'OO',
                            'Agrupa dados + comportamento + estado por objeto',
                            'Curva de aprendizado, overengineering',
                        ],
                    ],
                },
            ],
        },
        {
            'id': 'paradigmas',
            'titulo': 'Paradigmas de Programação',
            'origem': 'unidade-1/aula01-complexidade-oo',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Paradigma',
                        'Base',
                        'Exemplos',
                    ],
                    'linhas': [
                        [
                            'Procedural',
                            'Sequência de instruções, funções',
                            'C, Pascal, FORTRAN',
                        ],
                        [
                            'OO',
                            'Objetos com estado e comportamento',
                            'C++, Java, Python, Ruby',
                        ],
                        [
                            'Funcional',
                            'Funções puras, sem estado mutável',
                            'Haskell, Erlang, Clojure',
                        ],
                        [
                            'Multiparadigma',
                            'Combina paradigmas',
                            'C++17, Python, Rust',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'C++ é multiparadigma',
                    'paragrafos': [
                        'C++ suporta programação procedural (herança de C), OO (classes, herança, polimorfismo) e funcional (lambdas, std::function, algoritmos da STL). Isso é poder - e responsabilidade.',
                    ],
                },
            ],
        },
        {
            'id': 'quatro-pilares',
            'titulo': 'Os Quatro Pilares da OO',
            'origem': 'unidade-1/aula01-complexidade-oo',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Pilar',
                        'Definição',
                        'Benefício',
                    ],
                    'linhas': [
                        [
                            'Encapsulamento',
                            'Agrupar dados e operações; esconder implementação',
                            'Invariantes garantidas; interface estável',
                        ],
                        [
                            'Abstração',
                            'Expor apenas o essencial; esconder detalhes',
                            'Reduz carga cognitiva',
                        ],
                        [
                            'Herança',
                            'Reutilizar e especializar comportamento',
                            'Evita duplicação',
                        ],
                        [
                            'Polimorfismo',
                            'Mesmo código opera sobre tipos diferentes',
                            'Extensibilidade',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'Ordem de importância',
                    'paragrafos': [
                        'Encapsulamento e abstração são os mais importantes no dia a dia. Herança é a mais usada em excesso. Polimorfismo é o mais poderoso quando bem aplicado.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-1/aula01-complexidade-oo',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Explique o princípio de encapsulamento com um exemplo real em C++17. Mostre: (1) como a ausência de encapsulamento causa problemas, (2) como encapsulamento os resolve. Use snake_case e comentários em português."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'LLMs tendem a usar exemplos triviais demais (getter/setter puro), que não demonstram o valor real do encapsulamento. Peça invariante concreta, tal como a do construtor de <code>grade</code>: largura e altura positivas, e o vetor de células com exatamente largura × altura elementos.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Leia a grade em estilo C de <code>exemplos/deriva/comparativo/grade_procedural.hpp</code>, e as cinco regras que o comentário de cabeçalho dela lista. Para cada regra, descreva um cenário concreto em que a violação produziria um defeito difícil de encontrar, e diga se algum aviso do compilador o pegaria.',
            'origem': 'unidade-1/aula01-complexidade-oo',
        },
        {
            'n': '02',
            'html': 'Escreva, em papel e sem compilar, a declaração da classe que você poria no lugar de <code>struct grade_c { int largura; int altura; char* celulas; }</code>: quais membros ficam privados, quais métodos são <code>const</code>, e qual método você não escreveria por não haver invariante a proteger. Guarde a folha - na Aula 07 você a compara com <code>include/deriva/grade.hpp</code>.',
            'origem': 'unidade-1/aula01-complexidade-oo',
        },
        {
            'n': '03',
            'html': 'Pesquise: qual é a diferença entre <em>abstração de dados</em> (ADT) e <em>classe</em> em C++? Dê um exemplo de ADT que não é implementado como classe.',
            'origem': 'unidade-1/aula01-complexidade-oo',
        },
        {
            'n': '04',
            'html': 'A métrica desta aula não é elegância: é quantas maneiras de errar o desenho permite. Leia <code>maneiras_de_errar_em_c()</code> e <code>maneiras_de_errar_em_cpp()</code> em <code>exemplos/deriva/comparativo/grade_procedural.cpp</code>, e explique, uma por uma, as maneiras que a versão OO fecha - nomeando em cada caso o mecanismo da linguagem que a fecha, e não a disciplina de quem programa.',
            'origem': 'unidade-1/aula01-complexidade-oo',
        },
    ],
    'pendencias': [],
}
