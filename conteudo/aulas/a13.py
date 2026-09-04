# -*- coding: utf-8 -*-
"""Reescrito à mão sobre o Deriva - não rode build/extrair_v1.py aqui.

Origem no site v1: unidade-2/aula11-smart-pointers
Fatia: shared - fatia 2/2 do Cap. 11 - shared_ptr, weak_ptr, contagem de
referências, o ciclo que o contador acusa.
Este arquivo é a fonte de verdade do site v2 e do livro v2. O extrator do v1
sobrescreve o que está aqui; se precisar reextrair, faça em branch.
"""

AULA = {
    'n': 13,
    'slug': 'a13',
    'titulo': 'Ponteiros inteligentes II - posse compartilhada',
    'curto': 'Posse compartilhada: shared_ptr e weak_ptr',
    'unidade': 'II',
    'cap_v1': [
        11,
    ],
    'origem_v1': [
        'unidade-2/aula11-smart-pointers',
    ],
    'fatia': [
        'shared',
        'fatia 2/2 do Cap. 11 - shared_ptr, weak_ptr, contagem de referências, o ciclo que o contador acusa',
    ],
    'deriva': 'v1.3',
    'lab': 'LAB-07',
    'interativos': [
        'posse',
    ],
    'nota_migracao': 'MIGRAÇÃO DE RISCO 3/3 (continuação). A introdução comum sobre por que ponteiro inteligente existe vive na Aula 12 e é referenciada, não repetida. Os objetivos, o slide de LLM e os exercícios desta fatia passam a ser só de posse compartilhada, e o vazamento do ciclo deixa de ser afirmado por estimativa: são 160 bytes por par de nós, medidos em `testes/test_posse.cpp`.',
    'objetivos': [
        'Reconhecer o requisito de domínio que exige posse compartilhada',
        'Usar <code>shared_ptr</code> e <code>weak_ptr</code>, e dizer qual dos dois conta referência',
        'Provocar um ciclo de referências e desfazê-lo',
        'Medir o que um ciclo prende, sem sanitizer nem Valgrind',
    ],
    'slides': [
        {
            'id': 'shared-weak',
            'titulo': 'shared_ptr, weak_ptr e o ciclo que o contador acusa',
            'origem': 'unidade-2/aula11-smart-pointers',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v1.3 · o grafo de conexões da estação',
                    'paragrafos': [
                        'A v1.3 monta a estação como grafo: cada <code>no_estacao</code> é um setor, e as conexões ligam setores. Aqui a posse é compartilhada por requisito, e não por preguiça, porque uma eclusa pertence aos dois corredores que ela liga, e nenhum dos dois pode destruí-la sozinho.',
                        'As ligações para frente são <code>shared_ptr</code>, e possuem. A ligação de volta é <code>weak_ptr</code>, e observa sem possuir. É essa assimetria, e não uma regra decorada, que impede o ciclo.',
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'A pergunta que decide entre as duas aulas é sobre o domínio: existe mais de um dono legítimo, cada um capaz de sobreviver ao outro? No <code>mundo</code> da Aula 12 a resposta é não, e <code>unique_ptr</code> basta. No grafo da estação a resposta é sim, e é <code>shared_ptr</code> que a expressa. Escolher <code>shared_ptr</code> porque compila mais fácil é o caminho para o ciclo.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Tipo',
                        'Possui?',
                        'Conta referência?',
                        'Uso típico, e onde no Deriva',
                    ],
                    'linhas': [
                        [
                            '<code>entidade*</code> cru',
                            'Não',
                            'Não',
                            'observação: <code>mundo::primeira_com</code>',
                        ],
                        [
                            '<code>unique_ptr</code>',
                            'Sim, e sozinho',
                            'não se aplica',
                            'posse exclusiva: as entidades do <code>mundo</code>',
                        ],
                        [
                            '<code>shared_ptr</code>',
                            'Sim, com outros',
                            'Sim',
                            'as conexões para frente do grafo',
                        ],
                        [
                            '<code>weak_ptr</code>',
                            'Não',
                            'Não',
                            'a conexão de volta, que quebra o ciclo',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'weak_ptr obriga a perguntar',
                    'paragrafos': [
                        '<code>weak_ptr</code> não se desreferencia: <code>lock()</code> devolve um <code>shared_ptr</code> ou <code>nullptr</code>, e essa pergunta é obrigatória. É ela que torna o ponteiro pendurado impossível, e é exatamente o que <code>shared_ptr</code> na volta impediria de acontecer - não porque o objeto sempre estaria vivo, mas porque ele nunca morreria.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'O que o ciclo prende, medido',
                    'paragrafos': [
                        'Trocar a ligação de volta por <code>shared_ptr</code> fecha o ciclo, e nenhum dos dois nós volta a zero: cada um segura o outro. O vazamento não dá para travar em <code>static_assert</code>, porque o tamanho do bloco de controle é escolha da implementação, então ele é medido por um alocador que conta o que o <code>shared_ptr</code> pede. São 160 bytes presos por par de nós, e o nó, com o nome e os dois ponteiros, tem 64 deles: o resto é o bloco de controle que o <code>shared_ptr</code> aloca junto.',
                        'O material afirmava 96 bytes, herdados de uma estimativa do documento de projeto. O número medido nesta libstdc++ é 160, e é ele que o portão de números confere.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-2/aula11-smart-pointers',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Em C++17, snake_case: modele um grafo de setores em que cada aresta é bidirecional e um setor pertence a todos os vizinhos que o citam. Justifique, por requisito e não por estilo, qual direção da aresta possui e qual apenas observa, e escreva o teste que prova que nenhum nó sobrevive ao fim do escopo."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'Pedido um grafo, o modelo quase sempre escreve <code>shared_ptr</code> nas duas direções, e o resultado compila, passa nos testes de comportamento e vaza. O outro erro é chamar <code>lock()</code> e desreferenciar sem conferir o resultado, o que devolve o ponteiro pendurado que o <code>weak_ptr</code> existia para impedir. O item R1 da rubrica é a pergunta que pega os dois.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Troque <code>volta_</code> de <code>weak_ptr</code> para <code>shared_ptr</code> em <code>no_estacao</code> e rode a suíte. Quais testes falham, e quais continuam passando? Explique por que os testes de comportamento não acusam nada.',
            'origem': 'unidade-2/aula11-smart-pointers',
        },
        {
            'n': '02',
            'html': 'Com o ciclo fechado, use o alocador que conta de <code>medida_posse.hpp</code> para medir quantos bytes ficam presos por par de nós. Compare com os 160 bytes que o material afirma, e diga de onde vem cada parcela.',
            'origem': 'unidade-2/aula11-smart-pointers',
        },
        {
            'n': '03',
            'html': 'Escreva um teste que faça a contagem de referências de um nó subir e voltar dentro do mesmo escopo, e afirme os valores em cada ponto com <code>use_count()</code>. Diga por que esse número não serve como detector de vazamento.',
            'origem': 'unidade-2/aula11-smart-pointers',
        },
        {
            'n': '04',
            'html': 'Destrua o nó de destino e chame <code>lock()</code> no <code>weak_ptr</code> que apontava para ele. Mostre, num teste, que o resultado é vazio, e depois escreva a versão errada, que desreferencia sem perguntar, e explique por que ela pode passar numa execução e falhar na seguinte.',
            'origem': 'unidade-2/aula11-smart-pointers',
        },
    ],
    'pendencias': [],
}
