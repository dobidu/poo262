# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-2/aula10-raii-rule-of-five
Fatia: zero-tres - fatia 2/3 do Cap. 10 - cópia e atribuição; a regra dos cinco vai para a Aula 14, já na Unidade II
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Pendências desta aula: 0 (ver conteudo/PENDENCIAS.md)
"""

AULA = {
    'n': 9,
    'slug': 'a09',
    'titulo': 'Operações especiais: a regra do zero e do três',
    'curto': 'Regra do zero e do três',
    'unidade': 'I',
    'cap_v1': [
        10,
    ],
    'origem_v1': [
        'unidade-2/aula10-raii-rule-of-five',
    ],
    'fatia': [
        'zero-tres',
        'fatia 2/3 do Cap. 10 - cópia e atribuição; a regra dos cinco vai para a Aula 14, já na Unidade II',
    ],
    'deriva': 'v0.3',
    'lab': None,
    'interativos': [
        'ciclo',
    ],
    'nota_migracao': 'MIGRAÇÃO DE RISCO 1/3 (continuação). Atenção: a regra dos cinco atravessa fronteira de unidade e de prova.',
    'objetivos': [
        'Compreender a regra do zero: quando o compilador gera tudo, e melhor do que se escreveria à mão',
        'Aplicar a regra dos três nas suas duas formas - a longa, com destrutor, cópia e atribuição; e a curta, com <code>= delete</code>',
        'Reconhecer a cópia rasa <strong>no texto do código</strong>, antes de executá-lo',
        'Saber o que o contador de instâncias vivas acusa e o que ele deixa passar',
        'Conduzir a caça ao bug 1 na ordem: reproduzir, explicar em uma frase, corrigir, provar',
    ],
    'slides': [
        {
            'id': 'regra-zero',
            'titulo': 'Regra do Zero',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Se a sua classe gerencia recurso apenas através de tipos RAII da biblioteca padrão - <code>std::vector</code>, <code>std::string</code>, <code>std::unique_ptr</code> e assemelhados -, declare <strong>zero</strong> das seis operações especiais. O compilador gera versões corretas, que chamam a operação correta de cada membro. A regra do zero é a primeira escolha, e não um caso particular.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Ela tem duas vantagens, e a segunda é a que mais paga a longo prazo. A primeira é que as operações geradas são melhores do que as que escreveríamos: o compilador copia cada membro com o construtor de cópia daquele membro, move cada um com o de movimento, destrói na ordem inversa da construção, e não erra. A segunda é que elas <strong>não podem ficar desatualizadas</strong> - quando um membro novo aparece na classe, as operações geradas passam a tratá-lo no mesmo commit, sem que ninguém precise lembrar. Cópia escrita à mão precisa ser atualizada a cada membro novo, e o defeito de esquecer não produz aviso nenhum: o campo simplesmente não é copiado, e a classe passa a ter dois estados que divergem em silêncio.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A <code>grade</code> do Deriva é a regra do zero em forma pura, e o trecho está extraído mais abaixo nesta página: o que vale ler nele é o que <strong>não</strong> está escrito. Vale também copiar o hábito do cabeçalho dela, que lista em comentário as operações que não foram declaradas, para que quem lê saiba que a omissão é decisão, e não esquecimento.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O oposto está na variante <code>v0.3-quebrada/</code>, extraída ao lado e marcada como quebrada de propósito: ela guarda <code>celula*</code> cru, declara <code>~grade()</code> com <code>delete[]</code>, e não declara construtor de cópia nem atribuição. A cópia que o compilador gera copia o <strong>ponteiro</strong>, e não o buffer: duas grades, um buffer, dois <code>delete[]</code>. Declarar destrutor e esquecer a cópia é a violação mais barata da regra do três, e a que mais sobrevive à revisão - <code>-Wall -Wextra -Wpedantic</code> não emite uma palavra sobre ela, porque a linguagem está fazendo exatamente o que foi pedida.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Quando a regra do zero é impossível',
                    'paragrafos': [
                        'Apenas quando a classe gerencia um recurso que não tem tipo RAII pronto: socket, descritor de arquivo à moda de C, o modo do terminal da Aula 08. Nesses casos, encapsule o recurso numa classe dedicada e use a regra do zero em todo o resto.',
                        'O Deriva tem uma exceção a mais, e vale registrá-la para que a regra não pareça absoluta: <code>mapa</code> declara destrutor e cópia, e não por gerenciar recurso - é para mexer no contador de instâncias vivas. O preço é o da linha seguinte da tabela: a partir do momento em que o destrutor foi declarado, o compilador deixou de gerar as operações de movimento, e é a Aula 14 que fecha essa conta.',
                    ],
                },
            ],
        },
        {
            'id': 'regra-cinco',
            'titulo': 'A Regra dos Três, e as suas duas formas',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Onde a classe gerencia o recurso à mão - <code>celula*</code> cru com posse, descritor de arquivo, socket, o modo do terminal de <code>terminal_bruto</code> -, três operações andam juntas: destrutor, construtor de cópia e <code>operator=</code> de cópia. E o defeito não é a falta das três, que ninguém comete: é declarar <strong>uma</strong> e esquecer as outras duas. O compilador continua gerando a que faltou, e a que ele gera copia membro a membro, de forma que o ponteiro é duplicado e o recurso não. Ficam dois objetos apontando para o mesmo recurso, cada um com um destrutor pronto para liberá-lo.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Se você declarar...',
                        'o compilador NÃO gera...',
                    ],
                    'linhas': [
                        [
                            'qualquer construtor',
                            'o construtor padrão',
                        ],
                        [
                            'o destrutor',
                            'construtor e atribuição de movimento',
                        ],
                        [
                            'o construtor de cópia',
                            'construtor e atribuição de movimento',
                        ],
                        [
                            'a atribuição de cópia',
                            'construtor e atribuição de movimento',
                        ],
                        [
                            'o construtor de movimento',
                            'construtor e atribuição de cópia',
                        ],
                        [
                            'a atribuição de movimento',
                            'construtor e atribuição de cópia',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'A segunda linha da tabela é a que se costuma explicar errado, e no Deriva ela está medida. <code>mapa</code> declara destrutor e cópia, porque precisa mexer no contador de instâncias vivas; com isso, o compilador <strong>deixa de gerar</strong> as operações de movimento, e é a Aula 14 que passa a declará-las à mão. O que se espera dessa correção é que ela poupe construções, e não é o que acontece: <code>testes/test_mapa.cpp</code> mede os dois estados do código e afirma que <code>de_texto</code> custa <strong>duas</strong> construções com o construtor de movimento e duas sem ele - a do mapa local e a do que vai para dentro do <code>std::optional</code>. O que o movimento muda é o <em>custo</em> da segunda construção, e não o número delas; guarde o número e guarde a surpresa, porque os dois são o argumento da regra dos cinco, na Aula 14.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A regra dos três tem <strong>duas</strong> formas de ser cumprida, e a mais curta é a que se esquece. A <strong>forma longa</strong> é escrever as três: destrutor que libera, construtor de cópia que faz cópia profunda, e operador de atribuição que aloca o novo antes de liberar o antigo, com guarda de autoatribuição. É o que <code>mapa</code> faz, e o trecho está extraído mais abaixo nesta página; a ordem que o operador obedece é sempre a mesma e vale memorizá-la - <strong>aloca o novo, copia para dentro dele, libera o antigo, assume o novo</strong> -, porque liberar antes de alocar é o defeito clássico: a alocação pode falhar, e o objeto fica sem nenhum dos dois estados.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A <strong>forma curta</strong> é declarar as duas operações de cópia <code>= delete</code>, e é o que <code>terminal_bruto</code> faz. Ela cabe quando o recurso é único por natureza: há exatamente um terminal, e posse de recurso único não se duplica. Aí a regra dos três se cumpre em duas linhas, e a classe deixa de ter uma categoria inteira de defeitos por não ter a operação. As duas formas estão extraídas mais abaixo, e as duas vêm de código que compila.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Caça ao bug 1: cópia rasa em grade, semana 5',
                    'paragrafos': [
                        'O protocolo tem quatro passos, e a ordem é cobrada: <strong>reproduzir a falha; explicá-la em uma frase, por escrito, antes de tocar no código; corrigir; provar a correção.</strong> Os sete itens da rubrica da Aula 04 se aplicam por escrito.',
                        'O roteiro de observação são cinco olhares sobre o mesmo defeito, e o que se aprende é tanto o que cada instrumento vê quanto o que ele deixa de ver. Sem ferramenta nenhuma: escrever numa célula de <code>b</code> muda a célula correspondente de <code>a</code>, e os dois buffers têm o mesmo endereço - isto basta para o diagnóstico, e é o único caminho disponível no laboratório. Com o contador de instâncias vivas: ele <strong>fecha em zero</strong>, e é isso que engana. Com o alocador: a glibc pode abortar, e não é para se confiar, porque a detecção depende do arranjo das alocações. Com o ASan, se a sua máquina o tiver: as duas pilhas de liberação nomeadas. Com o compilador: nada.',
                        'E o conserto certo é o mais curto. Escrever o construtor de cópia e a atribuição funciona, e é o que a regra dos três manda; a resposta melhor é <strong>apagar o destrutor</strong> - trocar <code>celula*</code> por <code>std::vector&lt;celula&gt;</code> e voltar à regra do zero, com as cinco operações corretas de graça, inclusive as duas de movimento, que a versão escrita à mão não teria. Quantas linhas a mais a versão com <code>vector</code> tem? Nenhuma.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Este código em C++17 declara destrutor e não declara construtor de cópia nem atribuição de cópia. Diga, sem executá-lo: o que acontece quando um objeto dele é copiado, quantas vezes o recurso é liberado, e qual é o defeito em uma frase. Depois mostre as duas correções possíveis - a regra dos três escrita à mão, e o retorno à regra do zero - e conte as linhas de cada uma."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'Ele quase sempre oferece a forma longa, porque é a que aparece em todo tutorial, e quase nunca oferece a forma curta - o <code>= delete</code> - nem o retorno à regra do zero, que são as duas respostas melhores. Peça explicitamente as três alternativas e a contagem de linhas de cada uma.',
                        'E desconfie quando ele afirmar que o contador de instâncias vivas acusaria a cópia rasa. Não acusa: os dois objetos nascem e morrem corretamente, e o contador fecha em zero. Modelo que afirma o contrário está deduzindo de um padrão, e não do código que você mostrou.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Implemente <code>grade</code> pela regra do zero, com <code>std::vector&lt;celula&gt;</code> internamente. Verifique com testes que cópia, atribuição e destruição funcionam sem que você escreva uma linha para isso: escreva numa célula da cópia e confirme que a original não mudou.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
        {
            'n': '02',
            'html': 'Tome a sua <code>grade</code> do exercício 1 e quebre-a de propósito, como a <code>v0.3-quebrada</code>: troque o vetor por <code>celula*</code>, acrescente o destrutor com <code>delete[]</code>, e <strong>não</strong> escreva a cópia. Percorra os cinco olhares desta aula nesta ordem, e escreva, para cada um, o que ele acusou e o que ele deixou passar.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
        {
            'n': '03',
            'html': 'Escreva a frase única que explica o defeito do exercício 2, <strong>antes</strong> de consertá-lo. A frase precisa dizer o que acontece, e não o que fazer. Depois conserte pelas duas vias - a forma longa da regra dos três, e o retorno à regra do zero - e compare o número de linhas de cada conserto.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
        {
            'n': '04',
            'html': '<code>terminal_bruto</code> cumpre a regra dos três em duas linhas de <code>= delete</code>. Explique por que a forma longa seria <strong>errada</strong> nesse caso, e não apenas desnecessária: o que faria o segundo destrutor? Depois rode <code>testes/test_mapa.cpp</code>, confirme quantas construções <code>de_texto</code> custa, e diga por que o contador de instâncias vivas é incapaz de mostrar a diferença que a Aula 14 vai introduzir.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
    ],
    'pendencias': [],
}
