# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-3/aula24-serializacao
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Reescrito sobre o Deriva: o código desta aula é o que `build/extrair_codigo.py`
recorta de `src/partida.cpp` e `testes/test_partida.cpp`.
"""

AULA = {
    'n': 23,
    'slug': 'a23',
    'titulo': 'Serialização',
    'curto': 'Serialização e versionamento',
    'unidade': 'III',
    'cap_v1': [
        24,
    ],
    'origem_v1': [
        'unidade-3/aula24-serializacao',
    ],
    'fatia': None,
    'deriva': 'v2.5',
    'lab': None,
    'interativos': [
        'revisor',
    ],
    'nota_migracao': 'Salvar e carregar partida do Deriva; versionamento de formato.',
    'objetivos': [
        'Escolher o formato de serialização a partir da estrutura do dado, e justificar a escolha',
        'Versionar o formato de forma que um leitor novo abra arquivo antigo',
        'Distinguir mudança que exige subir a versão da que não exige',
        'Tratar campo ausente e chave desconhecida sem recusar o arquivo',
        'Reconhecer a <em>most vexing parse</em> quando o compilador reclama de algo que parece certo',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Serialização, formato e versionamento',
            'origem': 'unidade-3/aula24-serializacao',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'v2.5 - salvar e carregar a partida',
                    'paragrafos': [
                        'A <code>struct partida</code>, em <code>include/deriva/partida.hpp</code>, guarda o estado da sessão: o setor, a posição da sonda, a carga, o turno e a energia. <code>serializar</code> escreve, <code>desserializar</code> lê, e <code>partida::de</code> extrai o estado de um <code>mundo</code> em execução.',
                        'A versão do formato é <strong>a primeira linha do arquivo</strong>, e o valor corrente está em <code>partida::kVersaoAtual</code>. O leitor entende duas versões, e <code>versoes_aceitas</code> existe para que o teste de compatibilidade regressiva possa afirmar isso.',
                    ],
                },
            ],
        },
        {
            'id': 'nlohmann',
            'titulo': 'O formato, e por que aqui não é JSON',
            'origem': 'unidade-3/aula24-serializacao',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Serializar é responder duas perguntas antes de escrever a primeira linha: que dados definem o estado, e que formato o representa sem perder informação nem ganhar ambiguidade. A segunda depende da forma do dado, e não do gosto de quem escreve.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O formato da <code>partida</code> é texto de linhas <code>chave valor</code>, e a escolha tem três razões concretas: o despejo do replay já é texto, o <code>diff</code> da condição 3 do portão já compara texto, e um formato binário obrigaria a escrever uma ferramenta de inspeção só para poder depurar o salvamento. Nada aqui aninha: a <code>partida</code> é plana, com quatro inteiros, um nome de setor e um par de coordenadas.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'JSON entraria se houvesse estrutura aninhada de verdade, e a biblioteca de referência para isso em C++ é a <code>nlohmann/json</code>, que se instala como dependência do CMake do mesmo jeito que o Catch2 da Aula 2 e resolve a serialização de tipo próprio por sobrecarga não intrusiva de <code>to_json</code> e <code>from_json</code>. O critério para trazê-la é ter aninhamento, lista heterogênea, ou um consumidor fora do programa que já fale JSON. Trazer uma dependência para gravar meia dúzia de campos planos é custo sem contrapartida.',
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Serializar hierarquia polimórfica é outro problema',
                    'paragrafos': [
                        'A <code>partida</code> não salva as entidades, e é bom saber por que: gravar um <code>std::vector&lt;std::unique_ptr&lt;entidade&gt;&gt;</code> exige gravar o <strong>tipo concreto</strong> de cada elemento, porque a leitura precisa saber qual construtor chamar. Sem esse campo, a desserialização não tem como recriar a derivada, e o que volta é a base fatiada.',
                        'A solução é a fábrica por glifo da Aula 25: o glifo <em>é</em> o discriminador de tipo, já está no mapa, e <code>criar_por_glifo</code> é o único lugar que traduz glifo em classe concreta. Serialização polimórfica bem feita quase sempre acaba nesse desenho.',
                    ],
                },
            ],
        },
        {
            'id': 'versionamento',
            'titulo': 'Versionamento de formato, e compatibilidade regressiva',
            'origem': 'unidade-3/aula24-serializacao',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A versão vem primeiro porque quem lê precisa saber <strong>com que regras ler</strong> antes de ler qualquer outra coisa. Versão no meio do arquivo obriga a duas passadas, ou a adivinhar; versão no fim é pior ainda, porque o leitor já terá interpretado tudo errado quando chegar nela.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A regra do que sobe a versão é a que separa formato extensível de formato frágil: acrescentar campo <strong>opcional</strong> no fim não sobe, e mudar o significado de campo existente sobe. O campo <code>energia</code> foi o que a versão 2 acrescentou, e um arquivo da versão 1 não o tem - a compatibilidade regressiva é justamente o leitor novo aceitar isso.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O mecanismo que responde pelo campo ausente é o <strong>valor padrão do membro</strong>, declarado na <code>struct</code>. Sem ele, a partida antiga carregaria com zero de energia e a sonda apareceria morta, que é o defeito clássico de migração de formato, e <code>testes/test_partida.cpp</code> o cobre lendo um arquivo da versão 1 e conferindo o valor que sobrou. A chave desconhecida, por sua vez, é <strong>pulada</strong> em vez de recusada, e é isso que permite a um leitor da versão 2 abrir um arquivo da versão 3 que só acrescentou campos.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Versione desde o primeiro commit',
                    'paragrafos': [
                        'Acrescentar versão depois é trabalhoso e quebra os arquivos que já existem, porque eles não a têm e o leitor novo não sabe distinguir arquivo sem versão de arquivo corrompido. Uma linha no primeiro commit evita um caminho de migração inteiro.',
                        'Repare que <code>desserializar</code> devolve <code>std::optional&lt;partida&gt;</code> e não lança: arquivo de save corrompido é caso esperado, e a escolha segue a mesma regra da Aula 20 - quem chamou pode seguir sem o valor, oferecendo começar uma partida nova.',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'A most vexing parse, e o custo dela',
                    'paragrafos': [
                        'Em <code>desserializar</code> o fluxo de leitura é construído com chaves e não com parênteses, e a razão é uma ambiguidade da gramática: com parênteses, o compilador lê a <strong>declaração de uma função</strong> que devolve um <code>istringstream</code> e recebe um <code>std::string</code>, e depois reclama que não há <code>operator&gt;&gt;</code> para função - mensagem que não ajuda ninguém a descobrir que o problema é a sintaxe da declaração.',
                        'A inicialização uniforme com chaves, que a Aula 3 recomenda desde o começo, não tem essa ambiguidade. É o exemplo mais curto de por que a recomendação existe.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste tópico',
            'origem': 'unidade-3/aula24-serializacao',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Este é o formato de save da <code>partida</code>, texto de linhas <code>chave valor</code> com a versão na primeira linha. Quero acrescentar a lista de entidades, cada uma com glifo e posição. Proponha a mudança de formato, diga se ela sobe a versão e por quê, e escreva o caso de teste que prova que o leitor novo ainda abre um arquivo da versão 2."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o modelo costuma errar',
                    'paragrafos': [
                        'Ao serializar hierarquia, modelos esquecem de gravar o tipo concreto, e a desserialização volta a base fatiada sem que nada acuse - é o defeito que a rubrica da Aula 4 pega no item de posse e tipo. O segundo erro é recusar o arquivo inteiro quando encontra chave desconhecida, o que transforma toda extensão futura em quebra. O terceiro é subir a versão a cada mudança, inclusive nas que não precisam, e o custo disso é um caminho de leitura por versão que ninguém mantém.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Salve uma partida, edite o arquivo à mão trocando <code>energia</code> por uma chave que o leitor não conhece, e carregue de novo. O que acontece, e qual linha de <code>desserializar</code> decide isso? Depois remova a linha da energia e diga de onde vem o valor que aparece.',
            'origem': 'unidade-3/aula24-serializacao',
        },
        {
            'n': '02',
            'html': 'Acrescente à <code>partida</code> um campo <code>setores_visitados</code>, com valor padrão de membro. Sua mudança sobe a versão? Justifique com a regra do cabeçalho, e escreva o caso de teste que abre um arquivo da versão 2 depois da mudança.',
            'origem': 'unidade-3/aula24-serializacao',
        },
        {
            'n': '03',
            'html': 'Implemente <code>partida::aplicar_em(mundo&amp;)</code>, o caminho inverso de <code>partida::de</code>, e prove por replay que salvar, carregar e aplicar devolve o mesmo despejo byte a byte. Por que o <code>diff</code> vazio é evidência mais forte que um teste verde aqui?',
            'origem': 'unidade-3/aula24-serializacao',
        },
        {
            'n': '04',
            'html': 'Troque as chaves por parênteses na construção do fluxo em <code>desserializar</code>, compile, e transcreva a mensagem de erro inteira. Quantas linhas de mensagem separam o erro relatado da causa real?',
            'origem': 'unidade-3/aula24-serializacao',
        },
    ],
    'pendencias': [],
}
