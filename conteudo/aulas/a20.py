# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-3/aula21-tratamento-erros
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Reescrito sobre o Deriva: o código desta aula é o que `build/extrair_codigo.py`
recorta de `include/deriva/erro.hpp`, `src/erro.cpp` e `src/mapa.cpp`.
"""

AULA = {
    'n': 20,
    'slug': 'a20',
    'titulo': 'Tratamento de erros',
    'curto': 'Tratamento de erros',
    'unidade': 'III',
    'cap_v1': [
        21,
    ],
    'origem_v1': [
        'unidade-3/aula21-tratamento-erros',
    ],
    'fatia': None,
    'deriva': 'v2.2',
    'lab': 'LAB-11',
    'interativos': [
        'ciclo',
    ],
    'nota_migracao': 'Entra std::filesystem no carregamento de mapa - hoje ausente. Garantias de exceção e desenrolar da pilha com destrutores ganham peso, por ligarem à Aula 8.',
    'objetivos': [
        'Escrever hierarquia de exceções semântica, e dizer por que a raiz dela deriva de <code>std::runtime_error</code>',
        'Usar <code>std::optional</code> para ausência de resultado',
        'Usar <code>std::variant</code> para falha esperada que carrega informação',
        'Decidir entre exceção, <code>optional</code> e <code>variant</code> a partir do que o chamador tem de decidir',
        'Reconhecer a garantia forte, e o que a torna barata',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Erros: exceção, optional e variant',
            'origem': 'unidade-3/aula21-tratamento-erros',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v2.2 - três formas de dizer que não deu certo',
                    'paragrafos': [
                        'O carregamento de mapa deixa de ser uma função só. Em <code>include/deriva/erro.hpp</code>, a mesma operação passa a ter três respostas possíveis, e a escolha entre elas está declarada no tipo: <code>std::optional</code> para ausência, <code>std::variant</code> para falha esperada com informação, e exceção para o que rompe a operação.',
                        'Entra também <code>std::filesystem</code>, que o material anterior não tinha em lugar nenhum: <code>std::filesystem::path</code> nas assinaturas, e <code>std::filesystem::exists</code> com <code>std::error_code</code> em vez da sobrecarga que lança.',
                    ],
                },
            ],
        },
        {
            'id': 'excecoes',
            'titulo': 'A hierarquia de exceções, e onde ela começa',
            'origem': 'unidade-3/aula21-tratamento-erros',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A raiz é <code>erro_de_deriva</code>, e ela deriva de <code>std::runtime_error</code> e não de <code>std::exception</code> direto. A razão é prática: <code>runtime_error</code> já guarda a mensagem e resolve o <code>what()</code>, e herdar de <code>std::exception</code> para reimplementar <code>what()</code> é trabalho sem retorno.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'Duas folhas descem dela, e a divisão é semântica e não de conveniência. <code>mapa_invalido</code> é erro de <strong>conteúdo</strong>: o arquivo existe e não é um mapa. <code>falha_de_leitura</code> é erro de <strong>acesso</strong>: permissão, disco, dispositivo. Cada uma monta a mensagem na base e guarda o dado estruturado ao lado, o <code>path</code> e o <code>std::error_code</code>, porque quem trata precisa do dado e não de uma string para reanalisar.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'A armadilha da exceção que guarda std::string',
                    'paragrafos': [
                        'A tentação é declarar um membro <code>std::string</code> na exceção para compor a mensagem. Se o construtor de cópia da exceção lançar durante o desenrolar da pilha, o programa termina, e ele pode lançar justamente porque copiar <code>std::string</code> aloca. É por isso que a mensagem vai para o construtor da base, que já a guarda por nós.',
                        'A ligação com a Aula 8 é direta: o desenrolar da pilha roda os destrutores dos objetos locais, e é isso que faz RAII e exceção serem o mesmo assunto. Objeto que possui recurso por membro se desfaz sozinho no caminho de erro, sem um <code>catch</code> escrito para isso.',
                    ],
                },
            ],
        },
        {
            'id': 'optional-variant',
            'titulo': 'optional, variant e o ponto em que a ausência vira erro',
            'origem': 'unidade-3/aula21-tratamento-erros',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': '<code>mapa::carregar</code> devolve <code>std::optional&lt;mapa&gt;</code> desde a v0.3, porque arquivo ausente é <strong>ausência de resultado</strong> e não erro: quem chamou perguntou se havia um mapa ali, e a resposta é que não havia. Já <code>interpretar</code> devolve <code>resultado_de_mapa</code>, que é <code>std::variant&lt;mapa, razao&gt;</code>, porque quando o texto existe e não serve o chamador precisa saber <em>por que</em> para decidir o que fazer.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O motivo vem como <code>enum class razao</code> e não como string, e a diferença aparece no chamador: comparar string é frágil, e um <code>switch</code> sobre o enumerado é o que faz o compilador avisar quando um caso novo aparece. A tradução para texto legível fica em uma função só, <code>descrever</code>, que devolve <code>std::string_view</code> para literal, sem alocar.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O par completa em <code>carregar_ou_lancar</code>, e é ali que a ausência deixa de ser <code>optional</code> e passa a ser exceção, para o <strong>mesmo</strong> arquivo ausente. A diferença não é capricho: esta função promete devolver um mapa, e aquela promete responder se há um. Quem promete devolver e não pode cumprir não tem o que retornar, e o desenrolar da pilha é a resposta certa.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'A garantia forte, e por que aqui ela é barata',
                    'paragrafos': [
                        'Garantia forte é a promessa de que, se a operação lançar, o sistema fica exatamente como estava. Em <code>interpretar</code> ela sai de graça, porque toda a validação acontece <strong>antes</strong> de qualquer construção: nada é alocado até se saber que o texto serve, de forma que não há o que desfazer.',
                        'É essa a razão de a leitura ser separada da aplicação. Uma função que fosse lendo e já mexendo no <code>mundo</code> precisaria guardar o estado anterior para poder voltar, e é aí que a garantia forte passa a custar - normalmente uma cópia inteira do objeto.',
                    ],
                },
            ],
        },
        {
            'id': 'quando-usar',
            'titulo': 'Qual das três, e a pergunta que decide',
            'origem': 'unidade-3/aula21-tratamento-erros',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Situação',
                        'Forma',
                        'Onde está no Deriva',
                    ],
                    'linhas': [
                        [
                            'Ausência de resultado, sem informação a dar',
                            '<code>std::optional&lt;T&gt;</code>',
                            '<code>mapa::carregar</code> e <code>partida::desserializar</code>',
                        ],
                        [
                            'Falha esperada, e o chamador decide a partir do motivo',
                            '<code>std::variant&lt;T, motivo&gt;</code>',
                            '<code>interpretar</code>, com <code>enum class razao</code>',
                        ],
                        [
                            'A operação não pode ser cumprida, e não há o que decidir',
                            'Exceção',
                            '<code>carregar_ou_lancar</code>, <code>mapa_invalido</code> e <code>falha_de_leitura</code>',
                        ],
                        [
                            'Erro do sistema de arquivos que se quer inspecionar',
                            '<code>std::error_code</code> por parâmetro de saída',
                            '<code>std::filesystem::exists</code> em <code>src/erro.cpp</code>',
                        ],
                        [
                            'Condição que tem de valer em compilação',
                            '<code>static_assert</code>',
                            '<code>celula.hpp</code>, <code>leiaute.hpp</code> e <code>grade_generica.hpp</code>',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'A pergunta que decide não é sobre custo: é sobre o que o chamador tem de fazer com a resposta. Se ele pode seguir sem o valor, <code>optional</code>; se precisa do motivo para escolher entre dois caminhos, <code>variant</code>; se não há caminho nenhum a escolher, exceção. O custo entra depois, e só onde a medição mostrar que entra.',
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-3/aula21-tratamento-erros',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Este é <code>interpretar</code>, que devolve <code>std::variant&lt;mapa, razao&gt;</code>. Reescreva-o para lançar exceção em vez de devolver o motivo, e depois liste o que o chamador ganha e o que perde na troca. C++17, sem <code>std::expected</code>."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o modelo costuma errar',
                    'paragrafos': [
                        'Três erros são frequentes: tratar <code>std::optional</code> como ponteiro que pode ser nulo, e desreferenciá-lo sem testar; escrever <code>std::visit</code> sem cobrir todas as alternativas do <code>variant</code>, o que não compila e o modelo insiste que compila; e engolir a exceção num <code>catch (...)</code> que devolve <code>nullopt</code>, o que apaga justamente a informação que o <code>variant</code> existia para carregar.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Acrescente uma sexta <code>razao</code> a <code>erro.hpp</code>, para mapa sem parede na borda, e implemente a checagem em <code>interpretar</code>. O que o compilador diz sobre o <code>switch</code> de <code>descrever</code> depois de você acrescentar o enumerado e antes de tratar o caso novo?',
            'origem': 'unidade-3/aula21-tratamento-erros',
        },
        {
            'n': '02',
            'html': 'Troque o <code>std::variant&lt;mapa, razao&gt;</code> de <code>interpretar</code> por <code>std::optional&lt;mapa&gt;</code> e rode <code>testes/test_erro.cpp</code>. Quais casos de teste deixam de ser escrevíveis, e por quê?',
            'origem': 'unidade-3/aula21-tratamento-erros',
        },
        {
            'n': '03',
            'html': 'Em <code>carregar_ou_lancar</code>, <code>std::filesystem::exists</code> e a abertura do arquivo são operações distintas, e entre uma e outra o arquivo pode desaparecer. Escreva o caso de teste que expõe essa corrida, e diga por que ela não é corrigível apenas trocando a ordem das duas chamadas.',
            'origem': 'unidade-3/aula21-tratamento-erros',
        },
        {
            'n': '04',
            'html': 'Instrumente <code>terminal_bruto</code> com a marca de ciclo de vida da Aula 8, force <code>carregar_ou_lancar</code> a lançar com o terminal em modo bruto, e mostre pelo traço que o destrutor rodou durante o desenrolar da pilha. Depois remova o destrutor, como faz a variante <code>v0.2-quebrada</code>, e descreva o que sobra no terminal depois de o programa sair.',
            'origem': 'unidade-3/aula21-tratamento-erros',
        },
    ],
    'pendencias': [],
}
