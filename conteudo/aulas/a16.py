# -*- coding: utf-8 -*-
"""Reescrito à mão sobre o Deriva - não rode build/extrair_v1.py aqui.

Origem no site v1: unidade-2/aula14-testes-catch2
Página inteira.
Este arquivo é a fonte de verdade do site v2 e do livro v2. O extrator do v1
sobrescreve o que está aqui; se precisar reextrair, faça em branch.
"""

AULA = {
    'n': 16,
    'slug': 'a16',
    'titulo': 'Testes com Catch2 e replay determinístico',
    'curto': 'Catch2 e replay determinístico',
    'unidade': 'II',
    'cap_v1': [
        14,
    ],
    'origem_v1': [
        'unidade-2/aula14-testes-catch2',
    ],
    'fatia': None,
    'deriva': 'v1.6',
    'lab': 'LAB-09',
    'interativos': [
        'refator',
    ],
    'nota_migracao': 'O teste como especificação executável. Entra o replay: semente fixa, roteiro gravado, despejo idêntico byte a byte. É o oráculo das Aulas 24 e 25. Os trechos saem de `CMakeLists.txt`, do `Makefile`, de `src/fov.cpp`, de `src/main.cpp` e das suítes de `grade`, `mapa` e campo de visão.',
    'objetivos': [
        'Estruturar testes com <code>TEST_CASE</code> e <code>SECTION</code>, e dizer o que cada seção reexecuta',
        'Escolher entre <code>REQUIRE</code>, <code>CHECK</code> e <code>REQUIRE_THROWS_AS</code> pelo que cada um faz depois da falha',
        'Escrever teste que falha quando o comportamento muda, e não quando a implementação muda',
        'Usar o replay determinístico como portão de refatoração',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Testes automatizados com Catch2 v3',
            'origem': 'unidade-2/aula14-testes-catch2',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v1.6 · o campo de visão testado, e o replay',
                    'paragrafos': [
                        'A v1.6 escreve as suítes de campo de visão e de caminho, e liga o replay determinístico. O portão do Deriva passa a ter quatro condições, e duas delas são desta aula: <code>ctest</code> com 188 testes verdes, e o despejo idêntico byte a byte com semente fixa.',
                        'Rodar é <code>ctest --test-dir build --output-on-failure</code>, ou <code>make verifica</code> para as quatro condições de uma vez.',
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'O campo de visão é o primeiro alvo dos testes, e não o último, porque é função pura: mesma entrada, mesmo conjunto de células visíveis, sem montar o mundo e sem tocar no terminal. A implementação é Bresenham em inteiros, sem um ponto flutuante e sem arredondamento que dependa de plataforma, e é essa propriedade que o replay compra.',
                },
            ],
        },
        {
            'id': 'estrutura',
            'titulo': 'TEST_CASE, SECTION e o que cada seção reexecuta',
            'origem': 'unidade-2/aula14-testes-catch2',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Um <code>TEST_CASE</code> tem nome em prosa e etiquetas, e o nome é o que aparece na falha, de forma que ele deve dizer o que a classe promete e não qual método foi chamado. Lido de cima a baixo, o arquivo de teste de <code>grade</code> é a documentação de <code>grade</code>, com a diferença de ser executável.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O detalhe de <code>SECTION</code> que a prova cobra: o corpo do <code>TEST_CASE</code> roda uma vez <strong>por seção folha</strong>, e não uma vez para todas. O que está escrito antes das seções é arranjo, e cada ramo entra num objeto recém-montado. É isso que torna as seções independentes, e é exatamente a propriedade que se perde quando alguém guarda estado entre elas para não repetir a montagem.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Etiquetas filtram, e o filtro é ferramenta de depuração',
                    'paragrafos': [
                        '<code>ctest -R mapa</code> roda só os testes cujo nome registrado casa com <code>mapa</code>, e <code>./build/testes "*copiar*"</code> filtra pelo nome do caso dentro do binário do Catch2. É assim que se lê um número medido sem rodar a suíte inteira, e é o que o material faz para exibir o vazamento do ciclo da Aula 13.',
                    ],
                },
            ],
        },
        {
            'id': 'tipos-assert',
            'titulo': 'As asserções, e o que cada uma faz depois de falhar',
            'origem': 'unidade-2/aula14-testes-catch2',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A escolha entre as macros é sobre o que acontece <em>depois</em> da falha. <code>REQUIRE</code> interrompe o caso, e serve para pré-condição: se a montagem falhou, o resto do teste não tem sentido e as falhas seguintes só produziriam ruído. <code>CHECK</code> continua, e serve para verificações independentes, quando você quer o relatório completo numa única execução.',
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Macro',
                        'O que faz na falha',
                        'Quando usar',
                    ],
                    'linhas': [
                        [
                            '<code>REQUIRE(expr)</code>',
                            'interrompe o <code>TEST_CASE</code>',
                            'pré-condição, estado de que o resto depende',
                        ],
                        [
                            '<code>CHECK(expr)</code>',
                            'registra e continua',
                            'verificações independentes entre si',
                        ],
                        [
                            '<code>REQUIRE_FALSE(expr)</code>',
                            'interrompe',
                            'a negação, sem o <code>!</code> que se perde na leitura',
                        ],
                        [
                            '<code>REQUIRE_THROWS_AS(expr, tipo)</code>',
                            'interrompe',
                            'erro de programação, com o tipo exato exigido',
                        ],
                        [
                            '<code>REQUIRE_NOTHROW(expr)</code>',
                            'interrompe',
                            'operação que a classe promete não lançar',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'info',
                    'titulo': 'Por que Catch::Approx não aparece na suíte do Deriva',
                    'paragrafos': [
                        'Comparar ponto flutuante com <code>==</code> compara a representação, e não o valor pretendido, e é para isso que existe <code>Catch::Approx</code>. No Deriva ele não aparece uma vez, porque o domínio é inteiro: a grade tem coordenadas inteiras, o raio é distância de Manhattan e o campo de visão é Bresenham em inteiros. A ausência é decisão de projeto, e é ela que torna o despejo comparável byte a byte em qualquer máquina.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Teste que afirma implementação não é teste',
                    'paragrafos': [
                        'O teste tem de falhar quando o <strong>comportamento</strong> muda, e não quando a implementação muda. Um teste que afirma o número de chamadas internas, ou o valor de um membro privado alcançado por artifício, trava a refatoração em vez de a proteger, e é o item R7 da rubrica. O critério prático: se você reescrever o corpo do método mantendo a promessa, o teste tem de continuar verde.',
                    ],
                },
            ],
        },
        {
            'id': 'replay',
            'titulo': 'O replay determinístico como portão de refatoração',
            'origem': 'unidade-2/aula14-testes-catch2',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Teste de unidade afirma promessa por promessa. O replay afirma a saída inteira: semente fixa, roteiro de teclas gravado em arquivo, despejo comparado com <code>diff</code> contra o esperado. É a condição 3 das quatro do portão, e o que ela protege não é uma função, é o comportamento observável do programa completo.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Para que isso funcione, o sorteio do Deriva não é <code>std::mt19937</code> nem <code>std::random_device</code>: é um gerador escrito para ser reproduzível byte a byte em qualquer máquina. Aleatoriedade de verdade seria pior aqui, porque tornaria o oráculo inútil.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Regravar o esperado é uma decisão, e tem de ser tomada em voz alta',
                    'paragrafos': [
                        'Existe um alvo que regrava o arquivo esperado, e usá-lo é declarar que a saída <em>deveria</em> mudar. Numa refatoração é justamente o que não se pode fazer: refatoração correta é a que não muda a saída, e é assim que a Aula 24 verifica a sua. Se o <code>diff</code> aparecer durante uma refatoração, o defeito está no código novo, e não no esperado.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'A dependência de teste entra como SYSTEM, e com versão fixa',
                    'paragrafos': [
                        'O Catch2 chega por <code>FetchContent</code> marcado <code>SYSTEM</code>, para que aviso vindo do cabeçalho da dependência não conte na condição de zero warning, que existe para incidir sobre o seu código. E a etiqueta de versão é fixa, para que a suíte não mude de comportamento sem que ninguém tenha mexido nela.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-2/aula14-testes-catch2',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Em C++17 com Catch2 v3: escreva a suíte de uma função pura <code>visiveis(mapa, posicao, raio)</code> que devolve o conjunto de células vistas. Cubra a origem, a borda exata do raio, a parede que é vista e bloqueia o que está atrás, e a posição fora do mapa. Use <code>SECTION</code> para os ramos que partilham o mesmo arranjo, e não afirme nada sobre a ordem interna do conjunto."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'O erro central é gerar teste que afirma a implementação: contagem de chamadas, ordem interna de um contêiner não ordenado, valor de campo privado. Depois vêm os esquecimentos: o caso de fronteira exata, o tipo errado em <code>REQUIRE_THROWS_AS</code>, e o estado do objeto de origem depois de um movimento, que a Aula 14 mostra que não se afirma. Peça sempre o caso que <em>falharia</em> se a promessa fosse quebrada.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Escreva a suíte de <code>mapa::carregar</code> a partir de arquivo: arquivo existente, arquivo inexistente e arquivo com linha de largura diferente das outras. Os três casos de ausência devolvem <code>optional</code> vazio, e nenhum deles é exceção. Depois diga por que os testes do Deriva preferem <code>de_texto</code> a <code>carregar</code>.',
            'origem': 'unidade-2/aula14-testes-catch2',
        },
        {
            'n': '02',
            'html': 'Aplique TDD a uma função nova de <code>mapa</code>, que devolva as células de parede adjacentes a uma posição. Escreva primeiro os testes, incluindo o caso de canto, e só então a implementação. Registre quantas vezes o teste falhou por motivo que você não havia previsto.',
            'origem': 'unidade-2/aula14-testes-catch2',
        },
        {
            'n': '03',
            'html': 'Pegue um teste da suíte que afirme implementação em vez de comportamento, ou escreva um. Refatore o método correspondente sem mudar a promessa, e mostre o teste ficando vermelho sem que nada tenha se quebrado. Depois reescreva o teste para que ele volte a proteger, e não a travar.',
            'origem': 'unidade-2/aula14-testes-catch2',
        },
        {
            'n': '04',
            'html': 'Mude uma linha do render que altere a saída em um único caractere, e rode o replay. O <code>diff</code> aponta o quê, e em que linha? Depois desfaça, e explique por que o replay pega o que a suíte de unidade não pegaria.',
            'origem': 'unidade-2/aula14-testes-catch2',
        },
    ],
    'pendencias': [],
}
