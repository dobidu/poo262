# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: unidade-1/aula04-transicao-cpp
Página inteira.
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site v2 e do livro v2. O que não se deve fazer é rodar o extrator de
novo depois de editar - ele sobrescreve. Se precisar reextrair, faça em branch.

Pendências desta aula: 0 (ver conteudo/PENDENCIAS.md)
"""

AULA = {
    'n': 2,
    'slug': 'a02',
    'titulo': 'Infraestrutura do programador C++',
    'curto': 'Infraestrutura: CMake, FetchContent, gdb',
    'unidade': 'I',
    'cap_v1': [
        4,
    ],
    'origem_v1': [
        'unidade-1/aula04-transicao-cpp',
    ],
    'fatia': None,
    'deriva': 'v0.0',
    'lab': 'LAB-01',
    'interativos': [
        'expansor',
    ],
    'nota_migracao': 'Sobe do 4º para o 2º lugar. Entra FetchContent com FTXUI e Catch2 como dependência SYSTEM, para o portão de zero warnings incidir só no código do estudante. Sai o bloco de sanitizers como portão (o laboratório não os tem) e entra gdb com ponto de parada em destrutor.',
    'objetivos': [
        'Configurar o ambiente da disciplina: g++, CMake, gdb e git',
        'Compreender o modelo de compilação de C++ - pré-processamento, compilação e ligação - e saber em qual das três etapas cada erro aparece',
        'Ler o <code>CMakeLists.txt</code> do Deriva: o padrão fixado, o portão de aviso, e a dependência externa por <code>FetchContent</code> em tag imutável',
        'Rodar o portão <code>make verifica</code> e dizer qual das quatro condições falhou',
        'Parar o <code>gdb</code> num destrutor e ler de onde ele foi chamado',
        'Comparar C++ com C e com Python nas construções mais comuns',
    ],
    'slides': [
        {
            'id': 'intro',
            'titulo': 'Transição Python/C → C++ Moderno',
            'origem': 'unidade-1/aula04-transicao-cpp',
            'compartilhado': False,
            'blocos': [],
        },
        {
            'id': 'ambiente',
            'titulo': 'Configurando o Ambiente',
            'origem': 'unidade-1/aula04-transicao-cpp',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'codigo',
                    'lang': 'bash',
                    'legenda': 'Instalação e verificação (Ubuntu/Debian)',
                    'codigo': """\
# Compilador e ferramentas
sudo apt install -y build-essential g++ cmake git gdb

# Verificar. O material foi medido no g++ 13.3; C++17 completo vem do 9 em
# diante, e o CMakeLists.txt do Deriva exige CMake 3.16 ou mais recente.
g++ --version
cmake --version

# Primeiro programa, do echo ao binário que roda
echo '#include <iostream>
int main() { std::cout << "Olá, C++17!\\n"; }' > hello.cpp
g++ -std=c++17 -Wall -Wextra -Wpedantic hello.cpp -o hello && ./hello

# O Deriva, que já vem com CMakeLists.txt: configurar, compilar, rodar o portão
cd exemplos/deriva
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --parallel
make verifica""",
                },
                {
                    'tipo': 'callout',
                    't': 'tip',
                    'titulo': 'Sanitizer é ferramenta, e não portão',
                    'paragrafos': [
                        '<code>-fsanitize=address,undefined</code> aponta acesso fora de limite, dupla liberação e comportamento indefinido em execução, com a linha do defeito e a linha da alocação. Use-o sempre que ele estiver disponível.',
                        'Ele não é critério de aceitação nesta disciplina, e a razão é material: as máquinas do laboratório não o têm. No Deriva ele fica atrás da opção <code>DERIVA_SANITIZERS</code>, desligada por padrão, e se liga com <code>make sanitizers</code>. O que ocupa o lugar dele são as três técnicas que não dependem de ferramenta externa - o contador de instâncias vivas da Aula 07, a instrumentação de ciclo de vida da Aula 08, e o <code>gdb</code> com ponto de parada em destrutor.',
                    ],
                },
            ],
        },
        {
            'id': 'compilacao',
            'titulo': 'Modelo de Compilação',
            'origem': 'unidade-1/aula04-transicao-cpp',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'tabela',
                    'cabeca': [
                        'Etapa',
                        'Entrada',
                        'Saída',
                        'Ferramenta',
                    ],
                    'linhas': [
                        [
                            'Pré-processamento',
                            'arquivo.cpp + headers',
                            'arquivo.ii (expandido)',
                            'cpp',
                        ],
                        [
                            'Compilação',
                            'arquivo.ii',
                            'arquivo.o (objeto)',
                            'g++',
                        ],
                        [
                            'Linkagem',
                            '*.o + bibliotecas',
                            'executável',
                            'ld (via g++)',
                        ],
                        [
                            'CMake',
                            'CMakeLists.txt',
                            'Makefile/Ninja',
                            'cmake',
                        ],
                    ],
                },
                {
                    'tipo': 'prosa',
                    'html': 'Saber em qual das três etapas o erro aconteceu economiza mais tempo de depuração que qualquer outra coisa desta aula. Símbolo não declarado é erro de <strong>compilação</strong>, e a mensagem cita o arquivo e a linha do uso; símbolo declarado e nunca definido é erro de <strong>ligação</strong>, e a mensagem - <code>undefined reference to</code> - não se parece nada com a primeira, não traz linha nenhuma, e aparece no fim, quando ninguém está mais olhando para o código que a causou.',
                },
                {
                    'tipo': 'prosa',
                    'html': 'A linha de compilação da disciplina não é digitada à mão em exercício nenhum: ela é o que o CMake gera a partir do <code>CMakeLists.txt</code>, com o padrão fixado e o conjunto de avisos embutido em cada invocação do compilador. É por isso que o Deriva se opera em dois comandos - <code>cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug</code> para configurar e <code>cmake --build build --parallel</code> para compilar - e não em uma chamada de <code>g++ -c</code> por arquivo seguida de uma de ligação. Os trechos do <code>CMakeLists.txt</code> extraídos mais abaixo nesta página são o arquivo que produz essa linha.',
                },
            ],
        },
        {
            'id': 'c-para-cpp',
            'titulo': 'De C e Python para C++',
            'origem': 'unidade-1/aula04-transicao-cpp',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'codigo',
                    'lang': 'cpp',
                    'legenda': 'Equivalências: Python/C → C++17 - o arquivo inteiro, e ele compila',
                    'codigo': """\
#include <iostream>
#include <vector>

// Python: def f(x) -> int:     C: int f(int x)
int f(int x) { return x * 2; }              // C++ - tipos obrigatórios

int main() {
  // Python: print("hello")       C: printf("hello\\n")
  std::cout << "hello" << '\\n';             // C++ - sem '\\n' faltando

  // Python: x = [1, 2, 3]        C: int arr[] = {1, 2, 3};
  std::vector<int> v = {1, 2, 3};           // C++ - dimensionado em execução

  // Python: for x in lista:      C: for (int i = 0; i < n; i++)
  for (int x : v) std::cout << f(x) << ' '; // C++ - sobre o contêiner, sem índice
  std::cout << '\\n';
}""",
                },
            ],
        },
        {
            'id': 'llm',
            'titulo': 'LLMs neste Tópico',
            'origem': 'unidade-1/aula04-transicao-cpp',
            'compartilhado': False,
            'blocos': [
                {
                    'tipo': 'callout',
                    't': 'llm',
                    'titulo': 'Prompt sugerido',
                    'paragrafos': [
                        '<em>"Tenho experiência em Python e estou aprendendo C++17. Mostre as 10 principais diferenças que vão me pegar de surpresa, com exemplos de código nos dois lados. Foque em: gerenciamento de memória, tipos, includes, e comportamento de strings."</em>',
                    ],
                },
                {
                    'tipo': 'callout',
                    't': 'warn',
                    'titulo': 'O que o LLM costuma errar',
                    'paragrafos': [
                        'LLMs tendem a listar diferenças óbvias (ponto e vírgula, chaves) e ignorar as perigosas: undefined behavior, object slicing, e a diferença entre cópia e referência em tipos não-primitivos.',
                    ],
                },
            ],
        },
    ],
    'exercicios': [
        {
            'n': '01',
            'html': 'Configure o ambiente seguindo <code>exemplos/deriva/LEIA-ME.md</code>. Compile o Deriva com <code>cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug</code> e <code>cmake --build build --parallel</code>, rode <code>make verifica</code>, e reporte o resultado das quatro condições, uma por uma.',
            'origem': 'unidade-1/aula04-transicao-cpp',
        },
        {
            'n': '02',
            'html': 'Crie um <code>CMakeLists.txt</code> mínimo que compile dois arquivos <code>.cpp</code> num executável, com <code>CMAKE_CXX_STANDARD 17</code>, <code>CMAKE_CXX_EXTENSIONS OFF</code> e o conjunto de avisos do Deriva. Ponha os sanitizers atrás de uma opção desligada por padrão, e explique em uma frase por que eles não entram na configuração de Debug.',
            'origem': 'unidade-1/aula04-transicao-cpp',
        },
        {
            'n': '03',
            'html': 'Traduza o seguinte código C para C++17 moderno (sem <code>malloc</code>, sem arrays crus, sem <code>printf</code>): <code>int* arr = malloc(10*sizeof(int)); for(int i=0;i&lt;10;i++) arr[i]=i; free(arr);</code>',
            'origem': 'unidade-1/aula04-transicao-cpp',
        },
        {
            'n': '04',
            'html': 'Compile <code>exemplos/deriva/sanitizers/defeitos_de_memoria.cpp</code> com <code>-fsanitize=address</code> e sem ele. Transcreva a diferença entre as duas execuções, e explique por que o acesso fora de limite não produz aviso de compilador nenhum. Depois pare o <code>gdb</code> num destrutor com <code>make gdb-dtor</code> e diga de onde ele foi chamado.',
            'origem': 'unidade-1/aula04-transicao-cpp',
        },
    ],
    'pendencias': [],
}
