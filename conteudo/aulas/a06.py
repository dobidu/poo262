# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-1/aula07-uml-leve
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Pendências desta aula: 0 (ver conteudo/PENDENCIAS.md)
"""

AULA = {
    'n': 6,
    'slug': 'a06',
    'titulo': 'UML leve',
    'curto': 'UML que serve ao código',
    'unidade': 'I',
    'cap_v1': [
        7,
    ],
    'origem_v1': [
        'unidade-1/aula07-uml-leve',
    ],
    'fatia': None,
    'deriva': None,
    'lab': None,
    'interativos': [
        'uml',
        'revisor',
    ],
    'nota_migracao': 'Diagramas passam a ser do Deriva.',
    'objetivos': [
        'Ler e criar diagramas de classes UML',
        'Usar Mermaid para diagramas embutidos em Markdown',
        'Modelar relações: associação, composição, herança, realização',
        'Criar diagramas de sequência para fluxos importantes',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'UML Leve: Diagramas de Classes e Sequência',
            'origem': 'unidade-1/aula07-uml-leve',
            'compartilhado': False,
            'blocos': [],
        },
        {
            'id': 'classes',
            'titulo': 'Diagrama de Classes',
            'origem': 'unidade-1/aula07-uml-leve',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A classe é um retângulo de três compartimentos: o nome no topo, os atributos no meio, as operações no fundo. A visibilidade vem como prefixo de cada linha - <code>+</code> para <code>public</code>, <code>-</code> para <code>private</code>, <code>#</code> para <code>protected</code> -, e o tipo de retorno vem à direita, depois dos parênteses. É notação de leitura, e não de geração: nada aqui produz código, e o que ela tem de fazer é caber no quadro da sala.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O diagrama abaixo é o do Deriva na v0.3, que é o sistema que existe nesta aula. São quatro classes de domínio e nenhuma herança, e as duas coisas são decisões: a primeira relação de generalização chega na v1.0, com <code>entidade</code>. O que vale conferir nele é a ausência - <code>grade</code> não mostra nenhuma das operações especiais, porque segue a regra do zero, e a Aula 09 é sobre por que isso é decisão e não omissão.',
                },
                {
                    'tipo': 'mermaid',
                    'trecho': 'uml-mapa-tem-grade',
                },
                {
                    'tipo': 'callout',
                    't': 'deriva',
                    'titulo': 'As relações que o Deriva de fato tem',
                    'paragrafos': [
                        '<code>mapa</code> <strong>compõe</strong> uma <code>grade</code>, uma <code>vetor2</code> - o ponto de entrada - e uma <code>marca_de_vida</code>, todas por valor e todas 1 para 1. <code>grade</code> <strong>compõe</strong> as <code>celula</code> num <code>std::vector</code>, uma por posição.',
                        '<code>grade</code> <strong>depende de</strong> <code>vetor2</code>: recebe-o como parâmetro em <code>dentro()</code> e em <code>em()</code>, e não guarda nenhum. <code>mapa</code> depende de <code>std::filesystem::path</code>, que é o parâmetro de <code>carregar()</code>. E <code>marca_de_vida</code> depende de <code>instrumento</code>, onde ela anota o nascimento e a morte de quem a carrega.',
                        '<code>mapa</code> compõe <code>grade</code> porque um mapa <em>tem</em> uma grade: ele tem nome e ponto de entrada, que grade nenhuma tem, e não faz sentido passar um mapa onde se espera uma grade. Os dois trechos extraídos mais abaixo nesta página conferem isso contra o código, e é por isso que o desenho usa losango e não triângulo.',
                    ],
                },
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Notação',
                        'Significado',
                        'Em C++',
                    ],
                    'linhas': [
                        [
                            '△ ─ seta fechada vazia',
                            'Herança, ou generalização: “é um”',
                            '<code>class drone : public entidade</code>',
                        ],
                        [
                            '◆ ─ losango preenchido',
                            'Composição: a parte não existe sem o todo',
                            '<code>class mapa { grade grade_; };</code>',
                        ],
                        [
                            '◇ ─ losango vazio',
                            'Agregação: a parte pode existir sem o todo',
                            'coleção de ponteiros para <code>entidade</code> (Aula 12)',
                        ],
                        [
                            '△ ┄ moldura tracejada',
                            'Realização de interface pura',
                            '<code>class sonda_reparadora : public sonda, public i_reparavel</code>',
                        ],
                        [
                            '┄&gt; seta tracejada',
                            'Dependência, ou uso: métrica de acoplamento',
                            '<code>grade::em(vetor2)</code> recebe <code>vetor2</code> por parâmetro',
                        ],
                    ],
                },
            ],
        },
        {
            'id': 'sequencia',
            'titulo': 'Diagrama de Sequência',
            'origem': 'unidade-1/aula07-uml-leve',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'O diagrama de sequência mostra como os objetos interagem ao longo do tempo, lido de cima para baixo, com as mensagens trocadas horizontalmente entre as linhas de vida. No Deriva há uma coincidência útil: o traço de ciclo de vida da Aula 08 <em>é</em> um diagrama de sequência em texto - uma linha por mensagem, na ordem exata em que aconteceu -, e é essa ordem que os testes afirmam. Então existe um jeito de conferir o desenho: rodar <code>./build/deriva --replay roteiro.txt --traco</code> e comparar. Diagrama de sequência que discorda do traço está errado.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'O caso de uso que vale desenhar é o carregamento de um setor, e ele tem <strong>dois</strong> desfechos, porque a ausência de resultado é o assunto: <code>mapa::carregar</code> devolve <code>std::optional&lt;mapa&gt;</code>, e o <code>nullopt</code> é resposta, e não falha.',
                },
                {
                    'tipo': 'mermaid',
                    'trecho': 'uml-carregar-sequencia',
                },
            ],
        },
        {
            'id': 'mermaid',
            'titulo': 'Mermaid - Diagramas em Texto',
            'origem': 'unidade-1/aula07-uml-leve',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'Mermaid descreve o diagrama em texto, o que faz dele versionável: o desenho entra no repositório ao lado do código que ele descreve, e o <code>git diff</code> mostra o que mudou no desenho. Este é o diagrama de uma classe só, a <code>grade</code> de <code>include/deriva/grade.hpp</code>, e é o menor exemplo completo da notação.',
                },
                {
                    'tipo': 'mermaid',
                    'trecho': 'uml-grade-sozinha',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Desenhe antes de abrir o cabeçalho',
                    'paragrafos': [
                        'Faça o seu diagrama da <code>grade</code> antes de ler <code>grade.hpp</code>, e depois compare. Onde os dois divergirem, um dos dois está errado, e descobrir qual é o exercício 2 desta aula.',
                        'O GitHub renderiza Mermaid nativamente em arquivo <code>.md</code>, então o desenho pode morar no <code>LEIA-ME.md</code> do seu diretório. E há um cuidado que vale para todo diagrama: ele envelhece calado. Os dois trechos extraídos mais abaixo nesta página existem porque um diagrama envelhecido continuou afirmando que <code>sonda</code> era <code>final</code> depois de a v1.7 retirar a promessa.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-1/aula07-uml-leve',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Dado o código C++ abaixo, gere um diagrama de classes Mermaid que captura: classes, atributos (com tipos), métodos (com visibilidade +/-), e relações (herança, composição). Inclua multiplicidades."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        "LLMs frequentemente omitem multiplicidades ('1' vs '0..*'), confundem agregação com composição, e ignoram interfaces puras. Peça explicitamente cada elemento.",
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Desenhe em Mermaid o diagrama de classes de um sistema de biblioteca: livro (título, ISBN, ano), autor (nome, biografia), biblioteca (a coleção de livros), empréstimo (livro, usuário, data). Indique as relações corretas e diga, em cada caso, por que <strong>não</strong> é herança.',
            'origem': 'unidade-1/aula07-uml-leve',
        },
        {
            'n': '02',
            'html': 'Desenhe o diagrama de classes do Deriva v0.3 a partir dos cabeçalhos em <code>exemplos/deriva/include/deriva/</code>, sem olhar o desenho desta aula. Depois compare: você acertou as relações, e inventou alguma que o código não tem?',
            'origem': 'unidade-1/aula07-uml-leve',
        },
        {
            'n': '03',
            'html': 'Escreva o diagrama de sequência do empréstimo de livro do exercício 1: o usuário solicita, a biblioteca confere a disponibilidade, registra o empréstimo, devolve a confirmação. Inclua o desfecho em que o livro não está disponível, e diga que tipo de retorno em C++17 você usaria para representá-lo.',
            'origem': 'unidade-1/aula07-uml-leve',
        },
        {
            'n': '04',
            'html': 'A v1.7 do Deriva traz <code>sonda_reparadora</code>, que herda de <code>sonda</code> e de <code>i_reparavel</code>: é o diamante. Desenhe-o, marcando a interface pura com moldura tracejada, e diga por que esse diamante é inofensivo. Depois pare: <code>sonda</code> era <code>final</code> na v1.0. O que o seu desenho teria de mudar, e por que a promessa foi retirada?',
            'origem': 'unidade-1/aula07-uml-leve',
        },
    ],
    'pendencias': [],
}
