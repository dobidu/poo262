# -*- coding: utf-8 -*-
"""Reescrito à mão sobre o Deriva - não rode build/extrair_v1.py aqui.

Origem no site v1: unidade-2/aula18-polimorfismo-dinamico
Página inteira.
Este arquivo é a fonte de verdade do site v2 e do livro v2. O extrator do v1
sobrescreve o que está aqui; se precisar reextrair, faça em branch.
"""

AULA = {
    'n': 18,
    'slug': 'a18',
    'titulo': 'Polimorfismo dinâmico e RTTI',
    'curto': 'Polimorfismo dinâmico e RTTI',
    'unidade': 'II',
    'cap_v1': [
        18,
    ],
    'origem_v1': [
        'unidade-2/aula18-polimorfismo-dinamico',
    ],
    'fatia': None,
    'deriva': 'v1.8',
    'lab': None,
    'interativos': [
        'virtual',
    ],
    'nota_migracao': 'Renumeração. Os trechos passam a sair de `src/inspetor.cpp` e de `src/mundo.cpp`, que existem em par de propósito: o inspetor é o único lugar do Deriva onde `dynamic_cast` é a resposta, e o `mundo` é o contraste, onde nenhuma linha nomeia tipo concreto. O custo do `vptr` é o medido em `include/deriva/leiaute.hpp`.',
    'objetivos': [
        'Descrever o mecanismo de <code>vptr</code> e vtable, e dizer quanto ele custa por objeto',
        'Usar <code>dynamic_cast</code> e <code>typeid</code> com segurança, e na ordem certa',
        'Contrastar polimorfismo dinâmico com o estático da Aula 19',
        'Reconhecer quando <code>dynamic_cast</code> é sintoma de função virtual faltando',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Polimorfismo dinâmico: vtable, RTTI e dynamic_cast',
            'origem': 'unidade-2/aula18-polimorfismo-dinamico',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v1.8 · o inspetor de entidade no console',
                    'paragrafos': [
                        'A v1.8 entrega o inspetor: aponta-se para uma entidade e ele diz o que ela é. É a única ferramenta do Deriva que precisa perguntar o tipo, e por isso é o único lugar do projeto onde <code>dynamic_cast</code> é a resposta e não o sintoma.',
                        'A aula tem dois trechos em par, e a comparação entre eles é o conteúdo: o inspetor, que pergunta o tipo porque diagnosticar é a tarefa, e o turno do <code>mundo</code>, que não nomeia um único tipo concreto.',
                    ],
                },
            ],
        },
        {
            'id': 'vtable',
            'titulo': 'O mecanismo: vptr, vtable e o que a chamada virtual custa',
            'origem': 'unidade-2/aula18-polimorfismo-dinamico',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Quando uma classe declara função virtual, o compilador monta para ela uma tabela de ponteiros de função, uma entrada por virtual, e põe no objeto um ponteiro para essa tabela. A tabela é por <strong>classe</strong>, e existe uma vez no programa; o ponteiro é por <strong>objeto</strong>, e é ele que o objeto carrega. Chamar uma virtual através de um ponteiro para a base é, então, carregar o ponteiro do objeto, buscar a entrada na tabela e chamar o que está lá.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'É por isso que o despacho responde ao <strong>objeto</strong>, e não ao tipo do ponteiro: o ponteiro pode ser <code>entidade*</code> nos três casos, e a tabela alcançada é a da classe real. O teste extraído da Aula 11 mostra isso da forma mais curta possível: três objetos, um só tipo de ponteiro, e a saída é <code>@d!</code>, e não <code>eee</code>.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Estrutura',
                        'Tamanho medido',
                        'Por quê',
                    ],
                    'linhas': [
                        [
                            'sem nenhuma virtual',
                            '8 bytes',
                            'só a posição: não há tabela, então não há ponteiro',
                        ],
                        [
                            'com uma virtual',
                            '16 bytes',
                            '8 do ponteiro de tabela, 8 da posição',
                        ],
                        [
                            'derivada com um campo próprio',
                            '24 bytes',
                            'o custo do ponteiro não desaparece: ele se soma',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'São 8 bytes por objeto, não por classe',
                    'paragrafos': [
                        'O número está afirmado em <code>static_assert</code> em <code>include/deriva/leiaute.hpp</code>, e a distinção importa quando se multiplica. Uma célula não é polimórfica e não paga nada; uma entidade paga 8 bytes, e a estação tem poucas dezenas delas. Se a <code>celula</code> fosse polimórfica, os mesmos 8 bytes se multiplicariam pelas células do setor, e é essa conta, e não a indireção da chamada, que decide o projeto.',
                        'A alternativa sem tabela é o polimorfismo estático da Aula 19, com <code>template</code> e CRTP: o despacho se resolve na compilação, o objeto não carrega ponteiro, e o preço passa a ser código gerado por tipo em vez de indireção em tempo de execução.',
                    ],
                },
            ],
        },
        {
            'id': 'dynamic-cast',
            'titulo': 'dynamic_cast, typeid, e a ordem que não é opcional',
            'origem': 'unidade-2/aula18-polimorfismo-dinamico',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': '<code>dynamic_cast</code> pergunta, em tempo de execução, se o objeto apontado é daquele tipo. Para ponteiro, devolve <code>nullptr</code> quando não é, e a resposta se testa num <code>if</code>; para referência, lança <code>std::bad_cast</code>, porque não há valor que signifique "não é". <code>typeid</code> devolve o tipo real, e o nome que ele traz é definido pela implementação: serve para diagnóstico, e não para ser exibido a quem usa o programa.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A armadilha número um é a ordem da cadeia. Uma <code>sonda_reparadora</code> também <em>é</em> uma <code>sonda</code>, então uma cadeia que pergunte por <code>sonda</code> antes nunca alcança o ramo da reparadora, e o programa passa a descrever a entidade de forma incompleta sem errar em nada que o compilador veja. Perguntar pelo tipo mais derivado primeiro é obrigatório, e a necessidade dessa regra é, ela mesma, o argumento de que a cadeia deveria ser uma função virtual.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Pergunte por capacidade, não por tipo concreto',
                    'paragrafos': [
                        'Quando o <code>dynamic_cast</code> tem como alvo uma <strong>interface</strong>, e não uma classe concreta, a pergunta muda de natureza: em vez de "que classe é esta?", ela passa a ser "esta entidade sabe reparar?". É a consulta que herança pública não expressa, e é a forma em que <code>dynamic_cast</code> continua defensável, porque a resposta não depende de você ter enumerado as classes certas.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'dynamic_cast frequente é função virtual faltando',
                    'paragrafos': [
                        'No código de domínio, uma cadeia de <code>dynamic_cast</code> quase sempre significa que a operação deveria ser uma função virtual da base. O contraste está na mesma página: <code>entidade::descrever</code> resolve o mesmo problema por despacho, sem perguntar tipo nenhum, e acrescentar uma entidade nova não toca em uma linha dela. Quando a operação não cabe na interface base, o caminho é o Visitor, que a Aula 25 apresenta.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-2/aula18-polimorfismo-dinamico',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Em C++17, snake_case: tenho um <code>vector&lt;unique_ptr&lt;entidade&gt;&gt;</code> e preciso descrever cada entidade em texto, incluindo os campos que só algumas têm. Proponha duas soluções, uma por função virtual na base e uma por Visitor, e diga o que cada uma custa quando eu acrescentar uma entidade nova. Não use <code>dynamic_cast</code> em nenhuma das duas."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'A primeira proposta é quase sempre uma cadeia de <code>dynamic_cast</code>, porque é a que se escreve sem mudar a hierarquia, e ela costuma vir na ordem errada, do tipo mais geral para o mais derivado. Peça explicitamente as alternativas sem RTTI, e depois pergunte quantos arquivos cada uma obriga a abrir quando um tipo novo entra.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Em <code>include/deriva/leiaute.hpp</code>, acrescente um par de estruturas: uma sem função virtual e outra igual com uma virtual. Preveja os dois <code>sizeof</code> antes de compilar, e afirme-os em <code>static_assert</code>. Se o compilador recusar, é a sua previsão que está errada, e é essa a lição.',
            'origem': 'unidade-2/aula18-polimorfismo-dinamico',
        },
        {
            'n': '02',
            'html': 'Inverta a ordem da cadeia de <code>dynamic_cast</code> do inspetor, pondo <code>sonda</code> antes de <code>sonda_reparadora</code>. A suíte acusa? Diga qual teste cai, e o que o programa passaria a imprimir se aquele teste não existisse.',
            'origem': 'unidade-2/aula18-polimorfismo-dinamico',
        },
        {
            'n': '03',
            'html': 'Reescreva a descrição da entidade sem um único <code>dynamic_cast</code>, movendo para a base a função virtual que falta. Compare os dois desenhos por uma pergunta só: quantos arquivos você abre para acrescentar uma entidade nova em cada um?',
            'origem': 'unidade-2/aula18-polimorfismo-dinamico',
        },
        {
            'n': '04',
            'html': 'Compile o Deriva com <code>-fno-rtti</code>. Quais erros aparecem, e em que arquivos? O que o conjunto desses arquivos diz sobre onde a informação de tipo em tempo de execução é de fato usada no projeto?',
            'origem': 'unidade-2/aula18-polimorfismo-dinamico',
        },
    ],
    'pendencias': [],
}
