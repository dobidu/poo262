# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-1/aula08-classes-objetos
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Pendências desta aula: 0 (ver conteudo/PENDENCIAS.md)
"""

AULA = {
    'n': 7,
    'slug': 'a07',
    'titulo': 'Classes e objetos; o contador de instâncias vivas',
    'curto': 'Classes, objetos e o contador `vivos`',
    'unidade': 'I',
    'cap_v1': [
        8,
    ],
    'origem_v1': [
        'unidade-1/aula08-classes-objetos',
    ],
    'fatia': None,
    'deriva': 'v0.1',
    'lab': 'LAB-04',
    'interativos': [
        'inspetor',
    ],
    'nota_migracao': 'Membros estáticos ganham o exemplo canônico da disciplina: static int vivos, incrementado no construtor e decrementado no destrutor. É o detector de vazamento que a disciplina usa por 19 capítulos, e é o que motiva o template do Cap. 19.',
    'objetivos': [
        'Declarar e definir classes com encapsulamento correto (public/protected/private)',
        'Compreender o papel do ponteiro <code>this</code>',
        'Aplicar <em>const</em>-correctness em métodos, parâmetros e variáveis',
        'Usar membros <code>static</code> para dados compartilhados por instâncias',
        'Separar interface (<code>.hpp</code>) de implementação (<code>.cpp</code>), e reconhecer quando a separação não se paga',
        'Escrever o contador de instâncias vivas, e reconhecer o que ele acusa e o que ele não acusa',
        'Determinar o tamanho de um objeto a partir da ordem de declaração dos seus membros',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Classes e Objetos em C++',
            'origem': 'unidade-1/aula08-classes-objetos',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'Onde a v0.1 mora, arquivo por arquivo',
                    'paragrafos': [
                        '<code>include/deriva/vetor2.hpp</code> é a primeira “classe” do Deriva, e ela é um <code>struct</code> com dois <code>int</code> públicos. Isso não é descuido, é a decisão: <strong>não há invariante a proteger</strong>. Qualquer par de inteiros é um <code>vetor2</code> válido, inclusive um fora da grade, porque <code>vetor2</code> também serve de deslocamento; pôr os campos em <code>private</code> e escrever <code>x()</code> e <code>set_x()</code> acrescentaria cerimônia e nenhuma garantia.',
                        '<code>include/deriva/celula.hpp</code> é o que há numa posição, e o arquivo traz de propósito duas versões dos mesmos quatro campos: <code>celula</code>, agrupada por tamanho, ocupa 12 bytes; <code>celula_ingenua</code>, na ordem em que se pensa nela, ocupa 16. Os <code>static_assert</code> no fim do arquivo afirmam os dois números, e é isso que impede este material de mentir sobre eles.',
                        '<code>include/deriva/contador.hpp</code> é o contador de instâncias vivas, que é o detector de vazamento da disciplina e não depende de sanitizer nenhum. Ele reaparece por dezenove aulas, e é ele que sustenta a quarta condição do portão <code>make verifica</code>.',
                    ],
                },
            ],
        },
        {
            'id': 'separacao',
            'titulo': 'Separação de Interface e Implementação',
            'origem': 'unidade-1/aula08-classes-objetos',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Em C++, a convenção é separar a <strong>declaração</strong> - o contrato - em <code>.hpp</code>, e a <strong>definição</strong> - a implementação - em <code>.cpp</code>. Isso reduz o tempo de recompilação e mantém o detalhe de implementação fora do que quem chama precisa ler.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A separação, porém, não é obrigatória, e o Deriva a usa de forma <strong>desigual de propósito</strong>. <code>grade</code> e <code>mapa</code> têm cabeçalho e implementação, porque os métodos deles têm corpo grande e validação; <code>vetor2</code> e <code>celula</code> vivem inteiros no cabeçalho, sem <code>.cpp</code> nenhum, porque são agregados de dois e de quatro campos com operadores <code>constexpr</code> de uma linha, e criar um arquivo de implementação para eles acrescentaria um arquivo e nenhuma informação. O par completo está extraído mais abaixo nesta página: a declaração em <code>grade.hpp</code>, e a definição qualificada por <code>grade::</code>, fora da classe, em <code>src/grade.cpp</code>.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Guarda de inclusão: o Deriva usa #ifndef',
                    'paragrafos': [
                        'Todo cabeçalho do Deriva abre com <code>#ifndef DERIVA_ALGO_HPP</code> / <code>#define</code> e fecha com <code>#endif</code>. A alternativa <code>#pragma once</code> é uma linha só e todo compilador atual a entende, e é por isso que você vai encontrá-la em muito código - porém ela não está no padrão, e este projeto compila com <code>CMAKE_CXX_EXTENSIONS OFF</code> justamente para não depender do que está fora dele.',
                        'Se você usar <code>#pragma once</code>, use-o de forma consistente no projeto inteiro: o defeito não é escolher um dos dois, é misturar os dois no mesmo diretório e depois não saber qual arquivo está protegido por qual mecanismo.',
                    ],
                },
            ],
        },
        {
            'id': 'acesso',
            'titulo': 'Modificadores de Acesso',
            'origem': 'unidade-1/aula08-classes-objetos',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Modificador',
                        'Quem pode acessar',
                        'Uso típico',
                    ],
                    'linhas': [
                        [
                            '<code>public</code>',
                            'Qualquer código',
                            'Interface: construtores, getters, operadores',
                        ],
                        [
                            '<code>private</code>',
                            'Apenas a própria classe',
                            'Dados internos, métodos auxiliares',
                        ],
                        [
                            '<code>protected</code>',
                            'Própria classe + derivadas',
                            'Dados que subclasses precisam acessar',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Regra de ouro, e a exceção que ela tem',
                    'paragrafos': [
                        'Comece tudo como <code>private</code>. Torne <code>public</code> apenas o necessário para o contrato da classe. Use <code>protected</code> somente ao projetar herança, e mesmo assim prefira função de acesso protegida a dado diretamente protegido.',
                        'A exceção é a que esta aula já usou: quando a classe não tem invariante nenhuma, o <code>private</code> não protege nada, e o tipo é melhor como agregado de campos públicos. <code>vetor2</code> e <code>celula</code> são assim, e é por isso que ligação estruturada funciona sobre eles. Encapsular é meio, e a invariante é o fim.',
                    ],
                },
            ],
        },
        {
            'id': 'const',
            'titulo': 'Const-Correctness',
            'origem': 'unidade-1/aula08-classes-objetos',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Marque como <code>const</code> tudo que não deve ser modificado. O compilador confere isso em tempo de compilação, e é o que faz da palavra documentação executável: ela não descreve a intenção, ela a impõe. No Deriva, <code>const</code> e <code>[[nodiscard]]</code> andam juntos, porque marcam a mesma coisa por ângulos diferentes - um método <code>const</code> que devolve valor e não altera nada tem exatamente uma finalidade, que é o valor devolvido, e descartar esse valor não pode ser intencional.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Forma',
                        'O que promete',
                        'No Deriva',
                    ],
                    'linhas': [
                        [
                            'Método <code>const</code>',
                            'não altera o objeto sobre o qual foi chamado',
                            '<code>grade::largura() const</code>, <code>grade::dentro(vetor2) const</code>, <code>mapa::despejar() const</code>',
                        ],
                        [
                            'Parâmetro <code>const&amp;</code>',
                            'não copia, e só lê',
                            '<code>operator&lt;&lt;(std::ostream&amp;, const mapa&amp;)</code>, que por isso só alcança método <code>const</code>',
                        ],
                        [
                            'Retorno <code>const&amp;</code>',
                            'dá acesso de leitura sem dar acesso de escrita',
                            '<code>const celula&amp; em(vetor2) const</code>, a primeira do par de sobrecargas',
                        ],
                        [
                            'Objeto <code>const</code>',
                            'só permite chamar método <code>const</code>',
                            '<code>const grade g(20, 10)</code>, no trecho extraído mais abaixo',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'O par de sobrecargas de <code>grade::em()</code> merece atenção, porque é ele que junta as quatro formas numa só decisão. Há uma versão <code>const</code> que devolve <code>const celula&amp;</code> e uma versão não-const que devolve <code>celula&amp;</code>, e as duas existem porque o compilador escolhe pela constância do objeto: numa <code>grade</code> const, só a primeira é viável, e ela não deixa ninguém escrever na célula. Uma sobrecarga só, devolvendo referência não-const, permitiria escrever através de um objeto constante; devolvendo referência const, impediria escrever em qualquer um. É assim que uma classe fica utilizável em contexto de leitura sem abrir mão da escrita em contexto de escrita.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Do lado de quem consome a classe, o mesmo <code>const</code> aparece no parâmetro. Tirar o <code>const</code> de <code>operator&lt;&lt;(std::ostream&amp;, const mapa&amp;)</code> não mudaria uma linha do corpo dela, e faria o programa deixar de compilar em todo lugar que passe um mapa constante - o que é a prova de que a palavra não é decoração.',
                },
            ],
        },
        {
            'id': 'this',
            'titulo': 'O Ponteiro this e Interface Fluente',
            'origem': 'unidade-1/aula08-classes-objetos',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Dentro de qualquer função membro não-estática existe um ponteiro para o objeto sobre o qual a chamada aconteceu, e ele se chama <code>this</code>. Está lá mesmo quando ninguém o escreve: <code>grade::largura()</code> devolve <code>largura_</code>, e o que ela de fato devolve é <code>this-&gt;largura_</code>. Explicitá-lo se paga quando o objeto precisa ser mencionado inteiro, e não um membro dele.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Os dois usos que o Deriva tem estão em <code>mapa::operator=</code>, e o trecho está extraído mais abaixo nesta página. O primeiro é <code>if (this != &amp;o)</code>, a guarda de autoatribuição: sem ela, <code>m = m</code> liberaria os recursos do objeto antes de copiá-los de si mesmo. O segundo é <code>return *this</code>, que devolve referência ao próprio objeto e é o que permite escrever <code>a = b = c</code>, encadeando à direita como manda a linguagem. Fora desses dois lugares, <code>this</code> é implícito em todo o projeto, e escrevê-lo seria ruído.',
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'O Deriva não tem interface fluente, e é decisão',
                    'paragrafos': [
                        'Encadear <code>set_x().set_y()</code> exige que todo modificador devolva <code>*this</code>. Inventar essa cadeia no sistema só para demonstrar <code>this</code> seria acrescentar cerimônia ao código a serviço do material, que é a inversão que este material evita.',
                        'Onde você encontrar interface fluente em biblioteca de terceiro - e vai encontrar, em montador de consulta e de configuração - o mecanismo é este, e a partir daqui você o reconhece.',
                    ],
                },
                {
                    'tipo': 'mermaid',
                    'trecho': 'uml-agregados',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O desenho da v0.1 tem quatro caixas e <strong>nenhuma linha entre elas</strong>, e é isso que ele tem a dizer: nesta altura do Deriva não há herança nem composição, há quatro tipos e a decisão, tomada tipo por tipo, de encapsular ou não. <code>celula</code> e <code>celula_ingenua</code> declaram os mesmos quatro campos em ordens diferentes, e o compartimento do meio é onde a diferença de tamanho aparece antes de custar memória. Em <code>contador_mapa</code>, o <code>$</code> marca membro estático, que é a convenção da notação para o que <strong>não está dentro do objeto</strong>.',
                },
            ],
        },
        {
            'id': 'static',
            'titulo': 'Membros static',
            'origem': 'unidade-1/aula08-classes-objetos',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Membros <code>static</code> pertencem à classe, e não a instâncias individuais: uma variável estática é compartilhada por todos os objetos, e um método estático pode ser chamado sem que exista objeto algum. A consequência que mais confunde, e que o interativo desta aula mostra, é que <strong>o membro estático não está dentro do objeto</strong>. Acrescentar um <code>static int</code> a uma classe não muda o <code>sizeof</code> dela: a variável vive uma única vez, em memória estática, e todos os objetos falam da mesma. É por isso que ela serve de contador.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Antes do C++17, declarar um dado estático mutável exigia dois lugares: a declaração ia na classe, dentro do cabeçalho, e a definição ia em exatamente um <code>.cpp</code>, porque a declaração não reserva memória e a regra de uma definição só exige que a reserva aconteça uma vez em todo o programa. O C++17 acabou com a dança através de <strong>variável inline</strong>: <code>inline static int vivos = 0;</code> declara e define na mesma linha, dentro do cabeçalho, e o ligador aceita a repetição em todas as unidades de tradução que incluírem o arquivo. O contador precisa mudar de valor, então <code>constexpr</code> não serve; <code>inline static</code> serve.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A forma do contador cabe numa frase: <strong>incrementa no construtor, decrementa no destrutor; se não fecha em zero no fim de <code>main</code>, um destrutor não rodou.</strong> São duas variáveis, e não uma: <code>vivos</code> sobe e desce, <code>criados</code> só sobe, e a diferença entre elas diz quantos objetos morreram. É o que permite responder à pergunta da Aula 09 - quantos objetos foram construídos para produzir um mapa. Os dois trechos extraídos mais abaixo nesta página são a declaração e o uso.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o contador NÃO acusa',
                    'paragrafos': [
                        'Ele conta objetos, e não recursos. Na variante com cópia rasa da Aula 09, duas grades apontam para o mesmo bloco de memória, os dois objetos são construídos e destruídos corretamente, o contador <strong>fecha em zero</strong>, e o programa libera a mesma memória duas vezes. Reconhecer esse limite é parte da lição.',
                        'Ele também não é seguro entre threads - a Aula 22 mostra exatamente esta variável perdendo um incremento -, e é escrito à mão em cada classe que o quer, repetição deliberada que é o que motiva generalizá-lo em <code>contador_de_instancias&lt;T&gt;</code> por CRTP na Aula 19. Template que chega antes de o estudante sentir a repetição é solução para um problema que ele não teve.',
                        'E o incremento tem de estar em <strong>todos</strong> os construtores, inclusive no de cópia. Sem ele, o destrutor da cópia decrementaria algo que ninguém incrementou, e <code>vivos</code> fecharia negativo. Contador que fecha em número negativo não é falso alarme: é o mesmo defeito visto pelo outro lado.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-1/aula08-classes-objetos',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt de modelagem de classe',
                    'paragrafos': [
                        '<em>"Preciso da classe <code>grade</code> em C++17 para o projeto Deriva. Convenções: snake_case, identificadores e comentários em português. Requisitos: guarda as células em <code>std::vector&lt;celula&gt;</code>, e <code>celula</code> já existe; o construtor recebe largura e altura e valida que as duas são positivas <strong>na lista de inicialização</strong>, e não no corpo; métodos <code>largura()</code>, <code>altura()</code>, <code>dentro(vetor2)</code> e o par de sobrecargas const e não-const de <code>em(vetor2)</code>; todo método que não altera o objeto é <code>const</code>, e todo método que só devolve valor é <code>[[nodiscard]]</code>; nenhuma das seis operações especiais é declarada, pela regra do zero. Portão: compila com <code>-std=c++17 -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion</code> sem uma linha de aviso."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM provavelmente vai errar',
                    'paragrafos': [
                        'Sem instrução explícita, ele costuma: usar PascalCase no nome do tipo; validar no corpo do construtor em vez de na lista de inicialização; devolver <code>celula&amp;</code> numa sobrecarga só, sem a versão <code>const</code>; e declarar destrutor vazio, o que sai da regra do zero e passa a exigir as cinco operações. Confira o item R3 da rubrica antes de qualquer outra coisa.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Implemente <code>include/deriva/vetor2.hpp</code> do zero, sem olhar o arquivo: um agregado com <code>x</code> e <code>y</code>, os operadores de igualdade e desigualdade <code>constexpr</code>, <code>noexcept</code> e <code>[[nodiscard]]</code>, e um <code>static_assert</code> afirmando o <code>sizeof</code> que você prevê. Compile com o conjunto de avisos da Aula 02 e confirme que não há uma linha de aviso.',
            'origem': 'unidade-1/aula08-classes-objetos',
        },
        {
            'n': '02',
            'html': 'Implemente <code>grade</code> com cabeçalho e implementação separados: construtor com largura e altura, <code>largura()</code>, <code>altura()</code>, <code>dentro(vetor2)</code> e o par de sobrecargas de <code>em(vetor2)</code>. Marque como <code>const</code> todo método que não altera o objeto e como <code>[[nodiscard]]</code> todo o que só devolve valor. Depois tente, de propósito, chamar a versão não-const de <code>em()</code> numa <code>grade</code> const, e leia a mensagem do compilador até entendê-la.',
            'origem': 'unidade-1/aula08-classes-objetos',
        },
        {
            'n': '03',
            'html': 'Acrescente o contador de instâncias vivas a <code>grade</code>, com <code>inline static int vivos</code> e <code>inline static int criados</code>. Escreva um <code>main</code> que cria três grades e imprime o contador; destrói uma usando escopo e imprime; <strong>copia</strong> uma e imprime; e no fim confirma que <code>vivos</code> voltou a zero. Explique cada número <strong>antes</strong> de rodar o programa, e só então rode. Este é o portão do LAB-04.',
            'origem': 'unidade-1/aula08-classes-objetos',
        },
        {
            'n': '04',
            'html': 'Faça o contador fechar em número <strong>negativo</strong>, de propósito: declare o construtor de cópia e esqueça o incremento nele. Rode o exercício 3 outra vez. Por que o número é negativo, e o que isso diz sobre onde o incremento tem de estar? Depois declare uma <code>struct</code> com um <code>char</code>, um <code>double</code> e um <code>int</code>, nessa ordem, escreva o <code>static_assert</code> com o tamanho que você prevê, e compile: se errou, reordene os campos para obter o menor tamanho possível e explique de onde vem cada byte de padding.',
            'origem': 'unidade-1/aula08-classes-objetos',
        },
    ],
    'pendencias': [],
}
