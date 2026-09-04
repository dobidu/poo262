# MIGRAÇÃO DO LIVRO - 27 capítulos → 26 + 3 anexos

Gerado por `build/extrair_livro.py` a partir de `legado/poo.docx`.
O script se recusa a escrever se alguma seção do v1 ficar sem destino;
esta tabela é a prova, seção por seção, de que nenhuma ficou.

## Destino de cada seção do v1

| cap. v1 | seção | título | vai para |
|---|---|---|---|
| 1 | `intro` | (abertura) | Cap. 1 |
| 1 | `1.1` | Gerenciamento de Complexidade em Software | Cap. 1 |
| 1 | `1.2` | Limitações do Modelo Procedural | Cap. 1 |
| 1 | `1.3` | Os Quatro Pilares da POO | Cap. 1 |
| 1 | `1.4` | Exemplo Comparativo: Sistema de Alunos em C vs. C++ | Cap. 1 |
| 1 | `1.5` | Tabela Comparativa: C Procedural vs. C++ OO | Cap. 1 |
| 1 | `Exercícios Propostos` | Exercícios Propostos | Cap. 1 |
| 2 | `intro` | (abertura) | Cap. 3 |
| 2 | `2.1` | Entrada e Saída: de printf/scanf a cout/cin | Cap. 3 |
| 2 | `2.2` | Strings: de char\[\] a std::string | Cap. 3 |
| 2 | `2.3` | Ponteiros vs. Referências | Cap. 3 |
| 2 | `2.4` | C++ Moderno Essencial | Cap. 3 |
| 2 | `Exercícios Propostos` | Exercícios Propostos | Cap. 3 |
| 3 | `intro` | (abertura) | Cap. 5 |
| 3 | `3.1` | Baseadas em Objetos vs. Orientadas a Objetos | Cap. 5 |
| 3 | `3.2` | Sistemas de Tipos: os Eixos Fundamentais | Cap. 5 |
| 3 | `3.3` | Mecanismos de Reutilização: Herança, Composição e Traits | Cap. 5 |
| 3 | `3.4` | Posicionando as Linguagens | Cap. 5 |
| 3 | `Exercícios Propostos` | Exercícios Propostos | Cap. 5 |
| 4 | `intro` | (abertura) | Cap. 2 |
| 4 | `4.1` | O Modelo de Compilação de C++ | Cap. 2 |
| 4 | `4.2` | CMake - O Sistema de Build da Disciplina | Cap. 2 |
| 4 | `4.3` | GDB - Depuração Básica | Cap. 2 |
| 4 | `4.4` | Sanitizers - Detecção de Erros em Runtime | Cap. 2 |
| 4 | `4.5` | Transição de Python/C para C++ | Cap. 2 |
| 4 | `Exercícios Propostos` | Exercícios Propostos | Cap. 2 |
| 5 | `intro` | (abertura) | Cap. 4 |
| 5 | `5.1` | Por que Versionar Código? | Cap. 4 |
| 5 | `5.2` | Conceitos Fundamentais | Cap. 4 |
| 5 | `5.3` | Fluxo de Trabalho Individual | Cap. 4 |
| 5 | `5.4` | Branches e Merge | Cap. 4 |
| 5 | `5.5` | GitHub - Colaboração e Entrega | Cap. 4 |
| 5 | `5.6` | .gitignore para Projetos C++ | Cap. 4 |
| 5 | `Exercícios Propostos` | Exercícios Propostos | Cap. 4 |
| 6 | `intro` | (abertura) | Cap. 4 |
| 6 | `6.1` | O que São LLMs e Como Funcionam | Cap. 4 |
| 6 | `6.2` | Prompts Eficazes para POO | Cap. 4 |
| 6 | `6.3` | Prompts por Contexto de Desenvolvimento OO | Cap. 4 |
| 6 | `6.4` | Análise Crítica de Código Gerado por LLMs | Cap. 4 |
| 6 | `6.5` | Limites, Riscos e Responsabilidades | Cap. 4 |
| 6 | `Exercícios Propostos` | Exercícios Propostos | Cap. 4 |
| 7 | `intro` | (abertura) | Cap. 6 |
| 7 | `7.1` | Por que UML? A Modelagem Antes do Código | Cap. 6 |
| 7 | `7.2` | Diagrama de Classes - Notação Essencial | Cap. 6 |
| 7 | `7.3` | Relacionamentos entre Classes | Cap. 6 |
| 7 | `7.4` | Diagrama de Sequência - Interação entre Objetos | Cap. 6 |
| 7 | `7.5` | Fluxo de Trabalho com UML Leve | Cap. 6 |
| 7 | `Exercícios Propostos` | Exercícios Propostos | Cap. 6 |
| 8 | `intro` | (abertura) | Cap. 7 |
| 8 | `8.1` | Declaração e Definição de Classes | Cap. 7 |
| 8 | `8.2` | Modificadores de Acesso | Cap. 7 |
| 8 | `8.3` | O Ponteiro this | Cap. 7 |
| 8 | `8.4` | Const-Correctness | Cap. 7 |
| 8 | `8.5` | Membros Estáticos (static) | Cap. 7 |
| 8 | `Exercícios Propostos` | Exercícios Propostos | Cap. 7 |
| 9 | `intro` | (abertura) | Cap. 8 |
| 9 | `9.1` | O que é o Ciclo de Vida de um Objeto? | Cap. 8 |
| 9 | `9.2` | Tipos de Construtores | Cap. 8 |
| 9 | `9.3` | Listas de Inicialização - Por que Usar Sempre | Cap. 8 |
| 9 | `9.4` | Destrutores e a Ordem de Destruição | Cap. 8 |
| 9 | `9.5` | RAII - Resource Acquisition Is Initialization | Cap. 8 |
| 9 | `Exercícios Propostos` | Exercícios Propostos | Cap. 8 |
| 10 | `intro` | (abertura) | Cap. 8 |
| 10 | `10.1` | O que o Compilador Gera Automaticamente | Cap. 9 |
| 10 | `10.2` | Regra do Zero | Cap. 9 |
| 10 | `10.3` | Regra dos Três (Pré-C++11) | Cap. 9 |
| 10 | `10.4` | Regra dos Cinco (C++11 em diante) | Cap. 14 |
| 10 | `10.5` | Semântica de Valor vs. Referência | Cap. 14 |
| 10 | `Exercícios Propostos` | Exercícios Propostos | Cap. 8, Cap. 9, Cap. 14 **⚠ duas metades** |
| 11 | `intro` | (abertura) | Cap. 12 |
| 11 | `11.1` | Por que Smart Pointers? | Cap. 12 |
| 11 | `11.2` | unique_ptr - Propriedade Exclusiva | Cap. 12 |
| 11 | `11.3` | shared_ptr - Propriedade Compartilhada | Cap. 13 |
| 11 | `11.4` | weak_ptr - Quebrando Ciclos | Cap. 13 |
| 11 | `11.5` | Regra de Escolha | Cap. 13 |
| 11 | `Exercícios Propostos` | Exercícios Propostos | Cap. 12, Cap. 13 **⚠ duas metades** |
| 12 | `intro` | (abertura) | Cap. 14 |
| 12 | `12.1` | O Problema: Cópias Desnecessárias | Cap. 14 |
| 12 | `12.2` | lvalues e rvalues | Cap. 14 |
| 12 | `12.3` | std::move e Referências a rvalue (T&&) | Cap. 14 |
| 12 | `Exercícios Propostos` | Exercícios Propostos | Cap. 14 |
| 13 | `intro` | (abertura) | Cap. 15 |
| 13 | `13.1` | Por que Sobrecarregar Operadores? | Cap. 15 |
| 13 | `13.2` | Regras de Ouro | Cap. 15 |
| 13 | `13.3` | Exemplo: sample com Operadores | Cap. 15 |
| 13 | `Exercícios Propostos` | Exercícios Propostos | Cap. 15 |
| 14 | `intro` | (abertura) | Cap. 16 |
| 14 | `14.1` | Por que Testes Automatizados? | Cap. 16 |
| 14 | `14.2` | Configurando Catch2 com CMake | Cap. 16 |
| 14 | `14.3` | Primeiro Arquivo de Teste | Cap. 16 |
| 14 | `14.4` | Testando Comportamentos de Exceção e Edge Cases | Cap. 16 |
| 14 | `Exercícios Propostos` | Exercícios Propostos | Cap. 16 |
| 15 | `intro` | (abertura) | Cap. 10 |
| 15 | `15.1` | Herança como Modelagem de Domínio | Cap. 10 |
| 15 | `15.2` | Sintaxe e Tipos de Herança em C++ | Cap. 10 |
| 15 | `15.3` | Hierarquia de Efeitos - Sintonia v1.0 | Cap. 10 |
| 15 | `15.4` | Construtores e Destrutores na Hierarquia | Cap. 10 |
| 15 | `Exercícios Propostos` | Exercícios Propostos | Cap. 10 |
| 16 | `intro` | (abertura) | Cap. 17 |
| 16 | `16.1` | Herança Múltipla: Capacidades e Riscos | Cap. 17 |
| 16 | `16.2` | O Problema do Diamante | Cap. 17 |
| 16 | `16.3` | Resolvendo com Herança Virtual | Cap. 17 |
| 16 | `16.4` | Contraste com Java/C# | Cap. 17 |
| 16 | `Exercícios Propostos` | Exercícios Propostos | Cap. 17 |
| 17 | `intro` | (abertura) | Cap. 11 |
| 17 | `17.1` | A Necessidade de Funções Virtuais | Cap. 11 |
| 17 | `17.2` | override e final | Cap. 11 |
| 17 | `17.3` | Funções Virtuais Puras e Classes Abstratas | Cap. 11 |
| 17 | `17.4` | Mecanismo Interno: vtable e vptr | Cap. 11 |
| 17 | `Exercícios Propostos` | Exercícios Propostos | Cap. 11 |
| 18 | `intro` | (abertura) | Cap. 18 |
| 18 | `18.1` | Polimorfismo Dinâmico em Ação | Cap. 18 |
| 18 | `18.2` | dynamic_cast - Downcasting Seguro | Cap. 18 |
| 18 | `18.3` | RTTI - typeid e type_info | Cap. 18 |
| 18 | `Exercícios Propostos` | Exercícios Propostos | Cap. 18 |
| 19 | `intro` | (abertura) | Cap. 19 |
| 19 | `19.1` | O que São Templates? | Cap. 19 |
| 19 | `19.2` | Templates de Função | Cap. 19 |
| 19 | `19.3` | Templates de Classe - Buffer\<T\> | Cap. 19 |
| 19 | `19.4` | Polimorfismo Estático vs. Dinâmico | Cap. 19 |
| 19 | `19.5` | CRTP - Curiously Recurring Template Pattern | Cap. 19 |
| 19 | `Exercícios Propostos` | Exercícios Propostos | Cap. 19 |
| 20 | `intro` | (abertura) | Anexo A |
| 20 | `20.1` | O Problema dos Templates sem Restrições | Anexo A |
| 20 | `20.2` | Ranges - Programação Funcional sobre Sequências | Anexo A |
| 20 | `Exercícios Propostos` | Exercícios Propostos | Anexo A |
| 21 | `intro` | (abertura) | Cap. 20 |
| 21 | `21.1` | Exceções em C++ | Cap. 20 |
| 21 | `21.2` | std::optional - Resultado Ausente sem Exceção | Cap. 20 |
| 21 | `21.3` | std::variant - Resultado ou Erro | Cap. 20 |
| 21 | `Exercícios Propostos` | Exercícios Propostos | Cap. 20 |
| 22 | `intro` | (abertura) | Cap. 21 |
| 22 | `22.1` | Contêineres Essenciais | Cap. 21 |
| 22 | `22.2` | Algoritmos STL | Cap. 21 |
| 23 | `intro` | (abertura) | Cap. 22 |
| 23 | `23.1` | std::thread - Criação e Join | Cap. 22 |
| 23 | `23.2` | std::mutex e Race Conditions | Cap. 22 |
| 24 | `intro` | (abertura) | Cap. 23 |
| 24 | `24.1` | Estratégias de Serialização | Cap. 23 |
| 24 | `24.2` | Serialização JSON com nlohmann/json | Cap. 23 |
| 25 | `intro` | (abertura) | Cap. 24 |
| 25 | `25.1` | S - Responsabilidade Única (SRP) | Cap. 24 |
| 25 | `25.2` | O - Aberto/Fechado (OCP) | Cap. 24 |
| 25 | `25.3` | L - Substituição de Liskov (LSP) | Cap. 24 |
| 25 | `25.4` | I - Segregação de Interfaces (ISP) | Cap. 24 |
| 25 | `25.5` | D - Inversão de Dependência (DIP) | Cap. 24 |
| 25 | `Exercícios Propostos` | Exercícios Propostos | Cap. 24 |
| 26 | `intro` | (abertura) | Cap. 25 |
| 26 | `26.1` | Strategy - Encapsular Algoritmos | Cap. 25 |
| 26 | `26.2` | Observer - Notificação de Eventos | Cap. 25 |
| 26 | `26.3` | Factory Method - Criação Polimórfica | Cap. 25 |
| 26 | `26.4` | Decorator - Efeitos Encadeados | Cap. 25 |
| 26 | `26.5` | Composite - Hierarquia de Efeitos | Cap. 25 |
| 26 | `26.6` | Singleton - Uso Correto e Abusos | Cap. 25 |
| 26 | `Exercícios Propostos` | Exercícios Propostos | Cap. 25 |
| 27 | `intro` | (abertura) | Cap. 26 |
| 27 | `27.1` | Arquitetura do Qt | Cap. 26 |
| 27 | `27.2` | Separação Domínio/Apresentação com Qt | Cap. 26 |
| 27 | `27.3` | LLMs no Ciclo OO - Aprofundamento | Cap. 4 |
| 27 | `Exercícios Propostos` | Exercícios Propostos | Cap. 4, Cap. 26 **⚠ duas metades** |

## Orçamento de páginas

| unidade | capítulos | páginas-alvo |
|---|---|---|
| I - Fundamentos | 1 - 9 | ~40 |
| II - Hierarquias, posse e despacho | 10 - 18 | ~48 |
| III - Genericidade, robustez e projeto | 19 - 26 | ~46 |
| anexos A - C | - | ~14 |
| **total** | **26 + 3** | **~148** |

De 108 páginas para cerca de 148. O crescimento não vem de capítulo novo: vem da sintaxe de C++17 que falta e se distribui por dez capítulos, do bloco de instrumentação sem ferramenta externa, e das divisões - que custam páginas de moldura em cada metade.

## Pendências

- **Cap. 1** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 2** - escrever: gdb com ponto de parada em destrutor
- **Cap. 2** - escrever: portão `make verifica`
- **Cap. 2** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 3** - escrever: std::string_view e a pendência de tempo de vida
- **Cap. 3** - escrever: ligações estruturadas
- **Cap. 3** - escrever: [[nodiscard]] e [[maybe_unused]]
- **Cap. 4** - escrever: rubrica de revisão de código OO gerado por IA, publicada como artefato
- **Cap. 4** - fatia llm - conferir parágrafo por parágrafo que nada ficou de fora
- **Cap. 4** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 6** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 7** - escrever: o contador `vivos` como exemplo canônico de membro estático
- **Cap. 7** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 8** - escrever: instrumentação de ciclo de vida
- **Cap. 8** - escrever: terminal_bruto e o RAII com consequência física
- **Cap. 8** - fatia raii - conferir parágrafo por parágrafo que nada ficou de fora
- **Cap. 8** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 9** - fatia zero-tres - conferir parágrafo por parágrafo que nada ficou de fora
- **Cap. 9** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 10** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 11** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 12** - fatia unique - conferir parágrafo por parágrafo que nada ficou de fora
- **Cap. 12** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 13** - fatia shared - conferir parágrafo por parágrafo que nada ficou de fora
- **Cap. 13** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 14** - escrever: std::forward e encaminhamento perfeito
- **Cap. 14** - escrever: correção: estado válido mas não-especificado, com SSO
- **Cap. 14** - fatia cinco - conferir parágrafo por parágrafo que nada ficou de fora
- **Cap. 14** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 15** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 16** - escrever: replay determinístico como portão de refatoração
- **Cap. 16** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 17** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 18** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 19** - escrever: contador_de_instancias<T> por CRTP
- **Cap. 19** - fatia absorve-20 - conferir parágrafo por parágrafo que nada ficou de fora
- **Cap. 19** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 20** - escrever: std::filesystem no carregamento de mapa
- **Cap. 20** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 21** - escrever: lambdas como conteúdo de capítulo
- **Cap. 21** - escrever: std::clamp
- **Cap. 21** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 22** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 23** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 24** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 25** - prosa/código do Sintonia a migrar para o Deriva
- **Cap. 26** - fatia qt - conferir parágrafo por parágrafo que nada ficou de fora
- **Cap. 26** - prosa/código do Sintonia a migrar para o Deriva
- **Anexo B** - transcrever a referência rápida de C++17 do site
- **Glossário** - revisar: os verbetes novos da disciplina (contador `vivos`, replay determinístico, SSO, portão `make verifica`) precisam entrar
- **Referências Bibliográficas** - a bibliografia do livro NÃO foi auditada neste ciclo (PLANO-LIVRO §5). Duas correções já sabidas: autoria do Catch2 é Nash e Hořeňovský, e *Programming: Principles and Practice* está na 3ª ed., 2024. Falta acrescentar Josuttis, *C++17 - The Complete Guide*, e rodar a checagem de duplicatas
- **Cap. 27 §Exercícios Propostos** - foi para os capítulos [4, 26] do v2 - separar o texto
- **Cap. 10 §Exercícios Propostos** - foi para os capítulos [8, 9, 14] do v2 - separar o texto
- **Cap. 11 §Exercícios Propostos** - foi para os capítulos [12, 13] do v2 - separar o texto

**54 pendências.**
