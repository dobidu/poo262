# -*- coding: utf-8 -*-
"""Reescrito à mão sobre o Deriva - não rode build/extrair_v1.py aqui.

Origem no site v1: unidade-2/aula15-heranca-simples
Página inteira.
Este arquivo é a fonte de verdade do site v2 e do livro v2. O extrator do v1
sobrescreve o que está aqui; se precisar reextrair, faça em branch.
"""

AULA = {
    'n': 10,
    'slug': 'a10',
    'titulo': 'Herança simples',
    'curto': 'Herança simples',
    'unidade': 'II',
    'cap_v1': [
        15,
    ],
    'origem_v1': [
        'unidade-2/aula15-heranca-simples',
    ],
    'fatia': None,
    'deriva': 'v1.0',
    'lab': None,
    'interativos': [
        'inspetor',
    ],
    'nota_migracao': 'Sobe cinco posições: passa à frente dos ponteiros inteligentes. A hierarquia do site passa a ser a do Deriva, `entidade` → `sonda`/`drone`/`item`, e os trechos de código saem de `include/deriva/entidade.hpp` por âncora.',
    'objetivos': [
        'Distinguir herança (is-a) de composição (has-a) por uma pergunta que se responde no domínio',
        'Implementar hierarquias com proteção de acesso correta',
        'Determinar a ordem de construção e de destruição de um objeto derivado a partir do texto',
        'Reconhecer quando herança é a escolha errada',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Herança simples: is-a, especialização e o subobjeto base',
            'origem': 'unidade-2/aula15-heranca-simples',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v1.0 · a hierarquia que o domínio pediu',
                    'paragrafos': [
                        'Hoje a estação ganha habitantes. <code>entidade</code> é a base, e dela derivam <code>sonda</code>, <code>drone</code> e <code>item</code>: três coisas que ocupam uma célula e desenham um glifo, e que se distinguem pelo que fazem no turno.',
                        'A hierarquia é a que o domínio pede, e não taxonomia montada para o exercício. A sonda gasta energia agindo, o drone anda em linha e inverte ao bater, e o item não age - <code>item</code> não sobrescreve <code>agir</code>, e essa omissão é a informação.',
                    ],
                },
            ],
        },
        {
            'id': 'is-a',
            'titulo': 'is-a, has-a e uses-a',
            'origem': 'unidade-2/aula15-heranca-simples',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A pergunta que decide não é sobre reuso de código, é sobre substituição: onde o programa espera uma <code>entidade</code>, uma <code>sonda</code> serve? Se serve, a relação é is-a, e herança pública a expressa. Se o que você quer é apenas usar a implementação de outra classe, a relação é has-a, e o membro por valor a expressa melhor.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Relação',
                        'Quando usar',
                        'Implementação C++17',
                        'No Deriva',
                    ],
                    'linhas': [
                        [
                            'is-a (herança)',
                            'B substitui A onde A é esperado',
                            '<code>class B : public A</code>',
                            '<code>sonda</code> é uma <code>entidade</code>',
                        ],
                        [
                            'has-a (composição)',
                            'B usa A internamente e não é um A',
                            'membro por valor',
                            '<code>mapa</code> tem uma <code>grade</code>',
                        ],
                        [
                            'uses-a (dependência)',
                            'B usa A só durante a chamada',
                            'parâmetro de método',
                            '<code>agir(mundo&amp;)</code>',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Herança não é ferramenta de reuso',
                    'paragrafos': [
                        'A razão certa para <code>sonda</code> derivar de <code>entidade</code> é o polimorfismo: o <code>mundo</code> guarda <code>entidade*</code> e trata as três derivadas pelo mesmo tipo de ponteiro. Se o que você quer é reaproveitar uma implementação, prefira composição ou função livre - herdar por reuso amarra dois tipos que o domínio não amarrou.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Onde o contador de instâncias mora',
                    'paragrafos': [
                        'O contador <code>vivos</code> da Aula 7 é escrito à mão em cada classe concreta, e não na base. Um contador na base contaria objetos e não tipos, e é justamente essa distinção que a Aula 11 usa para provar que o destrutor virtual rodou. A repetição das três cópias escritas à mão é o argumento do <code>contador_de_instancias&lt;T&gt;</code> da Aula 19.',
                    ],
                },
            ],
        },
        {
            'id': 'hierarquia',
            'titulo': 'A hierarquia do Deriva, classe por classe',
            'origem': 'unidade-2/aula15-heranca-simples',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A base declara o que toda entidade tem, que é uma posição, e o que toda entidade responde, que é glifo e nome. <code>glifo()</code> e <code>nome()</code> são puramente virtuais, então <code>entidade</code> não se instancia; <code>agir(mundo&amp;)</code> é virtual com corpo vazio, porque existir sem agir é caso legítimo no domínio. O diagrama manipulável desta hierarquia está no interativo de UML da Aula 6, e o leiaute em memória, com o subobjeto base, está no inspetor de objeto desta página.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Classe',
                        'Deriva de',
                        'Glifo',
                        'O que faz no turno',
                    ],
                    'linhas': [
                        [
                            '<code>entidade</code>',
                            '-',
                            'puramente virtual',
                            'abstrata: não se instancia',
                        ],
                        [
                            '<code>sonda</code>',
                            '<code>entidade</code>',
                            '<code>@</code>',
                            'age e gasta energia',
                        ],
                        [
                            '<code>drone</code>',
                            '<code>entidade</code>',
                            '<code>d</code>',
                            'anda em linha e inverte ao bater',
                        ],
                        [
                            '<code>item</code>',
                            '<code>entidade</code>',
                            '<code>!</code>',
                            'não age: herda o corpo vazio da base',
                        ],
                        [
                            '<code>sonda_reparadora</code>',
                            '<code>sonda</code> e <code>i_reparavel</code>',
                            '<code>R</code>',
                            'chega na v1.7, na Aula 17',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'O `final` que teve de sair',
                    'paragrafos': [
                        'Na v1.0 a classe <code>sonda</code> era <code>final</code>, porque nada derivava dela e a palavra documentava a intenção. A v1.7 introduziu <code>sonda_reparadora</code>, e o compilador recusou com "cannot derive from final base". A palavra saiu, e a lição fica: <code>final</code> é promessa, e retirá-la é admitir que a hierarquia mudou de forma. Quem dependia da classe ser folha perde a garantia nesse instante.',
                    ],
                },
            ],
        },
        {
            'id': 'destrutor',
            'titulo': 'Ordem de construção, ordem de destruição, e o destrutor da base',
            'origem': 'unidade-2/aula15-heranca-simples',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Construir uma <code>sonda</code> constrói primeiro o subobjeto <code>entidade</code>, depois os membros na ordem de declaração, e só então roda o corpo do construtor da derivada. Destruir percorre o inverso exato. A consequência que a prova cobra: quando o construtor da base roda, a parte derivada ainda não existe, e por isso um método virtual chamado de dentro do construtor da base despacha para a versão <strong>da base</strong>.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A base declara <code>virtual ~entidade() = default</code>, e o trecho extraído logo abaixo mostra a declaração no contexto. A razão de ela ser virtual é o assunto da Aula 11, onde a ausência da palavra é medida na variante <code>v1.1-quebrada</code>; aqui basta fixar a regra: classe com função virtual tem destrutor virtual.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'A base polimórfica não se copia por valor',
                    'paragrafos': [
                        '<code>entidade</code> declara construtor de cópia e atribuição como <code>= delete</code>. Copiar por <code>entidade&amp;</code> copiaria só a parte base e descartaria o resto do objeto, que é o fatiamento. A cópia correta de uma hierarquia é uma função virtual <code>clonar</code>, e a Aula 25 a transforma em padrão.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-2/aula15-heranca-simples',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Em C++17, snake_case: escreva a base abstrata <code>entidade</code>, com posição, <code>glifo()</code> e <code>nome()</code> puramente virtuais e <code>agir(mundo&amp;)</code> virtual com corpo vazio, e três derivadas concretas. Marque as sobrescritas com <code>override</code>, declare o destrutor virtual e recuse a cópia da base."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'Três erros aparecem com frequência: o destrutor da base sai não virtual; membros que ninguém precisa de fora viram <code>protected</code>, o que abre o encapsulamento para toda a hierarquia; e a base fica copiável, o que deixa o fatiamento acontecer em silêncio. Os itens R2 e R5 da rubrica são as perguntas que pegam os três.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Escreva, sem compilar, a ordem completa de construção e de destruição de um <code>drone</code>: subobjeto base, membros, corpo. Depois confira contra <code>testes/test_ciclo_de_vida.cpp</code>, que afirma a ordem em vez de imprimi-la para você conferir a olho.',
            'origem': 'unidade-2/aula15-heranca-simples',
        },
        {
            'n': '02',
            'html': 'Acrescente ao Deriva uma quarta derivada de <code>entidade</code>, com glifo próprio e sem sobrescrever <code>agir</code>. Rode <code>make verifica</code>: as quatro condições do portão têm de continuar verdes, e o contador de instâncias vivas da sua classe tem de fechar em zero.',
            'origem': 'unidade-2/aula15-heranca-simples',
        },
        {
            'n': '03',
            'html': 'Demonstre o fatiamento: tente declarar <code>std::vector&lt;deriva::entidade&gt;</code>. O compilador recusa, e a mensagem cita duas razões diferentes. Diga quais são, e explique por que <code>std::vector&lt;std::unique_ptr&lt;entidade&gt;&gt;</code>, que é o que o <code>mundo</code> usa, não tem nenhuma delas.',
            'origem': 'unidade-2/aula15-heranca-simples',
        },
        {
            'n': '04',
            'html': 'Marque <code>drone</code> como <code>final</code> e escreva uma classe que derive dele. Leia a mensagem do compilador, e depois explique por que <code>sonda</code> deixou de ser <code>final</code> na v1.7 e o que se perdeu junto com a palavra.',
            'origem': 'unidade-2/aula15-heranca-simples',
        },
    ],
    'pendencias': [],
}
