# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-3/aula23-concorrencia
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Reescrito sobre o Deriva: o código desta aula é o que `build/extrair_codigo.py`
recorta de `include/deriva/fila_de_comandos.hpp`, `src/fila_de_comandos.cpp` e
`include/deriva/medida_corrida.hpp`. O número da corrida NÃO entra em
`conteudo/medidas.py`, de propósito: é faixa, e não valor.
"""

AULA = {
    'n': 22,
    'slug': 'a22',
    'titulo': 'Concorrência em C++ - panorâmica',
    'curto': 'Panorâmica de concorrência',
    'unidade': 'III',
    'cap_v1': [
        23,
    ],
    'origem_v1': [
        'unidade-3/aula23-concorrencia',
    ],
    'fatia': None,
    'deriva': 'v2.4',
    'lab': None,
    'interativos': [
        'corrida',
    ],
    'nota_migracao': 'Ponte explícita com Programação Concorrente. O interativo de race condition vem de LPII com a legenda trocada - primeiro reaproveitamento entre as duas disciplinas.',
    'objetivos': [
        'Criar thread com <code>std::thread</code> e proteger a região crítica com <code>std::scoped_lock</code>',
        'Reconhecer corrida de dados, e dizer por que ela é pior quando não se manifesta',
        'Escrever espera com <code>std::condition_variable</code> e predicado',
        'Decidir o que se compartilha entre threads, e reduzir isso ao mínimo',
        'Conhecer <code>std::async</code> e <code>std::future</code>, e o que eles resolvem',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Concorrência: thread, mutex e a fronteira',
            'origem': 'unidade-3/aula23-concorrencia',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v2.4 - a fila é a única fronteira',
                    'paragrafos': [
                        'A thread que lê o teclado passa a ser separada da que desenha, e entre as duas há <code>fila_de_comandos</code>, em <code>include/deriva/fila_de_comandos.hpp</code>. <strong>O que se compartilha é a fila, e nada mais.</strong> O <code>mundo</code> continua sendo de uma thread só, e o que atravessa a fronteira são comandos, um por vez, protegidos.',
                        'A decisão é o oposto da tentação: seria mais fácil deixar as duas threads mexerem no <code>mundo</code>, e é exatamente isso que produz a corrida que o interativo desta página mostra.',
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'Esta aula é panorâmica, e a ponte com Programação Concorrente é explícita: aqui entra o suficiente para que a posse e o tempo de vida das Aulas 12 a 14 continuem verificáveis quando há mais de uma thread, e não o modelo de memória de C++ inteiro. Quem quiser <code>std::atomic</code>, ordenação de memória e algoritmo sem trava encontra isso na outra disciplina.',
                },
            ],
        },
        {
            'id': 'thread-mutex',
            'titulo': 'Thread, mutex e a corrida medida',
            'origem': 'unidade-3/aula23-concorrencia',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Corrida de dados é o que acontece quando duas threads acessam a mesma posição de memória, uma delas escreve, e nada ordena os dois acessos. O caso mínimo é o próprio <code>vivos++</code> do contador da Aula 7, que em <code>include/deriva/medida_corrida.hpp</code> aparece incrementado por duas threads sem proteção: são três passos - ler, somar, escrever -, e nenhum deles é atômico, de forma que dois incrementos podem ler o mesmo valor e escrever o mesmo resultado.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A trava usa <code>std::scoped_lock</code>, que é C++17 e substitui <code>std::lock_guard</code>: ele aceita mais de um mutex e resolve a ordem de travamento sozinho, o que elimina uma classe inteira de impasse. Para um mutex só os dois são equivalentes, e usar o novo é hábito. Nos dois casos vale a regra de RAII da Aula 8: a trava é objeto, o destrutor destrava, e nenhum caminho de saída - inclusive o de exceção - deixa o mutex travado.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'A corrida é comportamento indefinido, e o número dela é uma faixa',
                    'paragrafos': [
                        'Duas threads somando cem mil cada, dez execuções, g++ 13.3, nesta máquina: cinco rodadas da suíte deram quatro, nove, nove, oito e sete execuções <strong>sem perda nenhuma</strong>, de dez, e a pior perda chegou a 63.116 de 200.000. Não há média a citar, e não há valor a travar num portão que exija igualdade: o resultado varia a cada execução, porque comportamento indefinido é isso mesmo.',
                        'A distribuição é a lição, e não o número. Um defeito que não aparece na maioria das tentativas é pior que um que aparece sempre, porque o teste verde não prova nada - e é por isso que <code>testes/test_corrida.cpp</code> afirma apenas o que o padrão garante, que o lado protegido nunca perde e o desprotegido não perde mais do que somou. Rode <code>./build/testes "*corrida*"</code> para ver os seus próprios números.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'Sem detector automático, e isso é conteúdo',
                    'paragrafos': [
                        'As máquinas do laboratório não têm sanitizer nem Valgrind, e o alvo <code>make sanitizers</code> deste repositório liga <code>address</code> e <code>undefined</code>, que não detectam corrida de dados. O que substitui o detector é a medição repetida: rodar o caso muitas vezes, contar quantas execuções perderam, e comparar com o lado protegido, que não perde em nenhuma.',
                        'É o mesmo raciocínio das três técnicas sem dependência externa das Aulas 7, 8 e 11 - contador de instâncias vivas, instrumentação de ciclo de vida e <code>gdb</code> com ponto de parada em destrutor. Onde não há ferramenta, a verificação vira parte do projeto.',
                    ],
                },
            ],
        },
        {
            'id': 'async',
            'titulo': 'A espera com predicado, e o que std::async resolveria',
            'origem': 'unidade-3/aula23-concorrencia',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A consumidora não pode ficar consultando a fila em laço, porque isso queima processador para não fazer nada. Ela espera em <code>std::condition_variable</code>, e a espera leva <strong>predicado</strong>: sem ele, um despertar espúrio faria a thread seguir com a fila vazia. O predicado é reavaliado a cada despertar, e é o que torna a espera correta em vez de provável.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A condição de parada não é uma variável booleana lida sem proteção, que é o erro que esta aula mostra medido: ela é parte do estado guardado pelo mesmo mutex. E a notificação sai <strong>fora</strong> da região travada, porque quem acorda tentaria travar de imediato, e acordar antes de destravar custa uma ida e volta a mais no escalonador.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Duas threads, e a saída é determinística: <code>exercitar_fila</code> devolve os comandos na ordem em que foram consumidos, e a ordem se repete execução após execução, porque a fila é FIFO e há um consumidor só. Concorrência não implica indeterminismo, e é isso que preserva o replay da Aula 16. Com dois consumidores a ordem deixaria de ser garantida, e o portão byte a byte não serviria mais.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'std::async e std::future, e por que o Deriva não os usa',
                    'paragrafos': [
                        '<code>std::async</code> recebe um callable, escolhe onde executá-lo e devolve um <code>std::future&lt;T&gt;</code>, que é a promessa do resultado; <code>get()</code> bloqueia até o valor existir e o entrega uma vez só. Com <code>std::launch::async</code> a execução é obrigatoriamente em outra thread, e sem essa política a implementação pode adiá-la até o <code>get()</code>, o que já surpreendeu muita gente que contava com paralelismo.',
                        'O par serve a tarefa que <strong>começa, termina e devolve um valor</strong>, e é aí que ele é melhor do que thread crua: a exceção lançada dentro da tarefa é capturada e relançada no <code>get()</code>, em vez de terminar o programa. O Deriva não o usa porque a thread de entrada não termina nem devolve valor: ela vive o programa inteiro empurrando comandos, e o que essa forma pede é fila com espera, não promessa de resultado.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-3/aula23-concorrencia',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Escreva em C++17 uma fila entre uma thread produtora e uma consumidora, com <code>std::mutex</code>, <code>std::condition_variable</code> e fechamento explícito. Exijo: predicado no <code>wait</code>, notificação fora da região travada, e a condição de fechamento guardada pelo mesmo mutex. Não use variável booleana lida sem trava."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o modelo costuma errar',
                    'paragrafos': [
                        'O erro mais comum é a espera sem predicado, seguido do <code>join</code> esquecido, que termina o programa com thread ainda viva. Depois vem a condição de parada como <code>bool</code> lido sem trava, que o modelo defende como inofensiva porque "é só um bool" - e a corrida sobre ela é comportamento indefinido igual à do contador desta aula. Modelos também introduzem impasse ao travar dois mutexes em ordens diferentes em threads diferentes, e a correção é <code>std::scoped_lock</code> com os dois de uma vez.',
                        'Nenhum desses defeitos aparece com sanitizer no laboratório, porque não há sanitizer no laboratório. A revisão tem de ser por leitura, com a rubrica da Aula 4 na mão.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Rode <code>./build/testes "*corrida*"</code> dez vezes e anote quantas execuções perderam incremento em cada rodada. Sua distribuição é parecida com a que a página cita? Explique por que um <code>REQUIRE</code> exigindo que a corrida apareça reprovaria o portão em máquina rápida.',
            'origem': 'unidade-3/aula23-concorrencia',
        },
        {
            'n': '02',
            'html': 'Remova o predicado do <code>wait</code> em <code>fila_de_comandos::puxar</code>, mantendo o <code>notify_one</code>, e rode <code>testes/test_concorrencia.cpp</code> repetidamente. O teste falha? Explique por que a ausência de falha não prova que o código está correto.',
            'origem': 'unidade-3/aula23-concorrencia',
        },
        {
            'n': '03',
            'html': 'Acrescente um segundo consumidor a <code>exercitar_fila</code> e compare o despejo de duas execuções. Que garantia se perde, e qual das quatro condições de <code>make verifica</code> passa a falhar?',
            'origem': 'unidade-3/aula23-concorrencia',
        },
        {
            'n': '04',
            'html': 'Escreva um impasse deliberado com dois mutexes travados em ordens opostas em duas threads, observe o programa parar, e corrija com <code>std::scoped_lock</code> recebendo os dois. Em seguida explique por que <code>std::scoped_lock</code> resolve isso sem que ninguém escolha uma ordem.',
            'origem': 'unidade-3/aula23-concorrencia',
        },
    ],
    'pendencias': [],
}
