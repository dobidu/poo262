# -*- coding: utf-8 -*-
"""Reescrito à mão sobre o Deriva - não rode build/extrair_v1.py aqui.

Origem no site v1: unidade-2/aula13-sobrecarga-operadores
Página inteira.
Este arquivo é a fonte de verdade do site v2 e do livro v2. O extrator do v1
sobrescreve o que está aqui; se precisar reextrair, faça em branch.
"""

AULA = {
    'n': 15,
    'slug': 'a15',
    'titulo': 'Sobrecarga de operadores',
    'curto': 'Sobrecarga de operadores',
    'unidade': 'II',
    'cap_v1': [
        13,
    ],
    'origem_v1': [
        'unidade-2/aula13-sobrecarga-operadores',
    ],
    'fatia': None,
    'deriva': 'v1.5',
    'lab': None,
    'interativos': [
        'virtual',
    ],
    'nota_migracao': 'Operadores do Deriva: vetor2, operator[] de mapa, operator<<. Os trechos saem de `include/deriva/vetor2.hpp`, de `include/deriva/mapa.hpp` e de `testes/test_operadores.cpp`, e os operadores de `vetor2` são `constexpr`, de forma que o compilador afirma o comportamento em vez de o teste observá-lo.',
    'objetivos': [
        'Decidir quando sobrecarregar um operador, e quando a função nomeada é melhor',
        'Escolher entre membro e função livre pela pergunta que a operação faz',
        'Escrever o par <code>const</code> e não-<code>const</code> de <code>operator[]</code> e dizer por que ele existe',
        'Implementar <code>operator&lt;&lt;</code> como função livre',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Sobrecarga de operadores idiomática',
            'origem': 'unidade-2/aula13-sobrecarga-operadores',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v1.5 · operadores de vetor2 e mapa[pos]',
                    'paragrafos': [
                        '<code>vetor2</code> ganha <code>+=</code>, <code>-=</code> e <code>*=</code> como membros, e <code>+</code>, <code>-</code>, <code>*</code> e <code>&lt;</code> como funções livres. <code>mapa</code> ganha o par <code>operator[]</code> em versão <code>const</code> e não-<code>const</code>, e o despejo passa a poder ir para um fluxo por <code>operator&lt;&lt;</code>.',
                        'Os operadores de <code>vetor2</code> são <code>constexpr</code>, e por isso o comportamento deles está afirmado em <code>static_assert</code> no próprio cabeçalho: se um deles quebrar, o Deriva não compila.',
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'Sobrecarregar um operador só se justifica quando a notação já existe no domínio e o leitor a lê sem aprender nada novo. Somar dois deslocamentos na grade é soma, e <code>a + b</code> diz isso melhor que <code>somar(a, b)</code>. Já "aplicar o campo de visão ao mapa" não é operação com símbolo consagrado, e ali a função nomeada ganha: operador inventado obriga o leitor a decorar a sua convenção.',
                },
            ],
        },
        {
            'id': 'membro-livre',
            'titulo': 'Membro ou função livre: a pergunta que decide',
            'origem': 'unidade-2/aula13-sobrecarga-operadores',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A pergunta é se a operação trata os dois lados igual. O composto <code>+=</code> não trata: ele modifica o objeto da esquerda e devolve referência a ele, então é membro. O binário <code>+</code> trata: ele produz um terceiro valor a partir de dois, sem privilegiar nenhum, então é função livre. Escrever <code>+</code> em termos de <code>+=</code> é a forma que não duplica a regra, e no <code>vetor2</code> é literalmente o que está escrito.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A consequência da escolha é a simetria. Como <code>operator*</code> é função livre e existe nas duas ordens, <code>3 * v</code> e <code>v * 3</code> compilam os dois, e o teste de operadores afirma isso. Um <code>operator*</code> membro aceitaria só <code>v * 3</code>, porque o lado esquerdo de um operador membro tem de ser o objeto, e nenhuma conversão o alcança.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Operador',
                        'Membro ou livre',
                        'Por quê',
                    ],
                    'linhas': [
                        [
                            '<code>+=</code>, <code>-=</code>, <code>*=</code>',
                            'membro',
                            'modifica o objeto da esquerda e devolve referência a ele',
                        ],
                        [
                            '<code>+</code>, <code>-</code>, <code>*</code>',
                            'livre',
                            'trata os dois lados igual; simétrico por construção',
                        ],
                        [
                            '<code>[]</code>',
                            'membro, em par',
                            'acesso ao próprio objeto, e a constância tem de propagar',
                        ],
                        [
                            '<code>&lt;&lt;</code>',
                            'livre',
                            'o lado esquerdo é o fluxo, e o fluxo não é nosso',
                        ],
                        [
                            '<code>&lt;</code>',
                            'livre',
                            'ordem total, para servir de chave de <code>std::map</code>',
                        ],
                    ],
                },
            ],
        },
        {
            'id': 'operadores-do-mapa',
            'titulo': 'Os operadores do mapa: o par const e o operator<<',
            'origem': 'unidade-2/aula13-sobrecarga-operadores',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': '<code>mapa</code> declara <code>operator[]</code> duas vezes, uma <code>const</code> devolvendo <code>const celula&amp;</code> e uma não-<code>const</code> devolvendo <code>celula&amp;</code>, e o par existe por uma razão que se enuncia pelos dois erros que ele evita. Com uma sobrecarga só, devolvendo referência não-<code>const</code>, seria possível escrever numa célula através de um mapa constante; devolvendo referência <code>const</code>, seria impossível escrever em qualquer mapa. A constância do objeto tem de propagar para o que o acesso devolve, e é isso que as duas assinaturas dizem.',
                },
                {
                    'tipo': 'prosa',
                    'html': '<code>operator&lt;&lt;</code> não pode ser membro de <code>mapa</code>, porque o operando da esquerda é o fluxo, e <code>std::ostream</code> não é uma classe nossa para modificar. Ele é função livre, tem duas linhas sobre <code>despejar()</code>, e devolve a referência ao fluxo para que a chamada se encadeie. O despejo continua determinístico, e é dessa propriedade que o replay da Aula 16 depende.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Três operadores que não se sobrecarregam',
                    'paragrafos': [
                        '<code>&amp;&amp;</code>, <code>||</code> e <code>,</code> têm, nas versões embutidas, avaliação em curto-circuito e ordem garantida. A versão sobrecarregada é uma chamada de função, e chamada de função avalia todos os argumentos: o curto-circuito desaparece em silêncio, e o código que dependia dele passa a executar o lado direito sempre. A sintaxe continua igual, e é isso que torna o defeito difícil de ver.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-2/aula13-sobrecarga-operadores',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Em C++17, snake_case: para um tipo <code>vetor2</code> de dois inteiros, escreva <code>+=</code>, <code>-=</code>, <code>*=</code>, <code>+</code>, <code>-</code>, <code>*</code>, <code>==</code>, <code>!=</code> e <code>&lt;</code>. Diga, para cada um, se é membro ou função livre e por quê, marque como <code>constexpr</code> o que puder ser, e afirme o comportamento em <code>static_assert</code> em vez de em teste de execução."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'Erros recorrentes: escrever todos os operadores como membros, o que quebra a simetria e faz <code>3 * v</code> deixar de compilar; entregar só a sobrecarga não-<code>const</code> de <code>operator[]</code>, o que impede ler de um objeto constante; e escrever <code>+</code> duplicando a regra em vez de o delegar a <code>+=</code>. Nenhum dos três falha na compilação do código gerado, e é por isso que a revisão é a única defesa.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Transforme <code>operator*</code> de <code>vetor2</code> em membro e tente compilar <code>3 * v</code>. Leia a mensagem do compilador e explique, na linguagem de resolução de sobrecarga, por que o lado esquerdo não é convertido.',
            'origem': 'unidade-2/aula13-sobrecarga-operadores',
        },
        {
            'n': '02',
            'html': 'Apague a sobrecarga <code>const</code> de <code>mapa::operator[]</code>. Que chamadas param de compilar, e em quais testes? Depois apague a não-<code>const</code> em vez dela, e compare os dois estragos.',
            'origem': 'unidade-2/aula13-sobrecarga-operadores',
        },
        {
            'n': '03',
            'html': 'Os operadores de <code>vetor2</code> são <code>constexpr</code> e o cabeçalho os afirma em <code>static_assert</code>. Escreva uma afirmação nova, sobre <code>manhattan</code>, que passe, e uma que falhe, e diga em que momento da compilação cada uma é decidida.',
            'origem': 'unidade-2/aula13-sobrecarga-operadores',
        },
        {
            'n': '04',
            'html': 'Escreva <code>operator&lt;&lt;</code> para <code>celula</code>, como função livre, e mostre que a chamada se encadeia. Depois explique por que ela não pode ser membro, e por que <code>operator&gt;&gt;</code> teria o mesmo impedimento.',
            'origem': 'unidade-2/aula13-sobrecarga-operadores',
        },
    ],
    'pendencias': [],
}
