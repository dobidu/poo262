# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-1/aula02-conceitos-fundamentais
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Pendências desta aula: 0 (ver conteudo/PENDENCIAS.md)
"""

AULA = {
    'n': 3,
    'slug': 'a03',
    'titulo': 'Fundamentos de C++17 para POO',
    'curto': 'Fundamentos de C++17',
    'unidade': 'I',
    'cap_v1': [
        2,
    ],
    'origem_v1': [
        'unidade-1/aula02-conceitos-fundamentais',
    ],
    'fatia': None,
    'deriva': None,
    'lab': 'LAB-02',
    'interativos': [
        'ciclo',
    ],
    'nota_migracao': 'O capítulo com maior déficit do livro. Entram std::string_view com a armadilha de tempo de vida, ligações estruturadas, [[nodiscard]] e [[maybe_unused]] - hoje com zero ocorrências no livro inteiro.',
    'objetivos': [
        'Distinguir classe (molde) de objeto (instância)',
        'Compreender mensagens e o mecanismo de despacho',
        'Identificar atributos de instância e atributos de classe',
        'Usar a terminologia OO corretamente em português e inglês',
        'Usar <code>std::string_view</code> sabendo que ela não possui os bytes que enxerga, e reconhecer a armadilha de tempo de vida que isso cria',
        'Ler e escrever ligação estruturada, <code>[[nodiscard]]</code> e <code>[[maybe_unused]]</code>',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Conceitos Fundamentais: Objetos, Classes e Mensagens',
            'origem': 'unidade-1/aula02-conceitos-fundamentais',
            'compartilhado': False,
            'blocos': [],
        },
        {
            'id': 'classe-objeto',
            'titulo': 'Classe vs. Objeto',
            'origem': 'unidade-1/aula02-conceitos-fundamentais',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Uma <strong>classe</strong> é um molde: define quais campos existem, em que ordem, e quais operações são legítimas sobre eles. Um <strong>objeto</strong> é uma instância concreta em memória, com os seus próprios valores. A classe existe em tempo de compilação e não ocupa byte nenhum de execução; o objeto existe em tempo de execução e ocupa exatamente o que a ordem de declaração dos membros mandar, que é o assunto da Aula 07.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'No Deriva o par mínimo é <code>grade</code> e as grades. A classe está declarada uma vez, em <code>include/deriva/grade.hpp</code>, com <code>largura_</code>, <code>altura_</code> e o vetor de <code>celula</code>. Duas grades construídas a partir dela - <code>grade a(4, 3)</code> e <code>grade b(80, 24)</code> - compartilham o <strong>código</strong> de <code>em()</code>, de <code>dentro()</code> e do construtor, e não compartilham <strong>dado</strong> nenhum: escrever numa célula de <code>a</code> não alcança <code>b</code>, e <code>a.largura()</code> devolve 4 enquanto <code>b.largura()</code> devolve 80. É a mesma função, chamada sobre objetos diferentes, e o que muda de uma chamada para a outra é só qual objeto está do lado esquerdo do ponto.',
                },
            ],
        },
        {
            'id': 'mensagens',
            'titulo': 'Mensagens e Despacho',
            'origem': 'unidade-1/aula02-conceitos-fundamentais',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Em OO, objetos se comunicam por <strong>mensagens</strong>. Em C++, uma mensagem é implementada como chamada de função membro, e a forma é sempre a mesma: <code>receptor.mensagem(argumentos)</code>. Quem manda a mensagem não escolhe o que acontece; quem decide é o receptor, e é nisso que o encapsulamento se apoia.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O caso do Deriva que mostra a diferença é <code>mapa::carregar(caminho)</code>. Quem chama manda um caminho e recebe um <code>std::optional&lt;mapa&gt;</code>. O que acontece entre as duas coisas - conferir se o arquivo existe, ler o conteúdo, partir em fileiras, recusar a fileira de largura divergente, achar a entrada da sonda - é decisão do receptor, e nada disso aparece na chamada. Trocar o algoritmo de leitura por outro não muda uma linha de quem chama, e é essa a liberdade que a mensagem compra. Compare com a versão em C da Aula 01: lá, <code>em(&amp;g, x, y)</code> é função livre, quem chama passa o endereço da struct, e nada na assinatura prende a função à grade a que ela pertence.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Mensagem ≠ Chamada de função',
                    'paragrafos': [
                        'Uma chamada de função em C é estática - o compilador sabe qual função chamar. Uma mensagem OO pode ser resolvida em tempo de execução (polimorfismo dinâmico), dependendo do tipo real do receptor.',
                    ],
                },
            ],
        },
        {
            'id': 'terminologia',
            'titulo': 'Terminologia: OO vs. C++',
            'origem': 'unidade-1/aula02-conceitos-fundamentais',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Conceito OO',
                        'Termo em C++',
                        'Exemplo',
                    ],
                    'linhas': [
                        [
                            'Classe',
                            'class / struct',
                            '<code>class grade { ... };</code>',
                        ],
                        [
                            'Objeto / Instância',
                            'variável do tipo classe',
                            '<code>grade g(80, 24);</code>',
                        ],
                        [
                            'Atributo',
                            'membro dado (<em>data member</em>)',
                            '<code>int largura_;</code>',
                        ],
                        [
                            'Método',
                            'função membro (<em>member function</em>)',
                            '<code>int largura() const;</code>',
                        ],
                        [
                            'Mensagem',
                            'chamada de função membro',
                            '<code>g.largura();</code>',
                        ],
                        [
                            'Construtor',
                            '<em>constructor</em>',
                            '<code>grade(int largura, int altura);</code>',
                        ],
                        [
                            'Destrutor',
                            '<em>destructor</em>',
                            '<code>~mapa();</code>',
                        ],
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-1/aula02-conceitos-fundamentais',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Explique em português a diferença entre classe e objeto em C++17, usando como exemplo uma grade de células de um jogo de terminal. A classe deve ter ao menos três atributos privados, um construtor que estabeleça a invariante, e um método <code>const</code>. Convenções: snake_case, identificadores e comentários em português."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'LLMs confundem atributos de instância com atributos de classe (static). Peça explicitamente que demonstre os dois e mostre que objetos independentes têm dados independentes.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Leia <code>exemplos/deriva/include/deriva/grade.hpp</code> e classifique cada membro como atributo ou método. Quantos atributos de instância há, quantos métodos, e quantos construtores? Depois faça o mesmo com <code>vetor2.hpp</code> e explique por que ele não tem atributo privado nenhum.',
            'origem': 'unidade-1/aula02-conceitos-fundamentais',
        },
        {
            'n': '02',
            'html': 'Construa duas grades de dimensões diferentes num <code>main()</code>, escreva um glifo numa célula de cada uma, e imprima as duas. Quais mensagens foram enviadas, e quem é o receptor de cada uma? Por que a escrita numa não alcança a outra, se as duas executam o mesmo código de <code>em()</code>?',
            'origem': 'unidade-1/aula02-conceitos-fundamentais',
        },
        {
            'n': '03',
            'html': 'Explique com um exemplo concreto por que dois objetos da mesma classe compartilham código mas não compartilham dados.',
            'origem': 'unidade-1/aula02-conceitos-fundamentais',
        },
        {
            'n': '04',
            'html': 'Pesquise a diferença entre <em>early binding</em> (ligação estática) e <em>late binding</em> (ligação dinâmica). Qual delas implementa o conceito de mensagem OO de forma mais fiel? Por quê?',
            'origem': 'unidade-1/aula02-conceitos-fundamentais',
        },
    ],
    'pendencias': [],
}
