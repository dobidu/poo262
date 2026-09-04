# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-3/aula19-templates-crtp, unidade-3/aula20-concepts-ranges
Fatia: absorve-20 - o Cap. 20 entra comprimido em 20 minutos e rotulado C++20; o conteúdo integral vira o Anexo A
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Reescrito sobre o Deriva: o domínio do v1 saiu, e o código desta aula é o que
`build/extrair_codigo.py` recorta de `include/deriva/grade_generica.hpp` e de
`include/deriva/contador_crtp.hpp`.
"""

AULA = {
    'n': 19,
    'slug': 'a19',
    'titulo': 'Templates, polimorfismo estático e CRTP',
    'curto': 'Templates, CRTP e contador_de_instancias<T>',
    'unidade': 'III',
    'cap_v1': [
        19,
        20,
    ],
    'origem_v1': [
        'unidade-3/aula19-templates-crtp',
        'unidade-3/aula20-concepts-ranges',
    ],
    'fatia': [
        'absorve-20',
        'o Cap. 20 entra comprimido em 20 minutos e rotulado C++20; o conteúdo integral vira o Anexo A',
    ],
    'deriva': 'v2.0',
    'lab': 'LAB-10',
    'interativos': [
        'expansor',
    ],
    'nota_migracao': 'if constexpr no lugar de SFINAE. O CRTP ganha alvo concreto: generalizar em contador_de_instancias<T> o que foi escrito à mão em três classes desde a Aula 7. A repetição anterior é o argumento do template.',
    'objetivos': [
        'Escrever template de função e de classe em C++17',
        'Restringir o parâmetro de tipo com <code>static_assert</code>, de forma que a mensagem de erro seja a sua e não a da biblioteca',
        'Usar <code>if constexpr</code> para podar em compilação o ramo que não vale para um <code>T</code>',
        'Reconhecer o CRTP em <code>contador_de_instancias&lt;T&gt;</code> e dizer o que ele custa em tempo de execução',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Templates de classe e CRTP',
            'origem': 'unidade-3/aula19-templates-crtp',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v2.0 - grade_de<T> e contador_de_instancias<T>',
                    'paragrafos': [
                        'A <code>grade</code> da v0.2 ganha um parâmetro de tipo e passa a ser <code>grade_de&lt;T&gt;</code>, em <code>include/deriva/grade_generica.hpp</code>. O que motivou generalizar não foi elegância: a v2.3 precisa de uma grade de <code>int</code> para o mapa de distâncias do campo de visão, e a v2.5 de uma grade de <code>char</code> para o que já foi visitado, de forma que a alternativa ao template seria copiar a classe três vezes.',
                        'Junto com ela, o contador de instâncias vivas, escrito à mão desde a Aula 7 em <code>sonda</code>, <code>drone</code>, <code>item</code>, <code>mapa</code>, <code>terminal_bruto</code> e <code>no_estacao</code>, é generalizado em <code>contador_de_instancias&lt;T&gt;</code>, em <code>include/deriva/contador_crtp.hpp</code>. A repetição das doze aulas anteriores era deliberada, e é ela o argumento deste template: quem escreveu a sexta cópia à mão entende por que generalizar.',
                    ],
                },
            ],
        },
        {
            'id': 'templates',
            'titulo': 'Template de função e de classe',
            'origem': 'unidade-3/aula19-templates-crtp',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Um template não é uma classe: é a receita a partir da qual o compilador escreve uma classe por tipo usado. <code>grade_de&lt;celula&gt;</code> e <code>grade_de&lt;int&gt;</code> são dois tipos distintos, sem parentesco nenhum entre si, e cada um só passa a existir no ponto em que alguém o instancia. Daí a regra prática que o Deriva obedece: a definição do template mora no cabeçalho, porque quem instancia precisa vê-la.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A <code>grade_de&lt;T&gt;</code> <strong>convive</strong> com a <code>grade</code> não genérica em vez de substituí-la, e a convivência é a decisão de projeto: generalizar não é obrigação retroativa, e reescrever as dezoito aulas anteriores para provar um ponto de template custaria mais do que o ponto vale. O apelido <code>grade_de_celulas</code> existe para que o caso comum continue com nome curto.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'As restrições vêm por <code>static_assert</code>, e ficam <strong>na definição</strong> e não no uso: assim, quem instancia com o tipo errado lê a frase que escrevemos, e não seiscentas linhas de instanciação. São três, e a terceira é a interessante - <code>grade_de&lt;bool&gt;</code> é recusada de propósito, porque <code>std::vector&lt;bool&gt;</code> empacota os bits e o <code>operator[]</code> dele devolve um proxy em vez de <code>bool&amp;</code>. Uma grade que promete <code>T&amp;</code> não pode ser instanciada com <code>bool</code>, e a saída é <code>char</code>, que é o que a v2.5 usa.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'if constexpr no lugar de SFINAE',
                    'paragrafos': [
                        'O despejo de <code>grade_de&lt;T&gt;</code> depende do que <code>T</code> é, e a decisão acontece em compilação. Com <code>if</code> comum, os ramos teriam de ser válidos para todo <code>T</code>, e <code>c.glifo</code> não existe em <code>int</code>, de forma que o código nem compilaria. O <code>if constexpr</code> de C++17 descarta o ramo não escolhido antes de ele precisar fazer sentido, e é por isso que ele substitui o SFINAE que o material antigo ensinava.',
                    ],
                },
            ],
        },
        {
            'id': 'crtp',
            'titulo': 'CRTP - polimorfismo estático, sem vtable',
            'origem': 'unidade-3/aula19-templates-crtp',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'CRTP é o padrão em que a classe derivada aparece como argumento de template da própria base: <code>peca</code> herda de <code>contador_de_instancias&lt;peca&gt;</code>. Parece circular e não é - a base é instanciada com um tipo que, naquele ponto, ainda está incompleto, e isso basta porque ela não usa nada de dentro dele.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O truque está no parâmetro <code>T</code>: cada instanciação de <code>contador_de_instancias&lt;X&gt;</code> é um tipo diferente, logo tem os seus próprios <code>vivos</code> e <code>criados</code>. Herança comum não faria isso, porque uma base não-template compartilharia um contador só entre todas as derivadas - que é exatamente o erro que um contador colocado em <code>entidade</code> cometeria, e a razão pela qual a Aula 11 o deixou fora da base.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Nada ali é virtual, e é isso que faz o polimorfismo ser <strong>estático</strong>: a chamada é resolvida em compilação, não há indireção em tempo de execução, e o objeto não cresce, porque não há vtable. O <code>static_assert</code> ao pé de <code>grade_generica.hpp</code> é quem afirma isso, comparando o <code>sizeof</code> da grade com a soma dos membros dela.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O destrutor da base do CRTP não é virtual, e isso é escolha',
                    'paragrafos': [
                        'O construtor e o destrutor de <code>contador_de_instancias&lt;T&gt;</code> são protegidos, e o destrutor não é virtual: esta base não existe para ser usada por ponteiro, e por isso não paga o que a Aula 11 cobrou de <code>entidade</code>. Quem herda dela e é base polimórfica declara o <strong>seu</strong> destrutor virtual, como <code>entidade</code> faz.',
                        'Repare também no construtor de cópia: ele incrementa <code>criados</code>, porque cópia é nascimento. O contador manual esquecia disso em algumas classes, e o template passa a acertar em todas de uma vez.',
                    ],
                },
            ],
        },
        {
            'id': 'static-vs-dynamic',
            'titulo': 'Estático contra dinâmico: o que cada um cobra',
            'origem': 'unidade-3/aula19-templates-crtp',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Aspecto',
                        'Polimorfismo dinâmico',
                        'Polimorfismo estático (CRTP)',
                    ],
                    'linhas': [
                        [
                            'Custo por chamada',
                            'Uma indireção pela vtable',
                            'Nenhuma: resolvido em compilação',
                        ],
                        [
                            'Tamanho do objeto',
                            'Mais o ponteiro da vtable',
                            'Base vazia, e o objeto não cresce',
                        ],
                        [
                            'Tamanho do binário',
                            'Uma cópia do código',
                            'Uma instanciação por <code>T</code>',
                        ],
                        [
                            'Tempo de compilação',
                            'Curto',
                            'Cresce com o número de tipos',
                        ],
                        [
                            'Extensão em tempo de execução',
                            'Sim, por ponteiro para a base',
                            'Não: os tipos são fixos em compilação',
                        ],
                        [
                            'Onde está no Deriva',
                            'A hierarquia <code>entidade</code> e a interface <code>i_apresentacao</code>',
                            '<code>grade_de&lt;T&gt;</code> e <code>contador_de_instancias&lt;T&gt;</code>',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'As duas formas estão no mesmo repositório e não competem: as classes das Aulas 7 a 18 continuam com o contador manual, de propósito, porque o material precisa das duas escritas lado a lado para que a comparação seja possível. <code>testes/test_generico.cpp</code> prova que se comportam igual, e é essa prova que autoriza a troca.',
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-3/aula19-templates-crtp',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Escreva um template C++17 <code>anel&lt;T, N&gt;</code> de capacidade fixa em compilação, com <code>N</code> como parâmetro não-tipo. Quero <code>empurrar</code>, <code>puxar</code>, <code>tamanho</code> e <code>vazio</code>, um <code>static_assert</code> para <code>N &gt; 0</code> e a definição inteira no cabeçalho. Não use concepts: o alvo é C++17."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o modelo costuma errar',
                    'paragrafos': [
                        'Com templates, três erros aparecem quase sempre: usar concepts de C++20 quando o pedido é C++17, pôr a definição num <code>.cpp</code> em vez do cabeçalho, e escrever a restrição no uso em vez da definição, de forma que a mensagem de erro volta a ser a da biblioteca. Confira os três antes de olhar a lógica.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Instancie <code>grade_de&lt;T&gt;</code> para <code>celula</code>, <code>int</code>, <code>char</code>, <code>double</code> e <code>bool</code>. Qual dos <code>static_assert</code> de <code>grade_generica.hpp</code> recusa cada caso que falha, e o que a mensagem diz? Compare com a mensagem que o compilador daria se o <code>static_assert</code> não existisse.',
            'origem': 'unidade-3/aula19-templates-crtp',
        },
        {
            'n': '02',
            'html': 'Acrescente a <code>grade_de&lt;T&gt;</code> um template membro <code>convertida_para&lt;U&gt;()</code> que devolve uma <code>grade_de&lt;U&gt;</code> do mesmo tamanho, aplicando um callable a cada célula. Instancie-o com uma lambda que transforme <code>celula</code> em <code>int</code>.',
            'origem': 'unidade-3/aula19-templates-crtp',
        },
        {
            'n': '03',
            'html': 'Troque o contador manual de <code>item</code> por <code>contador_de_instancias&lt;item&gt;</code> e rode <code>make verifica</code>. A condição 4 do portão, <code>vivos=0</code>, continua fechando? Depois faça a troca errada de propósito, herdando de <code>contador_de_instancias&lt;entidade&gt;</code> em duas classes concretas, e explique o que o contador passa a contar.',
            'origem': 'unidade-3/aula19-templates-crtp',
        },
        {
            'n': '04',
            'html': 'Escreva, no despejo de <code>grade_de&lt;T&gt;</code>, um quarto ramo de <code>if constexpr</code> para <code>T</code> ponto flutuante. Em seguida troque os <code>if constexpr</code> por <code>if</code> comum e diga qual ramo impede a compilação, e para qual <code>T</code>.',
            'origem': 'unidade-3/aula19-templates-crtp',
        },
        {
            'n': '01',
            'html': 'Leia o <code>concept guardavel</code> em <code>c20/restricoes.hpp</code> e diga quais dos três <code>static_assert</code> de <code>grade_generica.hpp</code> ele substitui, e o que ele acrescenta. Compile o alvo <code>deriva_c20</code> e provoque o erro com <code>grade_restrita&lt;bool&gt;</code>.',
            'origem': 'unidade-3/aula20-concepts-ranges',
        },
        {
            'n': '02',
            'html': 'Reescreva <code>glifos_de_parede</code> em C++17, sem <code>std::views</code>: um <code>std::copy_if</code> para um vetor temporário e um laço depois. Quantas alocações a versão de C++17 faz que a de ranges não faz?',
            'origem': 'unidade-3/aula20-concepts-ranges',
        },
        {
            'n': '03',
            'html': 'Compile a mesma restrição de tipo duas vezes, com <code>-std=c++17</code> e <code>static_assert</code>, e com <code>-std=c++20</code> e <code>concept</code>, passando um tipo que não serve. Compare o que o compilador aponta em cada caso: a linha da restrição, ou a linha da chamada.',
            'origem': 'unidade-3/aula20-concepts-ranges',
        },
        {
            'n': '04',
            'html': 'Pesquise <code>std::expected</code> (C++23) e compare-o com o par <code>std::optional</code> e <code>std::variant</code> que a Aula 20 usa em <code>erro.hpp</code>. Reescreva a assinatura de <code>interpretar</code> com <code>std::expected</code> e diga o que a mudança tira do chamador.',
            'origem': 'unidade-3/aula20-concepts-ranges',
        },
    ],
    'pendencias': [],
}
