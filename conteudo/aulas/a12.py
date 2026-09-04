# -*- coding: utf-8 -*-
"""Reescrito à mão sobre o Deriva - não rode build/extrair_v1.py aqui.

Origem no site v1: unidade-2/aula11-smart-pointers
Fatia: unique - fatia 1/2 do Cap. 11 - unique_ptr; a introdução comum (por que
ponteiro inteligente existe) vive AQUI e é referenciada, não duplicada, na
Aula 13.
Este arquivo é a fonte de verdade do site v2 e do livro v2. O extrator do v1
sobrescreve o que está aqui; se precisar reextrair, faça em branch.
"""

AULA = {
    'n': 12,
    'slug': 'a12',
    'titulo': 'Ponteiros inteligentes I - posse exclusiva',
    'curto': 'Posse exclusiva: unique_ptr',
    'unidade': 'II',
    'cap_v1': [
        11,
    ],
    'origem_v1': [
        'unidade-2/aula11-smart-pointers',
    ],
    'fatia': [
        'unique',
        'fatia 1/2 do Cap. 11 - unique_ptr; a introdução comum (por que ponteiro inteligente existe) vive AQUI e é referenciada, não duplicada, na Aula 13',
    ],
    'deriva': 'v1.2',
    'lab': None,
    'interativos': [
        'posse',
    ],
    'nota_migracao': 'MIGRAÇÃO DE RISCO 3/3. O ponteiro cru com posse entra como contraexemplo documentado, com menção ao tutorial de roguelike em C++ mais difundido (RogueBasin/libtcod), criticado justamente por isso. A fatia de posse compartilhada saiu inteira para a Aula 13, e com ela os objetivos, o slide de LLM e os exercícios que falavam de `shared_ptr`.',
    'objetivos': [
        'Ler o tipo de um contêiner e dizer quem é o dono do recurso',
        'Usar <code>unique_ptr</code> e <code>make_unique</code> para posse exclusiva',
        'Distinguir, na assinatura, transferência de posse de simples observação',
        'Justificar por que não há um <code>delete</code> em todo o Deriva',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Por que ponteiro inteligente existe, e o que unique_ptr resolve',
            'origem': 'unidade-2/aula11-smart-pointers',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v1.2 · o mundo passa a possuir as entidades',
                    'paragrafos': [
                        'A v1.2 introduz o <code>mundo</code>, que guarda as entidades num <code>std::vector&lt;std::unique_ptr&lt;entidade&gt;&gt;</code>. A posse fica declarada no tipo: o <code>mundo</code> é o dono, e nenhum comentário precisa dizer isso.',
                        'O par que amarra esta aula à anterior é <code>unique_ptr&lt;entidade&gt;</code> com destrutor virtual. Sem o destrutor virtual, este vetor destruiria só a parte base de cada objeto, e nenhum aviso apareceria, porque o <code>delete</code> mora dentro do <code>unique_ptr</code>, num cabeçalho do sistema.',
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'Ponteiro cru não diz nada sobre posse. Lendo <code>entidade* e</code> numa assinatura, você não sabe se deve destruir o objeto ao terminar, se outro alguém já vai destruí-lo, ou se ele já foi destruído. A informação existe, mas mora na documentação, ou na cabeça de quem escreveu. O ponteiro inteligente move essa informação para o <strong>tipo</strong>, onde o compilador a lê e o revisor não precisa perguntar.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Esta é a introdução comum aos dois tipos de posse, e ela vive aqui: a Aula 13, que trata da posse compartilhada, aponta para esta página em vez de repetir o argumento.',
                },
            ],
        },
        {
            'id': 'unique',
            'titulo': 'unique_ptr: posse exclusiva declarada no tipo',
            'origem': 'unidade-2/aula11-smart-pointers',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': '<code>std::unique_ptr</code> possui, e possui sozinho. Ele não se copia, e a tentativa de copiá-lo é erro de compilação, e não bug em produção; ele se move, e mover é justamente o gesto de transferir a posse. <code>std::make_unique</code> constrói o objeto e o embrulha numa expressão, de forma que não sobra um <code>new</code> solto a que ninguém corresponda.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'O que a assinatura diz',
                        'Como se escreve',
                        'Onde aparece no Deriva',
                    ],
                    'linhas': [
                        [
                            'toma posse',
                            '<code>std::unique_ptr&lt;entidade&gt;</code> por valor',
                            '<code>mundo::acrescentar</code>',
                        ],
                        [
                            'devolve posse',
                            '<code>[[nodiscard]] std::unique_ptr&lt;entidade&gt;</code>',
                            '<code>mundo::retirar_de</code>',
                        ],
                        [
                            'observa, sem posse',
                            '<code>entidade*</code> ou <code>entidade&amp;</code>',
                            '<code>mundo::primeira_com</code>',
                        ],
                        [
                            'usa durante a chamada',
                            '<code>const entidade&amp;</code>',
                            '<code>inspecionar</code>, na Aula 18',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Devolver posse e ignorar o retorno destrói o objeto',
                    'paragrafos': [
                        '<code>mundo::retirar_de</code> devolve <code>std::unique_ptr&lt;entidade&gt;</code>, e quem chamou passa a ser o dono. Ignorar esse retorno destrói a entidade na mesma linha, em silêncio. O <code>[[nodiscard]]</code> na declaração existe por isso, e transforma o descuido em aviso do compilador.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'O ponteiro cru como contraexemplo, não como proibição',
                    'paragrafos': [
                        'Ponteiro cru continua correto para <strong>observar</strong>, e <code>mundo::primeira_com</code> devolve um de propósito: ali a resposta pode ser "nenhuma", e a chamada não transfere nada. O que o material trata como contraexemplo é o ponteiro cru <em>com posse</em>, aquele para o qual existe um <code>delete</code> em algum lugar. No Deriva não existe nenhum.',
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
                        '<em>"Em C++17, snake_case: escreva uma classe <code>mundo</code> que possui suas entidades com posse exclusiva. Quero três assinaturas distintas: uma que toma posse, uma que devolve posse e uma que apenas observa, e quero que a diferença entre as três esteja no tipo de retorno e de parâmetro, sem comentário explicando."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'O erro mais comum é usar <code>std::shared_ptr</code> onde <code>unique_ptr</code> mais uma referência resolveria, porque posse compartilhada é mais fácil de explicar e nunca falha na compilação. O segundo é devolver <code>unique_ptr</code> sem <code>[[nodiscard]]</code>. Pergunte sempre quem é o dono, e exija que a resposta esteja na assinatura.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Tente copiar um <code>mundo</code>. O compilador recusa, e por duas razões que se somam: a cópia está <code>= delete</code>, e o <code>vector&lt;unique_ptr&lt;entidade&gt;&gt;</code> não seria copiável de todo modo. Explique cada uma, e diga o que uma cópia correta do <code>mundo</code> exigiria.',
            'origem': 'unidade-2/aula11-smart-pointers',
        },
        {
            'n': '02',
            'html': 'Chame <code>mundo::retirar_de</code> e descarte o retorno. Que aviso aparece, e o que aconteceu com a entidade? Depois guarde o retorno numa variável, deixe-a sair de escopo, e confira o contador de instâncias vivas da classe concreta.',
            'origem': 'unidade-2/aula11-smart-pointers',
        },
        {
            'n': '03',
            'html': 'Troque o <code>std::unique_ptr&lt;entidade&gt;</code> do <code>mundo</code> por <code>entidade*</code> e faça o programa voltar a compilar, com os <code>delete</code> que passam a ser necessários. Conte quantos lugares você teve de mexer, e quantas maneiras de errar o novo desenho permite.',
            'origem': 'unidade-2/aula11-smart-pointers',
        },
        {
            'n': '04',
            'html': 'O trecho de <code>medida_posse.hpp</code> mede o tamanho de <code>unique_ptr</code> com deletor padrão, com deletor vazio e com deletor com estado. Antes de rodar, escreva os três valores que você espera, e depois explique o que a otimização de base vazia faz com o segundo caso.',
            'origem': 'unidade-2/aula11-smart-pointers',
        },
    ],
    'pendencias': [],
}
