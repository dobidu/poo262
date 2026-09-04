# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-3/aula25-solid
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Reescrito sobre o Deriva: os cinco princípios saem de código que compila -
`variantes/v2.6-antes/mundo_god_class.cpp`, `src/mundo.cpp`,
`include/deriva/solid.hpp` e `include/deriva/apresentacao.hpp`.
"""

AULA = {
    'n': 24,
    'slug': 'a24',
    'titulo': 'SOLID e invariância de comportamento',
    'curto': 'SOLID e invariância',
    'unidade': 'III',
    'cap_v1': [
        25,
    ],
    'origem_v1': [
        'unidade-3/aula25-solid',
    ],
    'fatia': None,
    'deriva': 'v2.6',
    'lab': 'LAB-12',
    'interativos': [
        'refator',
    ],
    'nota_migracao': 'A refatoração do `mundo` como god class, verificada por replay. A lição é que refatoração correta é a que não muda a saída.',
    'objetivos': [
        'Nomear cada um dos cinco princípios e apontar, no código do Deriva, onde ele está honrado e onde está violado',
        'Reconhecer violação em código existente, inclusive em código gerado por modelo de linguagem',
        'Refatorar aplicando o princípio que a violação pede, e não o que estiver na moda',
        'Provar por replay que a refatoração não mudou a saída, e explicar por que teste verde não basta',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Princípios SOLID',
            'origem': 'unidade-3/aula25-solid',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v2.6 - o mundo como god class, e a caça ao bug 3',
                    'paragrafos': [
                        'A variante <code>variantes/v2.6-antes/mundo_god_class.cpp</code> guarda o <code>mundo</code> antes da refatoração, e nada nela está quebrado no sentido usual: ela compila sem um aviso, roda, e faz tudo o que a versão refatorada faz. O defeito é que a classe tem <strong>sete motivos independentes para mudar</strong> - estado do domínio, render direto em <code>std::cout</code>, entrada num <code>switch</code>, IA por <code>dynamic_cast</code>, log abrindo arquivo, persistência com o formato embutido, e uma terceira tabela de glifos para criar entidade.',
                        'A caça ao bug 3, na semana 13, não é achar o erro: é <strong>refatorar sob SOLID e provar que a saída não mudou</strong>. O oráculo é o replay, despejo idêntico byte a byte, e um <code>diff</code> vazio é a única evidência aceita - os testes que acompanham a variante passam nas duas versões, e é por isso que eles não servem de prova.',
                    ],
                },
            ],
        },
        {
            'id': 'overview',
            'titulo': 'Os cinco princípios, e onde cada um está no Deriva',
            'origem': 'unidade-3/aula25-solid',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Letra',
                        'Princípio',
                        'Em uma frase',
                        'Onde ler no código',
                    ],
                    'linhas': [
                        [
                            '<strong>S</strong>',
                            'Single Responsibility',
                            'Uma classe, um motivo para mudar',
                            '<code>variantes/v2.6-antes/mundo_god_class.cpp</code>, com sete',
                        ],
                        [
                            '<strong>O</strong>',
                            'Open/Closed',
                            'Aberta para extensão, fechada para modificação',
                            '<code>mundo::turno</code>, em <code>src/mundo.cpp</code>',
                        ],
                        [
                            '<strong>L</strong>',
                            'Liskov Substitution',
                            'A derivada honra a promessa da base',
                            '<code>parede_que_lanca</code>, em <code>include/deriva/solid.hpp</code>',
                        ],
                        [
                            '<strong>I</strong>',
                            'Interface Segregation',
                            'Interface pequena, e ninguém implementa o que não faz',
                            '<code>i_tudo</code> contra <code>i_desenhavel</code>, no mesmo arquivo',
                        ],
                        [
                            '<strong>D</strong>',
                            'Dependency Inversion',
                            'O alto nível depende da abstração',
                            '<code>i_apresentacao</code>, em <code>include/deriva/apresentacao.hpp</code>',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'Os dois princípios do meio moram num arquivo só, <code>include/deriva/solid.hpp</code>, e ele existe para ser violado de propósito: as classes de lá não entram no jogo, e sim na prova de que a violação compila.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Em Liskov, <code>parede</code> <em>é</em> um obstáculo, e obstáculo tem posição, de forma que herdar parece natural. O que <code>parede_que_lanca</code> quebra é a promessa da <strong>base</strong>: <code>mover</code> devolve onde o obstáculo ficou e nunca lança, e para quem não pode mover a resposta é a posição atual. O sintoma não aparece na parede - aparece em <code>empurrar_todos</code>, que recebe <code>obstaculo&amp;</code>, foi escrita antes de a parede existir, e estava correta quando foi escrita. É por isso que LSP se mede no <strong>chamador</strong>, e o pior está no fim: quando a exceção sobe, a caixa já foi movida, e a função deixou o sistema no meio do caminho sem ter feito nada de errado. A correção não é <code>try</code> e <code>catch</code>, é honrar a promessa, como faz <code>parede_honesta</code>.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Em Segregação de Interface, <code>i_tudo</code> pede <code>desenhar</code>, <code>salvar</code> e <code>reparar</code>, e quem só desenha é obrigado a mentir em dois métodos. <strong>Método vazio numa interface é a confissão de que ela pede demais</strong>, e a métrica aqui é contável: três métodos obrigados na forma gorda contra um na segregada, e as duas constantes do cabeçalho existem para que o teste conte isso em vez de a prosa afirmar.',
                },
            ],
        },
        {
            'id': 'srp',
            'titulo': 'SRP - uma classe, um motivo para mudar',
            'origem': 'unidade-3/aula25-solid',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Responsabilidade, aqui, não quer dizer "coisa que a classe faz": quer dizer <strong>motivo para editar o arquivo</strong>. Uma classe com sete motivos é editada por sete razões diferentes, por pessoas diferentes, em semanas diferentes, e cada edição arrisca o que as outras seis dependiam.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Responsabilidade no god class',
                        'O que ela impede',
                    ],
                    'linhas': [
                        [
                            'Render, direto em <code>std::cout</code>',
                            'Trocar por Qt sem editar esta classe; testar sem capturar a saída do processo',
                        ],
                        [
                            'Entrada, num <code>switch</code>',
                            'Desfazer, porque não há onde guardar o que foi feito',
                        ],
                        [
                            'IA, com <code>dynamic_cast</code> por tipo',
                            'Acrescentar comportamento sem tocar aqui',
                        ],
                        [
                            'Log, abrindo arquivo aqui dentro',
                            'Testar o log sem mexer no sistema de arquivos',
                        ],
                        [
                            'Persistência, com o formato embutido',
                            'Versionar o save sem risco para o resto',
                        ],
                        [
                            'Criação de entidade, terceira tabela de glifos',
                            'Acrescentar entidade sem editar três lugares',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'A sétima responsabilidade é o estado do domínio, e é a única que fica: é o que o <code>mundo</code> deveria ter sido desde o começo. As outras seis saem uma por vez, e a ordem que menos dói é log, render, criação, entrada, IA, persistência - com o <code>diff</code> rodando a cada passo, porque quem extrai três e só então compara não sabe qual das três mudou a saída.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Refatoração e melhoria não cabem na mesma passada',
                    'paragrafos': [
                        'Corrigir o alinhamento do render, acrescentar uma linha ao save, mudar a ordem das entidades no despejo: tudo isso é melhoria, e nenhuma delas cabe nesta refatoração. Misturar as duas é como se perde a capacidade de saber qual das duas quebrou o programa, porque o <code>diff</code> passa a acusar diferença esperada e diferença acidental com a mesma cara.',
                        'A ordem também é cobrada no laboratório: primeiro se estende o roteiro do replay, e só depois se refatora. O replay prova o que o roteiro exercita, e refatorar antes de escrever o caso é escrever o caso que passa.',
                    ],
                },
            ],
        },
        {
            'id': 'ocp',
            'titulo': 'OCP - a prova é negativa',
            'origem': 'unidade-3/aula25-solid',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Aberto para extensão e fechado para modificação é o princípio que mais se cita e menos se verifica, porque a verificação é <strong>negativa</strong>: não se prova que o desenho é aberto mostrando o que ele faz, e sim mostrando o que ele <em>não</em> exige que se mude.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'No Deriva a prova é curta. O <code>mundo</code> guarda <code>std::vector&lt;std::unique_ptr&lt;entidade&gt;&gt;</code> e o turno percorre esse vetor chamando <code>agir</code> pela base, de forma que acrescentar uma entidade nova - uma derivada de <code>entidade</code> com o seu próprio glifo e o seu próprio turno - não muda uma linha de <code>src/mundo.cpp</code>. A extensão acontece num arquivo novo, e o arquivo antigo fica fechado.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O contraste com o god class é direto: lá a IA é um <code>dynamic_cast</code> por tipo concreto, e cada comportamento novo obriga a acrescentar um ramo dentro da classe. O ramo compila, o teste passa, e o desenho apodrece uma linha por vez. É o mesmo padrão de decadência que a Aula 18 mostra no inspetor por RTTI: <code>dynamic_cast</code> em cadeia é quase sempre um <code>virtual</code> que não foi escrito.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Onde OCP se paga, e onde não',
                    'paragrafos': [
                        'A abertura custa: uma função virtual por ponto de extensão, uma indireção por chamada, e um contrato que passa a ser público. Vale onde a extensão de fato acontece, e a evidência é o próprio arquivo: <code>src/mundo.cpp</code> não menciona <code>sonda</code>, <code>drone</code> nem <code>item</code> em lugar nenhum, e é por isso que nenhuma entidade nova o obriga a mudar.',
                        'Onde a extensão não acontece, abrir é enfeite: o <code>vetor2</code> não tem função virtual nenhuma, e não vai ter, porque ninguém precisa de um vetor bidimensional alternativo.',
                    ],
                },
            ],
        },
        {
            'id': 'dip',
            'titulo': 'DIP - a interface de apresentação',
            'origem': 'unidade-3/aula25-solid',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Módulo de alto nível não deve depender de módulo de baixo nível: os dois dependem da abstração. No god class, o <code>mundo</code> escrevia direto em <code>std::cout</code>, e trocar a saída significava editar a classe que guarda o estado do jogo, o que é a definição de dependência invertida ao contrário.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A refatoração extrai <code>i_apresentacao</code>, com <code>desenhar</code> e <code>mensagem</code>, e é essa interface que o núcleo passa a conhecer. Duas implementações existem: <code>apresentacao_em_texto</code>, que acumula numa <code>std::string</code> e é o que os testes usam, e a <code>tela_qt</code> da v2.7, que é a mesma interface com um <code>QPlainTextEdit</code> do outro lado. O núcleo não sabe qual das duas está ali, e não tem como saber.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'É essa extração que torna a separação domínio e apresentação <strong>demonstrável</strong> em vez de afirmada, e a demonstração é a Aula 26: o segundo front-end existe sem que o núcleo mude uma linha, e a variante <code>v2.6-antes</code> continua no repositório para que se possa verificar que, antes dela, isso era impossível.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Testabilidade como métrica de DIP',
                    'paragrafos': [
                        'A pergunta que mede DIP não é sobre camada nem sobre diagrama: é se o teste consegue substituir a dependência. Se não dá para testar o log sem abrir arquivo, ou o render sem capturar a saída do processo, a dependência está no lugar errado - e no god class os dois casos aconteciam.',
                        'Com a interface no lugar, <code>registro_em_memoria</code> substitui o arquivo de log e <code>apresentacao_em_texto</code> substitui o terminal, sem caminho, sem permissão e sem limpeza depois. Os dois são curtos o bastante para caber numa tela, e são o que a versão anterior não conseguia ter.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'SOLID e LLMs',
            'origem': 'unidade-3/aula25-solid',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt de análise SOLID',
                    'paragrafos': [
                        '<em>"Analise <code>mundo_god_class.cpp</code> e identifique as violações dos cinco princípios SOLID. Para cada uma: nomeie o princípio, cite a linha, diga o que fica <strong>impossível</strong> por causa dela, e mostre a refatoração. Mantenha C++17 e <code>snake_case</code>, e não mude a saída do programa."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Onde o modelo erra com mais frequência',
                    'paragrafos': [
                        '<strong>LSP:</strong> confundem com <code>override</code> escrito corretamente, que é outra coisa - a violação de <code>parede_que_lanca</code> tem <code>override</code> e assinatura perfeitos. <strong>DIP:</strong> aceitam "usa abstração" sem verificar quem constrói a concreta, e a dependência costuma reaparecer no ponto de construção. <strong>ISP:</strong> propõem interface genérica demais, que pede menos por acidente e não por desenho.',
                        'E o erro mais caro é o que a caça ao bug 3 persegue: o modelo refatora e melhora na mesma resposta, o <code>diff</code> passa a acusar diferença, e ninguém sabe mais se a refatoração está correta. Peça as duas coisas em passadas separadas.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Abra <code>variantes/v2.6-antes/mundo_god_class.cpp</code> e identifique as sete responsabilidades sem consultar o <code>LEIA-ME.md</code> da variante. Depois compare com a tabela de lá: quais você agrupou como uma só, e o argumento de quem separou é melhor que o seu?',
            'origem': 'unidade-3/aula25-solid',
        },
        {
            'n': '02',
            'html': 'Extraia do god class a responsabilidade de log, aplicando DIP com <code>i_observador</code>, e rode o <code>diff</code> do replay antes e depois. Em seguida escreva o caso de teste que verifica o log com <code>registro_em_memoria</code>, sem tocar no sistema de arquivos.',
            'origem': 'unidade-3/aula25-solid',
        },
        {
            'n': '03',
            'html': 'Peça a um modelo de linguagem a análise SOLID de <code>mundo_god_class.cpp</code> e compare com o <code>LEIA-ME.md</code> da variante. Em que princípios ele acertou, em quais confundiu, e quantas das sete responsabilidades ele viu? Aplique a rubrica de revisão da Aula 4 à resposta dele.',
            'origem': 'unidade-3/aula25-solid',
        },
        {
            'n': '04',
            'html': 'Em <code>include/deriva/solid.hpp</code>, troque <code>parede_que_lanca</code> por <code>parede_honesta</code> em <code>empurrar_todos</code> e observe o que muda em <code>testes/test_solid.cpp</code>. Depois faça o exercício inverso: escreva uma terceira derivada que honre a assinatura e viole a promessa de outra maneira, sem lançar.',
            'origem': 'unidade-3/aula25-solid',
        },
    ],
    'pendencias': [],
}
