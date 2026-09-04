# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-1/aula05-git-github, unidade-1/aula06-llms-copiloto, unidade-3/aula27-qt-llms
Fatia: llm - a fatia de LLM do Cap. 27; a fatia de Qt vai para a Aula 26
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Pendências desta aula: 0 (ver conteudo/PENDENCIAS.md)
"""

AULA = {
    'n': 4,
    'slug': 'a04',
    'titulo': 'Git, LLM como copiloto e a rubrica de revisão',
    'curto': 'Git, LLM e a rubrica',
    'unidade': 'I',
    'cap_v1': [
        5,
        6,
        27,
    ],
    'origem_v1': [
        'unidade-1/aula05-git-github',
        'unidade-1/aula06-llms-copiloto',
        'unidade-3/aula27-qt-llms',
    ],
    'fatia': [
        'llm',
        'a fatia de LLM do Cap. 27; a fatia de Qt vai para a Aula 26',
    ],
    'deriva': None,
    'lab': 'LAB-03',
    'interativos': [
        'revisor',
    ],
    'nota_migracao': 'MIGRAÇÃO DE RISCO 2/3 - fusão de três origens. A rubrica de revisão de código OO gerado por IA sai do fim do livro e vem para cá, porque passa a ser instrumento das três caças ao bug: um instrumento tem de chegar antes do uso.',
    'objetivos': [
        'Usar Git para versionar código C++ (branches, commits, .gitignore)',
        'Colaborar via pull requests no GitHub',
        'Configurar GitHub Actions para build automático',
        'Usar o repositório do Deriva como registro das decisões de projeto do semestre',
        'Usar LLMs de forma produtiva para modelagem, refatoração e testes',
        'Reconhecer os padrões de erro mais comuns em código C++ gerado por LLM',
        'Escrever prompts eficazes para C++17 OO',
        'Aplicar, item por item, a rubrica de revisão de código OO gerado por IA',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Git e GitHub como Ambiente de Trabalho',
            'origem': 'unidade-1/aula05-git-github',
            'compartilhado': False,
            'blocos': [],
        },
        {
            'id': 'basico',
            'titulo': 'Fluxo de Trabalho Básico',
            'origem': 'unidade-1/aula05-git-github',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'codigo',
                    'lang': 'bash',
                    'legenda': 'Comandos fundamentais do dia a dia',
                    'codigo': """\
# Clonar o repositório da disciplina. O endereço é publicado no ambiente
# da turma a cada semestre, e não fica escrito aqui de propósito: material
# com URL fixa envelhece calado.
git clone <endereco-do-repositorio> && cd <nome-do-repositorio>

# Ver estado do repositório
git status        # o que mudou?
git diff          # o que exatamente mudou?
git log --oneline # histórico compacto

# Criar branch para isolar o que ainda pode não dar certo
git switch -c feat/contador-de-instancias

# Adicionar e commitar
git add include/deriva/contador.hpp src/mapa.cpp
git commit -m "feat: contador vivos e criados em mapa"

# Enviar para o remoto
git push origin feat/contador-de-instancias""",
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Commits atômicos e descritivos',
                    'paragrafos': [
                        'Cada commit deve fazer uma coisa só. Mensagem no formato <code>tipo(escopo): descrição</code>. Tipos: feat, fix, docs, test, refactor, chore.',
                    ],
                },
            ],
        },
        {
            'id': 'gitignore',
            'titulo': '.gitignore para projetos C++',
            'origem': 'unidade-1/aula05-git-github',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'codigo',
                    'lang': 'bash',
                    'legenda': '.gitignore do Deriva',
                    'codigo': """\
# Diretório de build, e as variações que as IDEs criam
build/
build-asan/
cmake-build-*/
CMakeFiles/
*.o  *.a  *.so  *.out

# O que o FetchContent baixa: FTXUI e Catch2 vêm por tag fixa
_deps/

# IDE e sistema operacional
.vscode/
.idea/
*.swp
.DS_Store""",
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'Nunca versione arquivos compilados',
                    'paragrafos': [
                        'Binário muda a cada compilação, produz conflito que ninguém resolve, e incha o repositório. As duas primeiras linhas resolvem quase tudo, porque o <code>FetchContent</code> clona a FTXUI e o Catch2 para dentro do próprio diretório de build; a linha de <code>_deps/</code> está ali para o caso de alguém configurar o projeto com outro diretório binário, que é o arranjo em que o código de terceiro escapa do <code>.gitignore</code> sem ninguém perceber.',
                        'O que sustenta a reprodutibilidade não é versionar o que foi baixado: é a tag imutável declarada no <code>CMakeLists.txt</code>, e é ela que garante que quem clonar o projeto compile a mesma coisa.',
                    ],
                },
            ],
        },
        {
            'id': 'actions',
            'titulo': 'GitHub Actions para C++',
            'origem': 'unidade-1/aula05-git-github',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'codigo',
                    'lang': 'yaml',
                    'legenda': 'ci.yml - o portão, rodado a cada push',
                    'codigo': """\
name: CI
on: [push, pull_request]
jobs:
  build-and-test:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - name: CMake configure
        run: cmake -B build -DCMAKE_BUILD_TYPE=Debug
      - name: Build
        run: cmake --build build --parallel
      - name: Portao
        run: make verifica""",
                },
                {
                    'tipo': 'prosa',
                    'html': 'O CI roda a cada push, e o que ele afirma é o mesmo que <code>make verifica</code> afirma na sua máquina: zero aviso, os testes verdes, o despejo do replay idêntico byte a byte, e o contador de instâncias vivas fechando em zero. Pull request com uma das quatro condições vermelha não é revisado.',
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-1/aula05-git-github',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Gere um arquivo .gitignore completo para um projeto C++17 com CMake, VS Code e CLion. Inclua comentários explicando cada seção. Não inclua entradas desnecessárias."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'LLMs geram .gitignore genéricos demais (com entradas para Java, Python, etc.) ou incompletos (esquecendo arquivos de sanitizer ou de IDE específica). Sempre revise e simplifique.',
                    ],
                },
            ],
        },
        {
            'id': 'intro',
            'titulo': 'LLMs como Copiloto no Desenvolvimento OO',
            'origem': 'unidade-1/aula06-llms-copiloto',
            'compartilhado': False,
            'blocos': [],
        },
        {
            'id': 'workflow',
            'titulo': 'Workflow de Desenvolvimento com LLM',
            'origem': 'unidade-1/aula06-llms-copiloto',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Tarefa',
                        'Efetividade do LLM',
                        'O que verificar',
                    ],
                    'linhas': [
                        [
                            'Esboço de classe (interface)',
                            '·····',
                            'Convenções, const, noexcept',
                        ],
                        [
                            'Implementação de método simples',
                            '····',
                            'Regra dos 5, exceções',
                        ],
                        [
                            'Testes Catch2',
                            '····',
                            'Cobertura, Approx para float',
                        ],
                        [
                            'Refatoração SOLID',
                            '···',
                            'LSP, ISP geralmente errados',
                        ],
                        [
                            'Templates complexos',
                            '··',
                            'Dedução de tipo, SFINAE',
                        ],
                        [
                            'Concorrência',
                            '·',
                            'Race conditions sutis',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Use o LLM como par de programação, não como oráculo',
                    'paragrafos': [
                        'O LLM é como um colega experiente que às vezes dorme na roda. Revise tudo, compile, teste com sanitizers.',
                    ],
                },
            ],
        },
        {
            'id': 'prompts',
            'titulo': 'Anatomia de um Prompt Eficaz',
            'origem': 'unidade-1/aula06-llms-copiloto',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'prosa',
                    'html': 'A resposta acompanha a qualidade da pergunta, e prompt vago produz resposta genérica. Um pedido de programação que serve tem quatro partes - contexto, restrições, tarefa e <strong>portão</strong> -, e a quarta é a que quase nunca aparece. Vale experimentar a diferença: prompt sem portão declarado produz código que parece pronto, e prompt com portão declarado produz código que o modelo já tenta defender, às vezes trazendo o teste junto, o que é ótimo e é armadilha - o teste que veio com o código é o item R7 da rubrica.',
                },
                {
                    'tipo': 'codigo',
                    'lang': 'text',
                    'legenda': 'Estrutura recomendada',
                    'codigo': """\
Contexto:
  Projeto: Deriva, roguelike de terminal em C++17
  Convenções: snake_case, identificadores e comentários em português,
              sem new nem delete crus

Tarefa:
  A classe, com a interface pública nomeada membro a membro.

Restrições:
  - C++17, e ele é teto: nada de C++20
  - sem include que não seja usado
  - sem dependência que não esteja no CMakeLists.txt

Portão:
  - compila com -std=c++17 -Wall -Wextra -Wpedantic -Wconversion
    -Wsign-conversion sem uma linha de aviso
  - passa nestes testes: <os que você escreveu antes de pedir>""",
                },
            ],
        },
        {
            'id': 'erros',
            'titulo': 'Padrões de Erro em Código Gerado por LLM',
            'origem': 'unidade-1/aula06-llms-copiloto',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Erro',
                        'Frequência',
                        'Como detectar',
                    ],
                    'linhas': [
                        [
                            'Sem destrutor virtual',
                            'Muito comum',
                            'Compilar com -Wall',
                        ],
                        [
                            'Object slicing em vector',
                            'Comum',
                            'Testar com ASan',
                        ],
                        [
                            'PascalCase em vez de snake_case',
                            'Muito comum',
                            'Revisão visual',
                        ],
                        [
                            'new/delete em vez de unique_ptr',
                            'Comum',
                            "grep 'new '",
                        ],
                        [
                            'Sem noexcept em move',
                            'Comum',
                            'Checar headers',
                        ],
                        [
                            'Testes sem Catch::Approx para float',
                            'Comum',
                            'Revisar testes',
                        ],
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O código gerado desta aula está no repositório',
                    'paragrafos': [
                        '<code>exemplos/deriva/revisao_ia/gerado.hpp</code> é o que um modelo produziu para o pedido "uma classe que guarda as leituras de um sensor da estação, com hierarquia e inventário". Ele compila sem uma linha de aviso e passa no teste que o próprio modelo escreveu, e tem três defeitos plantados, um por item da rubrica. Nenhum é erro de digitação: os três são decisões plausíveis, e é isso que os torna caros.',
                        'Os três estão marcados no arquivo com <code>DEFEITO n</code> e o item da rubrica que cada um viola, e a tarefa é encontrá-los antes de ler as marcas. Os trechos extraídos mais abaixo nesta página são a base da hierarquia gerada e o teste que veio com ela - leia os dois primeiro, sozinho.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-1/aula06-llms-copiloto',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Revise o código C++17 abaixo e identifique: (1) todos os warnings que -Wall -Wextra emitiria, (2) comportamentos indefinidos, (3) violações de boas práticas C++ modernas. Para cada problema, cite a linha e proponha a correção."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        "LLMs são auto-validadores ruins - tendem a dizer 'o código está correto' quando não está. Sempre compile você mesmo. Use o LLM para revisão, mas o compilador como árbitro final.",
                    ],
                },
            ],
        },
        {
            'id': 'retrospectiva',
            'titulo': 'Retrospectiva do Semestre',
            'origem': 'unidade-3/aula27-qt-llms',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Unidade',
                        'Conceitos-chave',
                        'Deriva',
                    ],
                    'linhas': [
                        [
                            'I - Fundamentos',
                            'Infraestrutura, C++17, Git e revisão de código gerado, tipos, UML, classes, ciclo de vida, operações especiais',
                            'v0.0 → v0.3',
                        ],
                        [
                            'II - Hierarquias, posse e despacho',
                            'Herança, virtuais, posse exclusiva e compartilhada, movimento, operadores, replay, diamante, RTTI',
                            'v1.0 → v1.8',
                        ],
                        [
                            'III - Genericidade, robustez e projeto',
                            'Templates e CRTP, erros, STL e lambdas, concorrência, serialização, SOLID, padrões, segundo front-end',
                            'v2.0 → v2.7',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'O Deriva atravessa as 26 aulas em vinte versões nomeadas, e cada uma delas é um estado do repositório que se pode voltar a visitar. É aí que o Git deixa de ser burocracia de entrega: o histórico é o registro das decisões de projeto do semestre, e o <code>DECISAO.md</code> de cada entrega é onde a justificativa fica escrita. Quando a caça ao bug da Aula 09 pedir em que momento a cópia rasa entrou no código, a resposta sai de um <code>git log</code> em segundos se cada commit fizer uma coisa, e sai de uma tarde de bissecção se um commit fizer sete.',
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'O que estudar em seguida',
                    'paragrafos': [
                        'Concepts e Ranges, que o Anexo A já traz como alvo opcional; C++20 além deles - módulos e corrotinas; concorrência estruturada, que a Aula 22 só panoramiza; e o lado de apresentação, que a Aula 26 abre com o segundo front-end sobre o mesmo núcleo.',
                        'Peça sempre fonte verificável ao LLM num roteiro de estudo, e confira cada recomendação antes de segui-la: recurso desatualizado e recurso inexistente saem com a mesma confiança.',
                    ],
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-3/aula27-qt-llms',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Escrevi um roguelike de terminal em C++17 ao longo de um semestre, com hierarquia polimórfica, posse por ponteiro inteligente, templates e um segundo front-end. Quais são as cinco áreas mais importantes para continuar evoluindo? Para cada uma: (1) o que aprender, (2) um recurso com autor e ano verificáveis, (3) um exercício prático sobre o código que já existe."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'Ao usar LLMs para roadmaps de aprendizado, peça sempre fontes verificáveis. LLMs podem sugerir recursos desatualizados ou inexistentes. Verifique cada recomendação antes de seguir.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Crie um repositório Git local para o Deriva v0.0 e faça ao menos três commits com mensagem que diga o que o commit faz, tais como <code>feat: CMakeLists com padrao C++17 e extensoes desligadas</code>, <code>feat: Catch2 por FetchContent como SYSTEM</code> e <code>test: teste de fumaca</code>. Depois leia o histórico com <code>git log --oneline</code> e diga, para cada commit, qual decisão de projeto ele registra.',
            'origem': 'unidade-1/aula05-git-github',
        },
        {
            'n': '02',
            'html': 'Provoque um conflito de merge: crie duas branches que mudam a mesma linha do <code>CMakeLists.txt</code>, tente o merge, e resolva à mão. Transcreva os comandos e explique o que os marcadores <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code>, <code>=======</code> e <code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> delimitam. Por que commitar com eles dentro de um <code>.cpp</code> é o erro que se comete uma vez só?',
            'origem': 'unidade-1/aula05-git-github',
        },
        {
            'n': '03',
            'html': 'Use <code>git bisect</code> para achar o commit que introduz um defeito num histórico de demonstração preparado pelo docente. Depois responda: quantos passos o <code>bisect</code> levou, e quantos ele levaria se cada commit tivesse feito sete coisas em vez de uma?',
            'origem': 'unidade-1/aula05-git-github',
        },
        {
            'n': '04',
            'html': 'Configure um hook de pre-commit que rode <code>clang-format --dry-run --Werror</code> e recuse o commit de código mal formatado. Explique por que um hook local não substitui o portão do CI, e o que cada um dos dois pega que o outro não pega.',
            'origem': 'unidade-1/aula05-git-github',
        },
        {
            'n': '01',
            'html': 'Leia <code>exemplos/deriva/revisao_ia/gerado.hpp</code> sem olhar as marcas de <code>DEFEITO</code> e sem olhar a versão revisada do mesmo arquivo. Aplique os sete itens da rubrica, um por um, por escrito. Depois compare o seu parecer com os três defeitos plantados: quantos você achou, e qual item da rubrica pegou cada um?',
            'origem': 'unidade-1/aula06-llms-copiloto',
        },
        {
            'n': '02',
            'html': 'Rode <code>exemplos/deriva/testes/test_revisao_ia.cpp</code> e confirme que o teste que veio com o código gerado passa. Depois escreva o teste que <strong>falharia</strong> na versão com defeito e passa na revisada. Qual dos dois testes prova algo sobre o que a classe promete?',
            'origem': 'unidade-1/aula06-llms-copiloto',
        },
        {
            'n': '03',
            'html': 'Escreva um prompt de revisão de código, seguindo a estrutura de quatro partes desta aula, e aplique-o ao <code>gerado.hpp</code>. O modelo achou os três defeitos? Em qual ele falhou, e o que faltava no seu pedido para que ele o encontrasse?',
            'origem': 'unidade-1/aula06-llms-copiloto',
        },
        {
            'n': '04',
            'html': 'Peça a um LLM que gere testes Catch2 para a hierarquia de <code>gerado.hpp</code>, exigindo caso de fronteira e caso de erro nomeados. Quantos dos testes gerados repetem o que <code>test_revisao_ia.cpp</code> já afirma, e quantos casos não cobertos ele identificou? Quantos afirmam detalhe interno em vez de comportamento?',
            'origem': 'unidade-1/aula06-llms-copiloto',
        },
        {
            'n': '01',
            'html': 'Aplique a rubrica ao seguinte código, e diga qual item cada defeito viola: <code>class Pilha { int* arr; int topo; public: Pilha() { arr = new int[100]; topo=0; } void empilhar(int x) { arr[topo++]=x; } int desempilhar() { return arr[--topo]; } };</code>',
            'origem': 'unidade-3/aula27-qt-llms',
        },
        {
            'n': '02',
            'html': 'Escreva um prompt que instrua um LLM a refatorar o código do exercício anterior com <code>std::vector</code>, validação nos métodos e const-correctness. Depois aplique a rubrica <strong>à refatoração</strong>: o modelo introduziu defeito novo ao consertar o antigo?',
            'origem': 'unidade-3/aula27-qt-llms',
        },
        {
            'n': '03',
            'html': 'Escolha uma classe do Deriva que você ainda não escreveu e peça-a a um LLM com o prompt completo desta aula, portão declarado incluído. Compile com o conjunto de avisos da Aula 02 e registre num <code>DECISAO.md</code> o que você aceitou, o que recusou, e por quê.',
            'origem': 'unidade-3/aula27-qt-llms',
        },
        {
            'n': '04',
            'html': 'Escreva um relatório de uma página sobre o seu semestre no Deriva: quais decisões de projeto - herança ou composição, virtual ou template, quem tem a posse - você mudaria com o que aprendeu depois, e em que momentos exatos o LLM ajudou e em que momentos atrapalhou. Cite ao menos um caso em que a rubrica pegou algo que você teria aceitado.',
            'origem': 'unidade-3/aula27-qt-llms',
        },
    ],
    'pendencias': [],
}
