# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-1/aula09-ciclo-de-vida, unidade-2/aula10-raii-rule-of-five
Fatia: raii - fatia 1/3 do Cap. 10 - só RAII
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Pendências desta aula: 0 (ver conteudo/PENDENCIAS.md)
"""

AULA = {
    'n': 8,
    'slug': 'a08',
    'titulo': 'Ciclo de vida e RAII',
    'curto': 'Ciclo de vida e RAII',
    'unidade': 'I',
    'cap_v1': [
        9,
        10,
    ],
    'origem_v1': [
        'unidade-1/aula09-ciclo-de-vida',
        'unidade-2/aula10-raii-rule-of-five',
    ],
    'fatia': [
        'raii',
        'fatia 1/3 do Cap. 10 - só RAII',
    ],
    'deriva': 'v0.2',
    'lab': 'LAB-05',
    'interativos': [
        'ciclo',
    ],
    'nota_migracao': 'MIGRAÇÃO DE RISCO 1/3 - absorve o RAII que estava no Cap. 10. Entra a instrumentação de ciclo de vida (construtores e destrutores imprimindo a própria execução) e o terminal_bruto.',
    'objetivos': [
        'Dominar os tipos de construtores: padrão, parametrizado, de cópia e de conversão',
        'Usar a lista de inicialização, e saber por que a validação de argumento tem de estar nela',
        'Determinar a ordem exata de construção e destruição de um trecho <strong>sem executá-lo</strong>',
        'Aplicar RAII como idioma, e reconhecer o recurso que sobrevive ao processo',
        'Instrumentar construtores e destrutores, e ler o traço que eles produzem',
        'Provar que o desenrolar da pilha por exceção chama os destrutores, em vez de pulá-los',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Ciclo de Vida: Construtores, Destrutores e RAII',
            'origem': 'unidade-1/aula09-ciclo-de-vida',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'A v0.2 entrega duas coisas, e as duas são ciclo de vida',
                    'paragrafos': [
                        '<code>grade</code>, com o construtor que valida largura e altura <strong>na lista de inicialização</strong> e dimensiona o vetor de células uma vez só. Nenhuma das operações especiais é declarada, e é a regra do zero: o <code>std::vector</code> já sabe se copiar, se mover e se destruir.',
                        '<code>terminal_bruto</code>, que põe o terminal em modo bruto no construtor e o restaura no destrutor. É o melhor exemplo de RAII que existe, e não é metáfora: se o destrutor não rodar, o terminal fica sem eco e sem Enter <strong>depois</strong> que o programa sai.',
                        'E entre as duas, a instrumentação: <code>marca_de_vida</code>, em <code>src/instrumento.cpp</code>, anota <code>+nome</code> ao nascer e <code>-nome</code> ao morrer. É RAII aplicado ao próprio rastreamento, e é a segunda das três técnicas que ocupam o lugar do sanitizer ausente.',
                    ],
                },
            ],
        },
        {
            'id': 'construtores',
            'titulo': 'Tipos de Construtores',
            'origem': 'unidade-1/aula09-ciclo-de-vida',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Todo objeto em C++ passa por três fases: construção, uso e destruição. A habilidade que esta aula existe para formar é mais estreita e mais difícil que isso: <strong>determinar a ordem exata em que as três fases acontecem, para todos os objetos de um trecho, sem executar o trecho.</strong> Quem só sabe responder compilando confia na execução observada, e não no texto lido, e a prova desta disciplina é em papel justamente por essa razão.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Construtor',
                        'Quando roda',
                        'No Deriva',
                    ],
                    'linhas': [
                        [
                            'Padrão',
                            'objeto criado sem argumento; o compilador o gera se a classe não declarar outro construtor',
                            '<code>vetor2 p;</code> nasce na origem, e só porque <code>int x = 0;</code> está escrito na declaração do membro - sem esse inicializador, membro de tipo primitivo nasce com lixo',
                        ],
                        [
                            'Parametrizado',
                            'é o que estabelece a invariante da classe',
                            '<code>grade(int largura, int altura)</code>: valida as duas dimensões e dimensiona o vetor; a partir do retorno dele não existe grade de dimensão não-positiva no programa',
                        ],
                        [
                            'De cópia',
                            'objeto inicializado a partir de outro do mesmo tipo, com <code>mapa b{a}</code> ou <code>mapa b = a</code>',
                            'gerado pelo compilador em <code>grade</code>, e escrito à mão em <code>mapa</code> - porque lá ele tem de mexer no contador de instâncias vivas',
                        ],
                        [
                            'De conversão',
                            'construtor de um argumento que a linguagem chama sozinha, salvo se declarado <code>explicit</code>',
                            '<code>explicit entidade(vetor2)</code>, e o <code>explicit</code> de <code>fahrenheit</code> da Aula 05 é o mesmo mecanismo, visto pelo lado do sistema de tipos',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'Os três primeiros aparecem juntos no código extraído mais abaixo nesta página, em <code>src/instrumento.cpp</code>: <code>marca_de_vida</code> tem construtor parametrizado que move o nome recebido na lista de inicialização, destrutor de uma linha, e construtor de cópia que existe para marcar a cópia no traço. Vale ler o que o de cópia faz com o nome, porque é disso que a Aula 09 depende - ele monta <code>o.nome_ + "\'"</code>, e é essa aspa que distingue, no traço, a cópia que ninguém pediu de uma construção legítima.',
                },
            ],
        },
        {
            'id': 'lista-init',
            'titulo': 'Listas de Inicialização',
            'origem': 'unidade-1/aula09-ciclo-de-vida',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A lista de inicialização - o <code>: membro_(expr)</code> antes do corpo - inicializa os membros <strong>antes</strong> de a primeira linha do corpo executar. Isso evita construção padrão seguida de atribuição, e é obrigatório para membro <code>const</code>, para referência, e para classe sem construtor padrão. Escrever <code>nome_ = nome</code> no corpo construiria a <code>std::string</code> vazia primeiro e só depois lhe daria o valor, e o movimento se perderia numa cópia.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Há um motivo mais forte, e ele custou uma depuração no Deriva: <strong>validação de argumento que protege a construção de um membro tem de estar na lista, e não no corpo.</strong> A primeira versão do construtor de <code>grade</code> validava no corpo, e um teste pegou o erro - com <code>grade(5, -1)</code>, o <code>-1</code> virava <code>size_t</code> enorme na conta do tamanho, e o <code>std::vector</code> lançava <code>length_error</code> antes de o corpo rodar. A mensagem que o estudante veria era <code>cannot create std::vector larger than max_size()</code>, que não diz nada sobre a grade nem sobre a altura negativa que ele digitou. O trecho extraído mais abaixo é a função de validação que resolveu isso: ela é livre, está fora da classe, e devolve o valor validado, para poder ser chamada <em>dentro</em> da lista.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Armadilha da ordem de inicialização',
                    'paragrafos': [
                        'A lista de inicialização roda na ordem em que os membros foram <strong>declarados na classe</strong>, e não na ordem em que você escreve a lista. Escreva a lista na mesma ordem dos membros, e o <code>-Wall</code> avisa quando as duas divergem.',
                        'Em <code>grade</code>, <code>largura_</code> e <code>altura_</code> vêm declarados antes de <code>celulas_</code>, e é por isso que a validação chega a tempo. Inverter a declaração dos membros quebraria a validação sem mudar uma linha do construtor - e é o tipo de defeito que só aparece no caso de erro.',
                    ],
                },
            ],
        },
        {
            'id': 'raii',
            'titulo': 'RAII - Resource Acquisition Is Initialization',
            'origem': 'unidade-1/aula09-ciclo-de-vida',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'RAII é o idioma mais importante de C++ moderno, e a ideia cabe numa linha: ao adquirir um recurso - arquivo, mutex, conexão, memória, o modo do terminal -, inicialize-o no construtor, e libere-o no destrutor. Como o destrutor é chamado ao sair do escopo, inclusive no desenrolar por exceção, o recurso é sempre liberado.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Compare as duas formas de ler um arquivo. Na forma de C, um <code>std::fopen</code> no começo e um <code>std::fclose</code> no fim, e a liberação depende de o fluxo chegar até ela: qualquer <code>return</code> antecipado, qualquer exceção lançada no meio, e o descritor vaza. Na forma de C++, um <code>std::ifstream</code> declarado no escopo abre no construtor e fecha no destrutor, e não há linha de liberação para esquecer, porque não há linha de liberação nenhuma. A garantia que sustenta as duas frases anteriores é uma só, e ela tem teste próprio no Deriva, extraído mais abaixo: <strong>quando uma exceção é lançada, os destrutores dos objetos já construídos no caminho são chamados, de dentro para fora, enquanto a pilha é desenrolada.</strong> A exceção não pula os destrutores; ela os chama.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Use sempre os tipos RAII da biblioteca padrão onde eles existirem - <code>std::ifstream</code> para arquivo, <code>std::unique_ptr</code> para memória, <code>std::lock_guard</code> para mutex. O “sempre” tem um limite, e é onde esta aula termina: a biblioteca padrão cobre os recursos que ela conhece, e o modo do terminal não é um deles, nem o descritor do sistema, nem a trava de banco, nem a entrada em <code>/tmp</code>. Para esses, a forma é a mesma, e escrevê-la uma vez é o que faz entender por que a biblioteca a usa.',
                },
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'terminal_bruto: RAII com consequência física',
                    'paragrafos': [
                        'Um jogo de terminal por turnos precisa ler tecla sem esperar Enter e sem que a tecla apareça na tela, e isso se faz pondo o terminal em <strong>modo bruto</strong>, que é uma chamada de sistema que altera o estado do dispositivo. <code>terminal_bruto</code> faz a chamada no construtor, guarda o estado anterior, e o restaura no destrutor.',
                        'Se o destrutor não rodar, o estado fica alterado <strong>depois</strong> que o programa sai, porque ele é um recurso do sistema operacional e sobrevive ao processo: ninguém devolve nada quando o programa morre, e o conserto é digitar <code>reset</code> seguido de Enter, às cegas. É aqui que RAII deixa de ser doutrina. Vazar memória é abstrato, porque o sistema recolhe tudo no fim do processo; vazar o modo do terminal significa que a próxima coisa que você digitar não vai aparecer na tela.',
                        'A variante <code>variantes/v0.2-quebrada/</code> omite o destrutor de propósito, e o roteiro é este, na ordem: rodar com <code>&lt; /dev/null</code> primeiro, onde não há terminal de verdade e portanto não há o que estragar; ler o contador de instâncias vivas; e só então rodar num terminal que se possa perder. Ferramenta nenhuma acusa esse vazamento - o ASan não conhece <code>termios</code> -, e o contador é a única pista automática que existe.',
                        'Duas outras decisões da classe fecham a aula. A guarda de <code>isatty</code>: o construtor pergunta se a entrada padrão é um terminal antes de mexer em qualquer coisa, e em teste, em pipe ou em integração contínua o objeto se constrói, conta como vivo, e não altera nada - sem ela, o <code>ctest</code> deixaria o terminal de quem roda a suíte em estado imprevisível. E não é copiável nem movível: há exatamente um terminal, e posse de recurso único não se duplica; copiar produziria dois objetos cujos destrutores restaurariam o mesmo estado duas vezes.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'A pergunta que fecha esta aula',
                    'paragrafos': [
                        'Vale responder por escrito: <strong>onde mais, no código que você escreve, existe recurso que sobrevive ao processo?</strong> Arquivo aberto com bloqueio, socket, entrada em <code>/tmp</code>, linha travada em banco de dados, semáforo nomeado. Todos têm a mesma forma, e nenhum deles é recolhido pelo sistema operacional quando o seu programa termina de qualquer jeito.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-1/aula09-ciclo-de-vida',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Implemente em C++17 uma classe RAII que gerencia uma conexão a um banco de dados SQLite. Deve abrir no construtor, fechar no destrutor, e não permitir cópia (mas permitir movimento). Convenções: snake_case, noexcept onde aplicável."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        "LLMs frequentemente esquecem <code>noexcept</code> no destrutor e no construtor de movimento, e confundem 'delete por cópia' com 'não-copiável'. Sem <code>noexcept</code> no move, std::vector não usará movimento.",
                    ],
                },
            ],
        },
        {
            'id': 'intro',
            'titulo': 'RAII e Regra dos Zero/Três/Cinco',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'Onde RAII já está no Deriva, sem ninguém ter escrito',
                    'paragrafos': [
                        'Em <code>grade</code>, o membro que gerencia recurso é um <code>std::vector&lt;celula&gt;</code>, e ele é adquirido na lista de inicialização e liberado no destrutor que o compilador gera. Não há linha de alocação nem de liberação em todo o arquivo, e é isso que a regra do zero compra: a Aula 09 é sobre por que essa ausência é decisão.',
                        'Em <code>mapa</code>, o rastreamento é ele mesmo RAII: um membro <code>marca_de_vida</code> anota o nascimento no construtor e a morte no destrutor, e o registro do fim acontece porque o destrutor roda, e não porque alguém lembrou de chamar algo.',
                        'Em <code>terminal_bruto</code>, o recurso não é memória: é o estado de um dispositivo do sistema operacional. É o único dos três em que RAII foi escrito à mão, e é o único em que esquecê-lo tem consequência que o estudante sente.',
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
                        '<em>"Escreva em C++17 uma classe RAII que ponha o terminal em modo bruto no construtor, guardando o estado anterior, e o restaure no destrutor. Requisitos: guarda de <code>isatty</code> antes de alterar qualquer coisa; cópia e atribuição declaradas <code>= delete</code>, porque há um terminal só; <code>noexcept</code> onde couber; snake_case, comentários em português. Portão: compila com <code>-Wall -Wextra -Wpedantic -Wconversion</code> sem aviso, e o <code>ctest</code> não deixa o terminal de quem roda a suíte alterado."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'Ele quase sempre esquece a guarda de <code>isatty</code>, porque nada no pedido a torna necessária até o dia em que a suíte de testes roda. Também tende a declarar o movimento como se fosse óbvio - e movimento de recurso único exige decidir o que sobra no objeto de origem, decisão que a Aula 14 cobra por escrito.',
                        'E há o erro que interessa mais: pedir “RAII para um <code>FILE*</code>” devolve, quase sempre, código correto e desnecessário, porque <code>std::ifstream</code> já é isso. Confira sempre se existe tipo da biblioteca padrão que resolve, antes de aceitar uma classe nova.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Implemente o construtor de <code>grade</code> validando <strong>na lista de inicialização</strong>, com uma função livre que devolve o valor validado. Depois escreva a mesma classe validando <strong>no corpo</strong>, e chame <code>grade(5, -1)</code> nas duas versões. Transcreva as duas mensagens de erro e explique por que a segunda não menciona a grade.',
            'origem': 'unidade-1/aula09-ciclo-de-vida',
        },
        {
            'n': '02',
            'html': 'Acrescente uma <code>marca_de_vida</code> como membro da sua <code>grade</code> e escreva um <code>main</code> com dois objetos no escopo externo e um no interno. <strong>Antes de compilar</strong>, escreva no papel o traço que você espera, linha por linha. Depois rode, compare, e explique cada divergência. Este é o portão do LAB-05.',
            'origem': 'unidade-1/aula09-ciclo-de-vida',
        },
        {
            'n': '03',
            'html': 'Repita o exercício 2 lançando uma exceção de dentro do escopo interno, sem capturá-la ali. Preveja o traço antes de rodar: quantos destrutores rodam, em que ordem, e qual objeto ainda não havia sido construído quando a exceção passou?',
            'origem': 'unidade-1/aula09-ciclo-de-vida',
        },
        {
            'n': '04',
            'html': 'Por que <code>explicit</code> importa no construtor de um argumento? Demonstre o defeito que aparece sem ele: escreva uma classe com construtor de um <code>int</code> sem <code>explicit</code>, uma função que a receba por valor, e chame essa função passando um número. Depois acrescente <code>explicit</code> e leia o que o compilador passa a recusar.',
            'origem': 'unidade-1/aula09-ciclo-de-vida',
        },
        {
            'n': '01',
            'html': 'Escreva <code>terminal_bruto</code>: construtor que põe o terminal em modo bruto guardando o estado anterior, destrutor que restaura, guarda de <code>isatty</code>, e as operações de cópia declaradas <code>= delete</code>. Rode. Depois <strong>apague o destrutor</strong> e rode outra vez com <code>&lt; /dev/null</code>, lendo o contador de instâncias vivas. Só então, se quiser, rode num terminal que você possa perder - e conserte com <code>reset</code>.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
        {
            'n': '02',
            'html': 'Escreva uma classe <code>guarda_de_arquivo</code> que garanta, por RAII, que um <code>FILE*</code> seja fechado ao sair de escopo: o construtor abre e lança se falhar, o destrutor chama <code>fclose</code>. Demonstre com o traço do exercício 2 anterior que o arquivo é fechado mesmo quando uma exceção é lançada no meio. Depois responda: que tipo da biblioteca padrão tornaria esta classe desnecessária, e em que caso ele não serviria?',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
        {
            'n': '03',
            'html': 'Compare <code>variantes/v0.2-quebrada/</code> com a versão boa de <code>terminal_bruto</code>, e percorra o roteiro de observação na ordem do <code>LEIA-ME.md</code> da variante: sem ferramenta, com o contador, com o alocador, com o ASan, com o compilador. Escreva, para cada um dos cinco, o que ele acusou e o que ele deixou passar.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
        {
            'n': '04',
            'html': 'Explique com código o que acontece quando um objeto que tem um <code>std::vector</code> como membro é copiado: a cópia é rasa, compartilhando a memória, ou profunda, com memória nova? Como isso mudaria se o membro fosse um <code>celula*</code> cru? Guarde a resposta - ela é o assunto da Aula 09 e da primeira caça ao bug.',
            'origem': 'unidade-2/aula10-raii-rule-of-five',
        },
    ],
    'pendencias': [],
}
