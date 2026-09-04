# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-3/aula22-stl
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Reescrito sobre o Deriva: o código desta aula é o que `build/extrair_codigo.py`
recorta de `src/inventario.cpp`.
"""

AULA = {
    'n': 21,
    'slug': 'a21',
    'titulo': 'STL panorâmica e lambdas',
    'curto': 'STL e lambdas',
    'unidade': 'III',
    'cap_v1': [
        22,
    ],
    'origem_v1': [
        'unidade-3/aula22-stl',
    ],
    'fatia': None,
    'deriva': 'v2.3',
    'lab': None,
    'interativos': [
        'expansor',
    ],
    'nota_migracao': 'Lambdas passam de UMA menção no livro inteiro a conteúdo de capítulo. Entra std::clamp.',
    'objetivos': [
        'Escolher o contêiner a partir do que a operação frequente exige',
        'Trocar laço manual por algoritmo, e dizer o que a troca ganha em intenção',
        'Escrever lambda com captura por valor e por referência, e saber quando cada uma pendura uma referência',
        'Usar <code>std::clamp</code> de C++17, com a armadilha do retorno por referência',
        'Compreender o modelo de iterador, e por que o de fim não é elemento',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'STL: contêineres, algoritmos e iteradores',
            'origem': 'unidade-3/aula22-stl',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v2.3 - o inventário da sonda',
                    'paragrafos': [
                        'A sonda passa a carregar peças, em <code>include/deriva/inventario.hpp</code> e <code>src/inventario.cpp</code>. O que faz os algoritmos valerem a pena ali é a <strong>capacidade</strong>: sem limite, guardar é <code>push_back</code> e pronto; com limite, aparecem as perguntas que a STL responde em uma linha - o que cabe, qual é a peça mais pesada, quantas satisfazem um critério, quanto de folga sobra.',
                        'Toda pergunta que o inventário responde sai de um algoritmo com lambda, e o único laço escrito à mão que sobra no arquivo é o do despejo, que percorre para formatar texto. É essa proporção que é o argumento da aula.',
                    ],
                },
            ],
        },
        {
            'id': 'conteineres',
            'titulo': 'Guia de escolha de contêiner',
            'origem': 'unidade-3/aula22-stl',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Contêiner',
                        'Acesso',
                        'Inserção',
                        'Onde está, ou por que não está, no Deriva',
                    ],
                    'linhas': [
                        [
                            '<code>vector&lt;T&gt;</code>',
                            'O(1)',
                            'O(1) no fim, O(n) no meio',
                            'As células de <code>grade_de&lt;T&gt;</code>, as entidades do <code>mundo</code>, as peças do inventário',
                        ],
                        [
                            '<code>deque&lt;T&gt;</code>',
                            'O(1)',
                            'O(1) nas duas pontas',
                            'A <code>fila_de_comandos</code> da v2.4, que entra por trás e sai pela frente',
                        ],
                        [
                            '<code>list&lt;T&gt;</code>',
                            'O(n)',
                            'O(1) em qualquer posição',
                            'Nenhum uso: sem iterador guardado, a inserção O(1) não se realiza',
                        ],
                        [
                            '<code>map&lt;K,V&gt;</code>',
                            'O(log n)',
                            'O(log n)',
                            'Nenhum uso ainda, e <code>vetor2</code> tem ordem total para poder ser chave',
                        ],
                        [
                            '<code>unordered_map&lt;K,V&gt;</code>',
                            'O(1) médio',
                            'O(1) médio',
                            'Nenhum uso: a ordem importa em quase tudo que o replay compara',
                        ],
                        [
                            '<code>set&lt;T&gt;</code>',
                            'O(log n)',
                            'O(log n)',
                            'As células visíveis em <code>fov.cpp</code>, e a ordem é o que torna o despejo comparável',
                        ],
                        [
                            '<code>array&lt;T,N&gt;</code>',
                            'O(1)',
                            'Impossível',
                            'Tamanho fixo em compilação, na pilha, sem alocação',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'O padrão é vector, e a exceção se justifica',
                    'paragrafos': [
                        'Na maioria dos casos <code>std::vector</code> é o contêiner certo, e a razão é a memória contígua: o processador lê a linha de cache inteira, de forma que percorrer é rápido mesmo quando a complexidade assintótica diz o contrário. Troque por outro quando tiver a operação frequente medida, e não pela tabela de O grande.',
                        'A coluna da direita é mais útil do que parece: metade das linhas diz <em>nenhum uso</em>, e isso é informação. Um sistema de vinte classes atravessa o semestre com <code>vector</code>, <code>deque</code>, <code>set</code> e <code>string</code>, e é bom saber disso antes de escolher a estrutura pelo nome mais interessante.',
                    ],
                },
            ],
        },
        {
            'id': 'algoritmos',
            'titulo': 'Algoritmos e lambdas no inventário',
            'origem': 'unidade-3/aula22-stl',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Uma lambda é um objeto com <code>operator()</code> que o compilador escreve para você, e a lista de captura é a lista de membros dele. Isso explica o comportamento inteiro: capturar por valor copia para dentro do objeto, capturar por referência guarda uma referência que vive tanto quanto o escopo de origem, e é por isso que lambda guardada fora do escopo tem de capturar por valor.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Em <code>inventario.cpp</code> as lambdas são todas locais, e as que capturam capturam por referência, porque morrem na mesma expressão em que nascem. Já em <code>estrategia_de_patrulha</code>, na Aula 25, a lambda é devolvida e sobrevive à chamada que a criou, de forma que a captura por valor deixa de ser preferência e passa a ser obrigação - é a armadilha de tempo de vida do <code>std::string_view</code> da Aula 3, noutra roupa.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Os algoritmos aparecem seis vezes no arquivo, e cada um carrega uma lição própria. Em <code>std::accumulate</code>, o zero inicial define o tipo da soma, e passar <code>0.0</code> daria soma em <code>double</code> sem ninguém pedir. Em <code>std::max_element</code>, a faixa vazia devolve <code>end()</code>, e desreferenciar o iterador de fim é comportamento indefinido, de forma que a comparação com <code>end()</code> não é cerimônia. Em <code>std::count_if</code>, o predicado vem de fora por <code>std::function</code>, e é isso que torna a função útil sem saber o que se vai perguntar.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'std::sort é instável, e o replay cobra',
                    'paragrafos': [
                        '<code>ordenar_por_massa</code> desempata pelo rótulo, e o desempate não é capricho: <code>std::sort</code> não promete preservar a ordem de entrada entre elementos equivalentes, de forma que sem o desempate a ordem entre massas iguais seria a que o algoritmo quisesse, e o despejo deixaria de ser byte a byte igual entre execuções. A condição 3 do portão falharia, e falharia de forma intermitente.',
                        'Quem quer estabilidade sem desempate usa <code>std::stable_sort</code>, e paga por ela em memória. O material escolheu o desempate explícito porque ele documenta o critério de ordem, que <code>stable_sort</code> deixa implícito na ordem de inserção.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'std::clamp, e o retorno por referência',
                    'paragrafos': [
                        'O construtor de <code>inventario</code> usa <code>std::clamp</code> de C++17 para prender a capacidade numa faixa, no lugar do par <code>std::min</code> e <code>std::max</code> aninhado, que obriga a ler duas chamadas encaixadas para descobrir a intenção.',
                        '<code>std::clamp</code> devolve <strong>referência const</strong> ao argumento escolhido, e aí está a armadilha: alimentá-lo com temporário e guardar o resultado por referência deixa uma referência pendurada. No Deriva o resultado é copiado para um <code>int</code>, e é isso que o torna seguro.',
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'O idioma <em>erase-remove</em> fecha a lista, e ele é o mais estranho da STL: <code>std::remove_if</code> não remove nada, apenas empurra o que sobrevive para a frente e devolve o novo fim, e é o <code>erase</code> do contêiner que corta. Em C++20 a mesma coisa é <code>std::erase_if</code>, uma chamada só - e o material nomeia o idioma antigo em vez de fingir que ele é natural, porque quem lê código de C++17 vai encontrá-lo.',
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-3/aula22-stl',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Dado <code>std::vector&lt;std::unique_ptr&lt;componente&gt;&gt;</code>, escreva uma função que devolva as <code>n</code> peças mais pesadas em ordem determinística, usando apenas algoritmos da STL, sem laço <code>for</code> nem <code>while</code> escrito à mão. C++17. Explique por que escolheu <code>std::partial_sort</code> ou <code>std::nth_element</code>."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o modelo costuma errar',
                    'paragrafos': [
                        'Modelos tendem ao laço manual quando a versão com algoritmo seria mais clara, e é preciso pedir explicitamente que não haja laço para ver se conseguem. O segundo erro é mais caro: sobre contêiner de <code>std::unique_ptr</code>, eles produzem cópia onde só pode haver movimento, e o código não compila; o terceiro é esquecer o desempate, e devolver ordem que muda entre execuções.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Reescreva <code>inventario::massa_total</code> com laço <code>for</code> à mão e compare as duas versões: o que a versão com <code>std::accumulate</code> diz que a outra não diz? Em seguida troque o zero inicial por <code>0.0</code> e explique o que muda no tipo do resultado.',
            'origem': 'unidade-3/aula22-stl',
        },
        {
            'n': '02',
            'html': 'Remova o desempate pelo rótulo de <code>ordenar_por_massa</code>, guarde duas peças de massa igual e rode <code>make verifica</code> algumas vezes. A condição 3 do portão falha sempre, às vezes, ou nunca? Relacione a resposta com o que a Aula 22 diz sobre defeito intermitente.',
            'origem': 'unidade-3/aula22-stl',
        },
        {
            'n': '03',
            'html': 'Escreva a versão errada de <code>std::clamp</code>: passe um temporário e guarde o resultado em <code>const int&amp;</code>. Compile com <code>-Wall -Wextra -Wpedantic</code> e diga se algum aviso aparece. Depois observe o valor no <code>gdb</code>.',
            'origem': 'unidade-3/aula22-stl',
        },
        {
            'n': '04',
            'html': 'Acrescente a <code>inventario</code> um método <code>mais_leve</code> por <code>std::min_element</code> e escreva o caso de teste para o inventário vazio antes de escrever o método. Por que o teste do vazio é o primeiro que se escreve aqui?',
            'origem': 'unidade-3/aula22-stl',
        },
    ],
    'pendencias': [],
}
