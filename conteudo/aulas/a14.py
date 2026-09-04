# -*- coding: utf-8 -*-
"""Reescrito à mão sobre o Deriva - não rode build/extrair_v1.py aqui.

Origem no site v1: unidade-2/aula12-move-semantics, unidade-2/aula10-raii-rule-of-five
Fatia: cinco - fatia 3/3 do Cap. 10 - a regra dos cinco.
Este arquivo é a fonte de verdade do site v2 e do livro v2. O extrator do v1
sobrescreve o que está aqui; se precisar reextrair, faça em branch.
"""

AULA = {
    'n': 14,
    'slug': 'a14',
    'titulo': 'Semântica de movimento e a regra dos cinco',
    'curto': 'Movimento e a regra dos cinco',
    'unidade': 'II',
    'cap_v1': [
        12,
        10,
    ],
    'origem_v1': [
        'unidade-2/aula12-move-semantics',
        'unidade-2/aula10-raii-rule-of-five',
    ],
    'fatia': [
        'cinco',
        'fatia 3/3 do Cap. 10 - a regra dos cinco',
    ],
    'deriva': 'v1.4',
    'lab': 'LAB-08',
    'interativos': [
        'move',
    ],
    'nota_migracao': 'MIGRAÇÃO DE RISCO 1/3 (fecho). Entram std::forward e o encaminhamento perfeito, que o v1 não tinha. E a prosa foi corrigida duas vezes: `std::move` não é o que esvazia a origem, e nesta toolchain a origem esvazia nos quatro casos medidos em `testes/test_move_string.cpp` - a afirmação de estado "indeterminado que talvez preserve o conteúdo" era folclore, e `build/verifica_numeros.py` recusa a volta dela.',
    'objetivos': [
        'Distinguir lvalue de rvalue e dizer qual sobrecarga cada expressão escolhe',
        'Implementar construtor e atribuição de movimento, com <code>noexcept</code> e a razão dele',
        'Dizer o que a norma promete sobre o objeto de origem depois de um <code>std::move</code>, e o que ela não promete',
        'Reconhecer o NRVO e distinguir elisão permitida de elisão obrigatória',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Semântica de movimento: rvalues e std::move',
            'origem': 'unidade-2/aula12-move-semantics',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v1.4 · movimento em grade e mapa',
                    'paragrafos': [
                        'A v1.4 dá a <code>mapa</code> as cinco operações especiais, declaradas no mesmo lugar e com a razão de cada uma escrita ao lado. Mover um mapa transfere o buffer da grade em vez de copiar célula por célula, e o teste prova isso por identidade de endereço, que é o único jeito de ver a diferença.',
                        'O contador de instâncias vivas da Aula 7 <strong>não</strong> distingue cópia de movimento: ele conta objetos, e dois objetos nascem nos dois casos. Saber o que o instrumento não vê vale tanto quanto saber usá-lo, e é essa a lição desta aula.',
                    ],
                },
            ],
        },
        {
            'id': 'lvalue-rvalue',
            'titulo': 'lvalue e rvalue: qual sobrecarga a expressão escolhe',
            'origem': 'unidade-2/aula12-move-semantics',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A distinção que a prova cobra é entre expressões, e não entre tipos. Uma expressão é lvalue quando tem identidade, isto é, quando você pode tomar o endereço dela e o objeto continua existindo depois: uma variável nomeada, o retorno de uma função que devolve referência. Uma expressão é rvalue quando é temporária e ninguém mais a nomeia: um literal, o resultado de uma soma, um objeto construído na própria chamada.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A consequência prática é que a sobrecarga é escolhida pela <strong>categoria da expressão</strong>. Passar uma variável de <code>mapa</code> para um parâmetro por valor escolhe o construtor de cópia; passar o resultado de <code>mapa::de_texto</code>, que é temporário, escolhe o de movimento. <code>std::move</code> existe para o caso do meio: quando você tem uma variável nomeada, portanto um lvalue, e quer que a chamada seja tratada como se fosse temporária.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Expressão',
                        'Categoria',
                        'Sobrecarga escolhida',
                    ],
                    'linhas': [
                        [
                            '<code>m</code>, uma variável de <code>mapa</code>',
                            'lvalue',
                            'cópia',
                        ],
                        [
                            '<code>*mapa::de_texto(t, "s")</code>',
                            'rvalue',
                            'movimento',
                        ],
                        [
                            '<code>std::move(m)</code>',
                            'rvalue (por conversão)',
                            'movimento',
                        ],
                        [
                            '<code>std::forward&lt;T&gt;(x)</code> em parâmetro dedutível',
                            'a que o chamador passou',
                            'a que o chamador escolheu',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'std::move não move nada',
                    'paragrafos': [
                        '<code>std::move(x)</code> é uma conversão de tipo, e nada mais: ela devolve uma referência a rvalue e não toca em um byte do objeto. Quem move é o construtor, ou a atribuição, que recebe esse rvalue. Por isso <code>std::move</code> sobre um tipo que não tem movimento compila e copia, em silêncio.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'T&& dedutível não é referência a rvalue',
                    'paragrafos': [
                        'Num parâmetro de template com tipo dedutível, <code>T&amp;&amp;</code> é referência universal: o colapso de referências faz a mesma assinatura servir para lvalue e para rvalue. É o que <code>encaminhamento.hpp</code> mostra na v1.4, e é por isso que ali se escreve <code>std::forward</code> e não <code>std::move</code> - <code>std::move</code> moveria sempre, inclusive de um lvalue que quem chamou ainda vai usar, e a quebra seria silenciosa.',
                    ],
                },
            ],
        },
        {
            'id': 'move-impl',
            'titulo': 'Implementar o movimento, e o que sobra na origem',
            'origem': 'unidade-2/aula12-move-semantics',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'O construtor de movimento de <code>mapa</code> toma os recursos do argumento e deixa a origem num estado que o destrutor dela possa consumir sem erro. Ele é <code>noexcept</code>, e a palavra não é decoração: <code>std::vector&lt;mapa&gt;</code> só usa o movimento ao realocar se ele for <code>noexcept</code>, e sem a palavra o vetor copia, porque precisa poder voltar atrás se algo lançar no meio da realocação.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A atribuição de movimento não mexe no contador de instâncias, e o construtor mexe. Atribuir não cria nem destrói ninguém, apenas troca o conteúdo de dois objetos que já existiam, e é a assimetria que mais confunde na regra dos cinco.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que a norma promete sobre a origem, e o que ela não promete',
                    'paragrafos': [
                        'Depois de um movimento, a norma promete que a origem fica num estado <strong>válido mas não-especificado</strong>. Válido quer dizer que o destrutor roda, que atribuir um valor novo funciona, e que qualquer operação sem pré-condição pode ser chamada. Não-especificado quer dizer que <em>ler o valor e depender dele</em> é o que não se pode fazer.',
                        'Nesta toolchain, <code>std::move</code> sobre <code>std::string</code> <strong>esvazia a origem nos quatro casos medidos</strong>: string curta e longa, por construção e por atribuição. É justamente porque <code>REQUIRE(origem.empty())</code> passa aqui que o folclore sobrevive e o defeito embarca: o código que depende do vazio quebra na próxima implementação, e não nesta.',
                        'A diferença que de fato se reproduz entre curta e longa não é o estado da origem, é se algum byte foi copiado. Na curta, o buffer é interno ao objeto, então não há ponteiro a roubar e o destino recebe uma cópia dos caracteres, num endereço novo. Na longa, o mesmo ponteiro de heap troca de dono, e nenhum byte de conteúdo se move.',
                    ],
                },
            ],
        },
        {
            'id': 'nrvo',
            'titulo': 'NRVO: o retorno que não copia nem move',
            'origem': 'unidade-2/aula12-move-semantics',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Uma função que constrói uma variável local e a devolve por valor não precisa copiar nem mover nada: o compilador pode construir a variável diretamente no lugar do retorno. É a otimização de valor de retorno nomeado, e <code>mapa::de_texto</code> é o caso, com a variável <code>m</code> montada dentro da função e devolvida ao final.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A distinção que a prova cobra: em C++17 a elisão é <strong>obrigatória</strong> quando o que se devolve é um prvalue, isto é, um temporário sem nome; quando o que se devolve é uma variável nomeada, o compilador <em>pode</em> elidir e não é obrigado. Retornar sempre a mesma variável local ajuda; devolver variáveis diferentes em ramos diferentes de um <code>if</code> tira do compilador a chance.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Nunca escreva return std::move(local)',
                    'paragrafos': [
                        'Envolver a variável local em <code>std::move</code> no <code>return</code> transforma o que era uma variável nomeada, candidata à elisão, numa expressão rvalue que já não é a variável: o compilador perde a elisão e você paga um movimento que não existia. É um dos poucos casos em que escrever mais produz código pior, e é o erro que os modelos de linguagem mais repetem neste tópico.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-2/aula12-move-semantics',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Em C++17, snake_case: dada uma classe <code>mapa</code> que compõe uma grade com buffer em heap, escreva o construtor e a atribuição de movimento, e depois escreva um teste que prove, por identidade de endereço, que mover transferiu o buffer e copiar não. Não afirme nada sobre o valor do objeto de origem depois da operação."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'Três erros aparecem quase sempre: <code>return std::move(local)</code>, que desliga a elisão; o construtor de movimento sem <code>noexcept</code>, o que faz o <code>std::vector</code> copiar ao realocar sem avisar ninguém; e a afirmação de que a origem fica vazia, escrita como se fosse garantia da norma. O terceiro é o mais caro, porque o teste que ele gera passa nesta implementação.',
                    ],
                },
            ],
        },
        {
            'id': 'regra-cinco',
            'titulo': 'A regra dos três, do zero e dos cinco',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A regra do zero, da Aula 9, continua sendo a primeira resposta: se todos os membros já cuidam de si, não declare nenhuma das cinco operações e deixe o compilador gerá-las. <code>grade</code> é esse caso, e a cópia gerada é profunda porque o membro é um <code>std::vector</code>. A regra dos cinco vale quando você declara uma delas, porque declarar uma altera o que o compilador gera das outras.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Operação',
                        'O compilador gera?',
                        'Regra',
                    ],
                    'linhas': [
                        [
                            'Construtor padrão',
                            'Sim, se nenhum outro construtor for declarado',
                            '-',
                        ],
                        [
                            'Destrutor',
                            'Sempre, se você não o declarar',
                            'Se você o declara, declare também as outras quatro',
                        ],
                        [
                            'Cópia (construtor e atribuição)',
                            'Sim, salvo se houver movimento declarado',
                            'Regra dos três',
                        ],
                        [
                            'Movimento (construtor e atribuição)',
                            'Não, se houver destrutor ou cópia declarados',
                            'Regra dos cinco',
                        ],
                    ],
                },
                {
                    'tipo': 'codigo',
                    'lang': 'cpp',
                    'legenda': 'Quando declarar a Regra dos Cinco',
                    'codigo': """\
// Necessário quando você gerencia recurso manualmente
class raw_buffer {
    float* data_;
    std::size_t size_;
public:
    raw_buffer(std::size_t n) : data_{new float[n]}, size_{n} {}
    ~raw_buffer()                        { delete[] data_; }
    raw_buffer(const raw_buffer& o)      : data_{new float[o.size_]}, size_{o.size_}
                                         { std::copy(o.data_, o.data_+size_, data_); }
    raw_buffer& operator=(raw_buffer o)  { swap(*this, o); return *this; } // copy-and-swap
    raw_buffer(raw_buffer&& o) noexcept  : data_{o.data_}, size_{o.size_}
                                         { o.data_ = nullptr; o.size_ = 0; }
    raw_buffer& operator=(raw_buffer&& o) noexcept { swap(*this, o); return *this; }
};""",
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'Por que o Deriva não tem uma classe assim',
                    'paragrafos': [
                        'A ilustração acima existe porque o Deriva não tem onde extraí-la: não há um <code>new</code> com posse em todo o projeto, e por isso nenhuma classe precisa das cinco por gerência manual de memória. <code>mapa</code> declara as cinco por outra razão, que é instrumentar o próprio ciclo de vida, e é dele que sai o trecho extraído desta aula.',
                    ],
                },
            ],
        },
        {
            'id': 'llm-cinco',
            'titulo': 'LLMs e as operações especiais',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Em C++17, snake_case: escreva uma classe que possua um <code>FILE*</code> por RAII e aplique a regra dos cinco completa. Explique por que a atribuição usa copy-and-swap, e diga o que o compilador teria gerado se eu tivesse declarado só o destrutor."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'Declarar o destrutor e esquecer o construtor de movimento é o padrão, e o resultado compila e copia onde deveria mover. Depois vem a atribuição escrita à mão, sem copy-and-swap, que libera o recurso antes de adquirir o novo e deixa o objeto destruído se a aquisição lançar. O item R2 da rubrica é a pergunta que pega os dois.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Antes de compilar, escreva quantas construções, cópias e movimentos de <code>mapa</code> acontecem em <code>std::vector&lt;mapa&gt; v; v.push_back(*mapa::de_texto(t, "s"));</code>. Depois confira com a instrumentação de ciclo de vida da Aula 8, e explique cada diferença entre a sua previsão e o traço.',
            'origem': 'unidade-2/aula12-move-semantics',
        },
        {
            'n': '02',
            'html': 'Retire o <code>noexcept</code> do construtor de movimento de <code>mapa</code> e faça um <code>std::vector&lt;mapa&gt;</code> realocar. Mostre, pelo traço, que o vetor passou a copiar, e explique por que a garantia de exceção do vetor exige isso.',
            'origem': 'unidade-2/aula12-move-semantics',
        },
        {
            'n': '03',
            'html': 'Escreva um teste que mova um <code>std::string</code> curto e um longo, e que afirme apenas o que a norma promete. Depois escreva a versão errada, que afirma <code>origem.empty()</code>, e explique por que ela passa nesta implementação e por que isso a torna pior, e não melhor, que uma que falha.',
            'origem': 'unidade-2/aula12-move-semantics',
        },
        {
            'n': '04',
            'html': 'Troque <code>std::forward</code> por <code>std::move</code> na fábrica de <code>encaminhamento.hpp</code>. A suíte acusa? Diga qual teste cai, e o que teria acontecido se ele não existisse.',
            'origem': 'unidade-2/aula12-move-semantics',
        },
        {
            'n': '05',
            'html': 'Identifique a qual das três regras - zero, três ou cinco - pertence o defeito do código gerado em <code>revisao_ia/</code>, e aplique a regra correta. O instrumento é o traço de ciclo de vida: a cópia que ninguém pediu aparece nele.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
        {
            'n': '06',
            'html': '<code>grade</code> segue a regra do zero, e a cópia que o compilador gera é profunda. Acrescente a ela um membro <code>FILE* registro_ = nullptr;</code> e nada mais. O que passa a acontecer na cópia, e por que nenhum aviso aparece? Corrija, e diga se a correção é declarar as cinco ou trocar o membro.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
        {
            'n': '07',
            'html': 'Implemente copy-and-swap para uma classe que possua um recurso, e mostre que a atribuição continua correta mesmo se o construtor de cópia lançar. Diga em que ponto exato o objeto de destino deixa de estar em risco.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
        {
            'n': '08',
            'html': 'A variante <code>variantes/v0.3-quebrada/</code> viola a regra dos três em <code>grade</code>: destrutor declarado, cópia esquecida. Reproduza a liberação dupla sem sanitizer, usando o contador de instâncias vivas e o <code>gdb</code> com ponto de parada no destrutor, e depois conserte aplicando a regra.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
    ],
    'pendencias': [],
}
