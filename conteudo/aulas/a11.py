# -*- coding: utf-8 -*-
"""Reescrito à mão sobre o Deriva - não rode build/extrair_v1.py aqui.

Origem no site v1: unidade-2/aula17-funcoes-virtuais
Página inteira.
Este arquivo é a fonte de verdade do site v2 e do livro v2. O extrator do v1
sobrescreve o que está aqui; se precisar reextrair, faça em branch.
"""

AULA = {
    'n': 11,
    'slug': 'a11',
    'titulo': 'Funções virtuais e classes abstratas',
    'curto': 'Funções virtuais e vtable',
    'unidade': 'II',
    'cap_v1': [
        17,
    ],
    'origem_v1': [
        'unidade-2/aula17-funcoes-virtuais',
    ],
    'fatia': None,
    'deriva': 'v1.1',
    'lab': 'LAB-06',
    'interativos': [
        'virtual',
    ],
    'nota_migracao': 'O destrutor virtual ganha tratamento próprio: o vazamento que sua ausência produz, acusado pelo contador `vivos` da Aula 7 e lido no gdb. Os trechos saem de `include/deriva/entidade.hpp`, de `testes/test_entidade.cpp` e da variante `v1.1-quebrada`.',
    'objetivos': [
        'Usar <code>virtual</code>, <code>override</code> e <code>final</code> onde cada um cabe',
        'Declarar classes abstratas com funções puramente virtuais',
        'Descrever o mecanismo de <code>vptr</code> e vtable e dizer quanto ele custa em bytes',
        'Provar que o destrutor virtual rodou sem sanitizer nem Valgrind',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Funções virtuais, override, final e abstração',
            'origem': 'unidade-2/aula17-funcoes-virtuais',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v1.1 · o despacho, e o destrutor que o acompanha',
                    'paragrafos': [
                        '<code>glifo()</code> e <code>nome()</code> passam a puramente virtuais, o que torna <code>entidade</code> abstrata, e <code>agir(mundo&amp;)</code> passa a virtual com corpo vazio. A base ganha <code>virtual ~entidade() = default</code>, e é essa palavra que a caça ao bug 2 retira para ver o que acontece.',
                        'A variante <code>variantes/v1.1-quebrada/</code> traz a base com função virtual e destrutor não virtual. O que ela mede não é o vazamento, que é conhecido: é <strong>quando o compilador avisa</strong>.',
                    ],
                },
            ],
        },
        {
            'id': 'override-final',
            'titulo': 'virtual, override e final',
            'origem': 'unidade-2/aula17-funcoes-virtuais',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'As três palavras respondem a perguntas diferentes. <code>virtual</code>, na base, diz que a chamada se resolve pelo objeto e não pelo ponteiro. <code>override</code>, na derivada, pede ao compilador que confira: se a assinatura não casar com nenhuma função virtual da base, o programa não compila, e é assim que um erro de digitação deixa de criar uma função nova em silêncio. <code>final</code> proíbe continuar sobrescrevendo, ou continuar derivando.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Na derivada, <code>virtual</code> não se repete: <code>override</code> já diz que a função sobrescreve, e diz melhor, porque o compilador o verifica. No Deriva, <code>drone</code> e <code>item</code> são <code>final</code> e <code>sonda</code> não é, e a razão dessa assimetria está na Aula 17.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Escreva sempre override',
                    'paragrafos': [
                        'Sem <code>override</code>, trocar <code>glifo</code> por <code>Glifo</code> ou esquecer o <code>const</code> na assinatura produz uma função nova que ninguém chama, e o objeto passa a desenhar o glifo da base. O compilador não tem como saber que você queria sobrescrever, salvo se você disser. O item R5 da rubrica é a pergunta que pega isso na revisão.',
                    ],
                },
            ],
        },
        {
            'id': 'abstrata',
            'titulo': 'Classes abstratas e interfaces puras',
            'origem': 'unidade-2/aula17-funcoes-virtuais',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Uma função puramente virtual, escrita com <code>= 0</code>, declara a operação e recusa fornecer o corpo. Basta uma para que a classe se torne abstrata e deixe de ser instanciável. Em <code>entidade</code> isso não é cerimônia: uma entidade sem glifo não significa nada no domínio, e a partir da v1.1 é o compilador que passa a dizer isso, em vez de a documentação.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Interface pura é o caso extremo: só funções puramente virtuais, nenhum dado, e destrutor virtual. É a forma que <code>i_reparavel</code> tem na v1.7, e a Aula 17 mostra por que ela é o único uso de herança múltipla que este material recomenda sem ressalva. A diferença entre "classe abstrata" e "interface pura" é a presença de estado, e é ela que decide se a herança múltipla vai duplicar alguma coisa.',
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'A abstração é afirmada, não descrita',
                    'paragrafos': [
                        'O trecho extraído de <code>testes/test_entidade.cpp</code> afirma quatro decisões de projeto com <code>std::is_abstract_v</code>, <code>std::is_constructible_v</code>, <code>std::has_virtual_destructor_v</code> e <code>std::is_copy_constructible_v</code>. São perguntas respondidas em tempo de compilação: se alguém tornar a base instanciável ou copiável por acidente, o teste falha antes de o programa rodar.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-2/aula17-funcoes-virtuais',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Em C++17, snake_case: dada a base abstrata <code>entidade</code>, com <code>glifo()</code> e <code>nome()</code> puramente virtuais e <code>agir(mundo&amp;)</code> virtual, escreva uma derivada concreta e um teste que afirme, sem executar nada, que a base é abstrata, tem destrutor virtual e não é copiável."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'Erros recorrentes: <code>override</code> escrito numa função que a base não declarou virtual, o que ao menos falha na compilação; <code>final</code> posto na classe quando a intenção era pôr no método; e o destrutor da base declarado virtual sem corpo nem <code>= default</code>, o que passa da compilação e falha na ligação. Nenhum dos três aparece se você pedir o teste junto com o código.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Retire <code>override</code> de <code>drone::glifo</code> e troque o nome do método por <code>Glifo</code>. Compile: o portão do Deriva emite algum aviso? Rode o teste do despacho e diga qual glifo o drone passa a desenhar, e por quê.',
            'origem': 'unidade-2/aula17-funcoes-virtuais',
        },
        {
            'n': '02',
            'html': 'Rode a variante <code>variantes/v1.1-quebrada/</code> nos três casos que o <code>LEIA-ME.md</code> dela descreve: <code>delete</code> textual, o mesmo <code>delete</code> dentro de <code>unique_ptr</code>, e os dois com <code>-Wnon-virtual-dtor</code>. Anote quantos avisos aparecem em cada caso e explique por que o caso do <code>unique_ptr</code> é o mais perigoso dos três.',
            'origem': 'unidade-2/aula17-funcoes-virtuais',
        },
        {
            'n': '03',
            'html': 'Naquela variante, o contador <code>vivos</code> fecha em zero e mente. Diga por que, e escreva a correção: onde o contador tem de morar para acusar o defeito. Confira sua resposta contra o Deriva bom, onde o contador está em cada classe concreta.',
            'origem': 'unidade-2/aula17-funcoes-virtuais',
        },
        {
            'n': '04',
            'html': 'Use <code>make gdb-dtor</code> como modelo e ponha um ponto de parada no destrutor de <code>deriva::sonda</code>. Delete uma sonda por <code>entidade*</code> com o destrutor virtual e sem ele, e mostre, pela pilha de chamadas, de onde o destrutor é chamado em cada caso.',
            'origem': 'unidade-2/aula17-funcoes-virtuais',
        },
    ],
    'pendencias': [
        {
            'tipo': 'caca-bug',
            'onde': 'aula 11',
            'o_que': 'CAÇA AO BUG 2: destrutor não virtual - semana 9. A variante e o roteiro existem em `variantes/v1.1-quebrada/`; falta o roteiro de condução em sala.',
        },
    ],
}
