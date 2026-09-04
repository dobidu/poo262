# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-3/aula27-qt-llms
Fatia: qt - fatia de Qt do Cap. 27; a fatia de LLM foi para a Aula 4
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Reescrito sobre o Deriva: o esqueleto Qt é `qt/janela.hpp`, `qt/janela.cpp` e
`qt/main_qt.cpp`, atrás de `-DDERIVA_COM_QT=ON` e desligado por padrão.
"""

AULA = {
    'n': 26,
    'slug': 'a26',
    'titulo': 'Qt e a separação domínio/apresentação',
    'curto': 'Qt sobre o mesmo núcleo',
    'unidade': 'III',
    'cap_v1': [
        27,
    ],
    'origem_v1': [
        'unidade-3/aula27-qt-llms',
    ],
    'fatia': [
        'qt',
        'fatia de Qt do Cap. 27; a fatia de LLM foi para a Aula 4',
    ],
    'deriva': 'v2.7',
    'lab': None,
    'interativos': [
        'refator',
    ],
    'nota_migracao': 'MIGRAÇÃO DE RISCO 2/3 (fecho). Demonstração do docente com esqueleto publicado - o plano v2 não exige entrega. Fica QObject, signals/slots e o argumento do segundo front-end sobre o mesmo núcleo.',
    'objetivos': [
        'Compreender o modelo de objetos do Qt: <code>QObject</code>, a árvore de pais, e signals e slots',
        'Reconhecer onde a posse no Qt contraria a regra da Aula 12, e por que a exceção é declarada',
        'Explicar por que o segundo front-end existe sem que o núcleo mude uma linha',
        'Fechar o semestre pelo critério: o que se aprendeu se verifica em código que compila',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Qt, signals e slots sobre o mesmo núcleo',
            'origem': 'unidade-3/aula27-qt-llms',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v2.7 - o segundo front-end',
                    'paragrafos': [
                        'O esqueleto está em <code>qt/janela.hpp</code>, <code>qt/janela.cpp</code> e <code>qt/main_qt.cpp</code>, e <strong>não entra no build padrão</strong>: ele exige <code>cmake -S . -B build -DDERIVA_COM_QT=ON</code> e Qt6 instalado. O laboratório não tem Qt, e por isso esta aula é demonstração do docente com esqueleto publicado, sem entrega obrigatória.',
                        'A <code>tela_qt</code> implementa <code>i_apresentacao</code>, a mesma interface que <code>apresentacao_em_texto</code> implementa, e o núcleo não sabe qual das duas está do outro lado. Fora dessa implementação, nenhuma linha de <code>src/</code> nem de <code>include/deriva/</code> muda para a janela existir.',
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'O argumento da aula não é Qt. É que a separação entre domínio e apresentação, afirmada ao longo do semestre e extraída na Aula 24, passa a ser <strong>demonstrável</strong>: há duas interfaces sobre o mesmo núcleo, no mesmo repositório, e a variante <code>v2.6-antes</code> continua ali para que se possa verificar que, antes da extração de <code>i_apresentacao</code>, isso era impossível - o <code>mundo</code> escrevia direto em <code>std::cout</code>.',
                },
            ],
        },
        {
            'id': 'qobject',
            'titulo': 'QObject, o MOC e a posse por árvore',
            'origem': 'unidade-3/aula27-qt-llms',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A macro <code>Q_OBJECT</code> na declaração da classe exige o MOC, um pré-processador que lê o cabeçalho e <strong>gera código</strong> a partir dele: é ele que dá a cada classe um nome consultável em tempo de execução e registra os slots. É por isso que <code>CMAKE_AUTOMOC</code> existe, e é o que faz esta classe precisar de um sistema de build que entenda Qt - compilar o <code>.cpp</code> à mão não basta.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Um slot é um método comum que o MOC registra para poder ser chamado por nome, sem que quem chama conheça o tipo de quem recebe: é a versão do Qt para o Observer da Aula 25. A ligação se faz com <code>connect</code>, e a forma que o esqueleto usa passa <strong>ponteiro de função membro</strong>, que o compilador verifica. A forma antiga, com as macros <code>SIGNAL</code> e <code>SLOT</code>, casava strings em tempo de execução, e um erro de digitação virava conexão que nunca acontece, sem um aviso.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Posse no Qt é a exceção declarada à regra da Aula 12',
                    'paragrafos': [
                        '<code>QObject</code> tem árvore de pais, e o pai destrói os filhos. Passar um <code>QWidget*</code> cru ao construtor do filho <strong>entrega a posse</strong> ao pai, de forma que <code>std::unique_ptr</code> sobre <code>QWidget</code> com pai é dupla liberação. A regra do semestre - posse declarada no tipo - vale, e esta é a exceção, que fica escrita no cabeçalho em vez de escondida.',
                        'As duas formas convivem na mesma função: <code>new QPlainTextEdit(this)</code> entrega o visor à árvore do Qt, e o <code>std::unique_ptr</code> guarda a <code>tela_qt</code>, que é nossa e não é <code>QObject</code>. Dentro da <code>tela_qt</code>, o ponteiro para o visor é cru, porque é observação e não posse - o mesmo critério de <code>mundo::primeira_com</code>.',
                    ],
                },
            ],
        },
        {
            'id': 'separacao',
            'titulo': 'Separação domínio e apresentação, e o ponto de composição',
            'origem': 'unidade-3/aula27-qt-llms',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Camada',
                        'Responsabilidade',
                        'Depende de',
                    ],
                    'linhas': [
                        [
                            'Domínio: <code>mundo</code>, <code>entidade</code>, <code>mapa</code>',
                            'Estado do setor, turno, regra de movimento',
                            'C++17 e a STL, e nada mais',
                        ],
                        [
                            'Apresentação: <code>i_apresentacao</code>',
                            'A interface que o núcleo conhece',
                            'Nada: é abstração pura',
                        ],
                        [
                            'Implementações: <code>apresentacao_em_texto</code>, <code>tela_qt</code>',
                            'Desenhar, cada uma no seu destino',
                            'A interface, e o Qt6 no caso da segunda',
                        ],
                        [
                            'Persistência: <code>partida</code>',
                            'Salvar e carregar, com a versão do formato',
                            'A STL, e o texto que o replay já compara',
                        ],
                        [
                            'Composição: <code>main.cpp</code> e <code>qt/main_qt.cpp</code>',
                            'Escolher as concretas e ligá-las',
                            'Todas as camadas, e é o único lugar que pode',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'A última linha é a que importa: existe <strong>um</strong> lugar autorizado a conhecer todas as camadas, e é o ponto de composição. <code>qt/main_qt.cpp</code> carrega o mapa, monta o <code>mundo</code>, acrescenta a sonda e entrega o mundo pronto para a janela; o mesmo <code>mundo</code> que o executável de terminal usa, montado do mesmo jeito.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O critério de aceitação da aula é verificável sem Qt instalado, e é isso que o torna útil: <code>testes/test_padroes.cpp</code> monta duas implementações de <code>i_apresentacao</code> no mesmo processo, sobre o mesmo <code>mundo</code>, e confere que desenhar cinco vezes não altera o estado do domínio - despejo byte a byte igual. Se desenhar mudasse estado, a segunda interface veria um sistema diferente da primeira, e a separação seria mentira.',
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Configure com <code>-DDERIVA_COM_QT=ON</code> e compile o esqueleto. Depois acrescente as ações de leste e oeste ao menu, ligando-as a <code>mover_sonda</code>, e confira que <code>src/</code> e <code>include/deriva/</code> não precisaram de uma linha. Se precisaram, o que a sua mudança violou?',
            'origem': 'unidade-3/aula27-qt-llms',
        },
        {
            'n': '02',
            'html': 'Escreva uma terceira implementação de <code>i_apresentacao</code> que grave o despejo em arquivo, e ligue-a ao mesmo <code>mundo</code> das outras duas. Quantos arquivos você teve de tocar, e quais? Compare com o que a variante <code>v2.6-antes</code> exigiria para a mesma tarefa.',
            'origem': 'unidade-3/aula27-qt-llms',
        },
        {
            'n': '03',
            'html': 'Troque, no esqueleto, o <code>new QPlainTextEdit(this)</code> por um <code>std::unique_ptr&lt;QPlainTextEdit&gt;</code> membro e observe o que acontece ao fechar a janela. Explique o defeito com o vocabulário da Aula 12, e diga por que <code>-Wall -Wextra -Wpedantic</code> não o pega.',
            'origem': 'unidade-3/aula27-qt-llms',
        },
        {
            'n': '04',
            'html': 'Escreva um relatório de uma página respondendo à pergunta do semestre: como você determina, <strong>a partir do texto</strong>, qual destrutor roda e em que ordem, no caminho em que a janela do Qt é fechada com o <code>historico</code> cheio de comandos? Cite os três instrumentos das Aulas 7, 8 e 11 e diga o que cada um mostraria.',
            'origem': 'unidade-3/aula27-qt-llms',
        },
    ],
    'pendencias': [],
}
