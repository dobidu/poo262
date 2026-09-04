# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-1/aula03-classificacao-linguagens
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Pendências desta aula: 0 (ver conteudo/PENDENCIAS.md)
"""

AULA = {
    'n': 5,
    'slug': 'a05',
    'titulo': 'Classificação de linguagens e sistemas de tipos',
    'curto': 'Linguagens e sistemas de tipos',
    'unidade': 'I',
    'cap_v1': [
        3,
    ],
    'origem_v1': [
        'unidade-1/aula03-classificacao-linguagens',
    ],
    'fatia': None,
    'deriva': None,
    'lab': None,
    'interativos': [
        'virtual',
    ],
    'nota_migracao': 'Renumeração.',
    'objetivos': [
        'Distinguir linguagens baseadas em objetos de linguagens OO completas',
        'Comparar sistemas de tipos: estático vs. dinâmico, forte vs. fraco',
        'Compreender single dispatch vs. multiple dispatch',
        'Posicionar C++ no espectro de linguagens',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Classificação de Linguagens Baseadas em Objetos',
            'origem': 'unidade-1/aula03-classificacao-linguagens',
            'compartilhado': False,
            'blocos': [],
        },
        {
            'id': 'classificacao',
            'titulo': 'Baseada em Objetos vs. OO',
            'origem': 'unidade-1/aula03-classificacao-linguagens',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Característica',
                        'Baseada em Objetos',
                        'Orientada a Objetos',
                    ],
                    'linhas': [
                        [
                            'Encapsulamento',
                            'sim',
                            'sim',
                        ],
                        [
                            'Objetos e classes',
                            'sim',
                            'sim',
                        ],
                        [
                            'Herança',
                            'não',
                            'sim',
                        ],
                        [
                            'Polimorfismo',
                            'não',
                            'sim',
                        ],
                        [
                            'Exemplo',
                            'Ada 83, primeiras versões do Visual Basic',
                            'C++, Java, Python, Ruby, Smalltalk',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'JavaScript moderno é OO',
                    'paragrafos': [
                        'JavaScript com ES6+ tem herança via prototype chain e polimorfismo. É considerado OO - mas com um modelo diferente do C++. Python também é OO completo.',
                    ],
                },
            ],
        },
        {
            'id': 'tipos',
            'titulo': 'Sistemas de Tipos',
            'origem': 'unidade-1/aula03-classificacao-linguagens',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Dimensão',
                        'Opção A',
                        'Opção B',
                    ],
                    'linhas': [
                        [
                            'Quando checar',
                            'Estático (compilação)',
                            'Dinâmico (execução)',
                        ],
                        [
                            'Conversão implícita',
                            'Fraco (C)',
                            'Forte (Python, Haskell)',
                        ],
                        [
                            'Declaração',
                            'Explícita (C++)',
                            'Inferida (auto, var)',
                        ],
                    ],
                },
                {
                    'tipo': 'codigo',
                    'lang': 'cpp',
                    'legenda': 'C++ - tipagem estática e forte (com nuances)',
                    'codigo': """\
int x = 42;
// x = "hello"; // ERRO em compilação - sistema de tipos estático
auto y = 3.14;  // tipo inferido em compilação - ainda estático
float f = x;    // conversão implícita int→float - ponto fraco de C""",
                },
            ],
        },
        {
            'id': 'dispatch',
            'titulo': 'Single vs. Multiple Dispatch',
            'origem': 'unidade-1/aula03-classificacao-linguagens',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Em C++, a resolução de método virtual depende <strong>apenas do tipo do receptor</strong> (single dispatch). Em linguagens com multiple dispatch (Julia, Common Lisp), depende dos tipos de todos os argumentos.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A diferença aparece quando a resposta depende de <strong>dois</strong> objetos, e no Deriva o caso é a colisão: sonda contra parede, sonda contra sonda, parede contra parede. A função <code>resolver(const colisao&amp;, const colisao&amp;)</code>, extraída mais abaixo nesta página, faz esse despacho à mão, perguntando o tipo de cada operando com <code>dynamic_cast</code> - justamente porque <code>virtual</code> responde por um só. O nome dela é a prova do ponto: se houvesse despacho múltiplo, ela não existiria.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Com N tipos, aquela função cresce com N², e é esse crescimento que faz o padrão Visitor existir. O contorno que C++17 oferece para o mesmo problema é <code>std::visit</code> sobre <code>std::variant</code>, que cobra em compilação o tratamento de todas as alternativas; a Aula 20 mostra onde isso ajuda e onde atrapalha.',
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-1/aula03-classificacao-linguagens',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Compare os sistemas de tipos de C++, Python e Java em uma tabela. Para cada um: estático/dinâmico, forte/fraco, single/multiple dispatch, garbage collected. Mostre um exemplo de erro de tipo em cada linguagem."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        "LLMs frequentemente classificam C++ como 'fortemente tipado' sem mencionar as conversões implícitas problemáticas (int→float→double) e os C-style casts que quebram a segurança de tipos.",
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Compile e teste: <code>int x = 42; void* p = &amp;x double* d = (double*)p; std::cout &lt;&lt; *d;</code>. O que acontece? Por que isso é um problema de sistema de tipos?',
            'origem': 'unidade-1/aula03-classificacao-linguagens',
        },
        {
            'n': '02',
            'html': 'Python é tipado dinamicamente mas fortemente tipado. Demonstre isso: mostre um erro que Python lança em tempo de execução por incompatibilidade de tipos, mas que C++ detectaria em compilação.',
            'origem': 'unidade-1/aula03-classificacao-linguagens',
        },
        {
            'n': '03',
            'html': 'Acrescente um terceiro tipo de <code>colisao</code> - um drone - a <code>exemplos/deriva/tipos/despacho.hpp</code> e estenda <code>resolver</code> para tratá-lo. Quantos ramos a função passa a ter? Depois implemente o mesmo despacho por Visitor e compare: qual das duas formas obriga o compilador a acusar o caso que você esqueceu?',
            'origem': 'unidade-1/aula03-classificacao-linguagens',
        },
        {
            'n': '04',
            'html': 'Pesquise: o que é <em>duck typing</em>? Compare com o uso de templates em C++, que é polimorfismo estático, e com <code>tem_glifo&lt;T&gt;</code> de <code>tipos/despacho.hpp</code>, que é um trait escrito à mão. Em que momento cada uma das três abordagens detecta que o tipo não serve?',
            'origem': 'unidade-1/aula03-classificacao-linguagens',
        },
    ],
    'pendencias': [],
}
