# Glossário

Termos fundamentais da disciplina, em ordem alfabética. Cada verbete registra o capítulo em que o conceito entra, de forma que a consulta devolva também o lugar do material onde o mecanismo é desenvolvido. Os verbetes coincidem com os do glossário do site: uma fonte, dois meios.

**Abstração** (Cap. 1): Mecanismo pelo qual detalhes de implementação são ocultados, expondo apenas o essencial para o usuário de uma classe ou módulo.

**AddressSanitizer (ASan)** (Cap. 2): Instrumentação do compilador que detecta em execução erros de memória: uso após liberação, acesso fora dos limites, vazamentos. Nesta disciplina ele é **ferramenta**, e não portão: as máquinas do laboratório não o têm, e o portão de aceitação usa as três técnicas sem dependência externa - o contador de instâncias vivas, a instrumentação de ciclo de vida, e o `gdb` com ponto de parada em destrutor.

**`auto`** (Cap. 3): Palavra-chave de C++11 que instrui o compilador a deduzir o tipo de uma variável a partir da expressão de inicialização. Obrigatório para guardar uma lambda, cujo tipo não tem nome que se possa escrever.

**Caça ao bug** (Caps. 9, 11 e 24): Atividade em dupla, uma por unidade, em que cada equipe recebe uma versão do Deriva plausível e errada. A ordem de trabalho é cobrada: reproduzir a falha, explicá-la em uma frase **antes** de tocar no código, corrigir, e provar a correção. O instrumento de avaliação é a rubrica de revisão do Cap. 4.

**Classe abstrata** (Cap. 11): Classe com pelo menos uma função virtual pura (`= 0`); não pode ser instanciada diretamente.

**CMake** (Cap. 2): Sistema de build multiplataforma para projetos C++; gera Makefiles ou projetos de IDE a partir de `CMakeLists.txt`. No Deriva ele também fixa as dependências por `FetchContent`, com versão travada, e as declara como `SYSTEM`, para que o portão de zero aviso incida apenas sobre o código do estudante.

**Composição** (Cap. 9): Relação "tem um" entre classes, alternativa à herança quando não há relação "é um". `mapa` **compõe** uma `grade`: ele tem nome e ponto de entrada, que grade nenhuma tem, e não faz sentido passar um mapa onde se espera uma grade.

**Concept (C++20)** (Anexo A): Restrição sobre parâmetro de template promovida a entidade nomeada da linguagem, verificável, componível e capaz de aparecer na assinatura. Fora do padrão-alvo da disciplina; o equivalente em C++17 é `static_assert` no corpo da classe.

**const-correctness** (Cap. 7): Prática de marcar como `const` todos os métodos, parâmetros e variáveis que não devem modificar dados. No Deriva ela anda junto com `[[nodiscard]]`: um método `const` que devolve valor e não altera nada tem exatamente uma finalidade, e descartar o valor não pode ser intencional.

**Contador de instâncias vivas** (Cap. 7): `inline static int vivos`, incrementado no construtor e decrementado no destrutor. É o detector de vazamento que a disciplina usa do Cap. 7 ao fim do semestre, sem depender de sanitizer, e é a quarta condição do portão `make verifica`. Conta objetos, e não recursos: a cópia rasa da caça ao bug 1 fecha em zero. Não é seguro entre threads, e o Cap. 22 mostra exatamente esta variável perdendo um incremento.

**CRTP** (Cap. 19): *Curiously Recurring Template Pattern*: a classe derivada se passa como argumento de template para a própria base, o que resolve o polimorfismo em tempo de compilação, sem `vptr`. Aqui o alvo concreto é generalizar o contador `vivos` em `contador_de_instancias<T>`, e o que motiva o template é a repetição de tê-lo escrito à mão em três classes.

**Deriva** (Anexo C): O sistema-base da disciplina: um roguelike de terminal em que uma sonda de inspeção percorre uma estação orbital abandonada, através do console. Cada aula entrega uma versão que compila, da v0.0 à v2.7, e cada versão parte da anterior.

**Desenrolar da pilha** (Caps. 8 e 20): Processo pelo qual, ao ser lançada uma exceção, os destrutores dos objetos já construídos no caminho são chamados, de dentro para fora, até que um handler a capture. A exceção não pula os destrutores: ela os chama. É esta garantia, e nada mais, que faz RAII funcionar.

**Despacho dinâmico** (Cap. 11): Resolução em tempo de execução de qual implementação de um método virtual chamar, através da vtable.

**Destrutor virtual** (Cap. 11): Destrutor declarado `virtual` em classe base; garante que o destrutor da classe derivada seja chamado ao destruir através de ponteiro para a base. A sua ausência é a caça ao bug 2, e o contador `vivos` é o que a acusa.

**DIP** (Cap. 24): *Dependency Inversion Principle*: módulos de alto nível dependem de abstrações, e não de implementações concretas. No Deriva é o princípio cujo retorno está agendado, porque é ele que permite ao Cap. 26 pôr um front-end Qt sobre o mesmo núcleo.

**`dynamic_cast`** (Cap. 18): Operador de conversão de tipo verificado em execução; devolve `nullptr` quando aplicado a ponteiro incompatível, e lança `std::bad_cast` quando aplicado a referência.

**Encapsulamento** (Cap. 7): Agrupamento de dados e operações em uma classe, com controle de acesso. O critério para tornar um atributo privado é a existência de invariante a proteger, e não a regra automática: `vetor2` é um agregado de campos públicos porque qualquer par de inteiros é um `vetor2` válido.

**event loop** (Cap. 26): Laço que retira eventos de uma fila e os despacha para handlers ou slots; núcleo de aplicações Qt. Ele inverte o controle em relação ao laço próprio do Deriva de terminal, e é por isso que, sob Qt, o turno passa a ser resolvido dentro de um slot.

**Factory Method** (Cap. 25): Padrão que concentra num lugar a decisão de qual classe construir, devolvendo a base. No Deriva ele converte o glifo do mapa, ou a etiqueta de tipo do arquivo de partida, no objeto da classe certa.

**Fatiamento de objeto** (Cap. 10): Guardar um objeto de classe derivada por valor em contêiner da classe base descarta a parte específica da derivada. O sintoma é comportamento da base onde se esperava o da derivada, sem aviso e sem erro de execução.

**Garantia de exceção** (Cap. 20): O que uma função promete quando uma exceção passa por ela. São quatro níveis: `noexcept`, que é a promessa de não lançar, verificada em execução; **forte**, que é tudo ou nada, sem efeito parcial observável; **básica**, em que nada vazou e nenhuma invariante foi violada, porém o objeto pode ter mudado; e nenhuma, que é o objeto em estado inconsistente.

**GDB** (Cap. 2): Depurador do projeto GNU. A terceira das três técnicas que substituem o sanitizer ausente é o `gdb` com ponto de parada em destrutor, que mostra qual destrutor roda e de onde é chamado.

**God class** (Cap. 24): Classe que acumulou responsabilidades até ter vários motivos independentes para mudar. O sintoma prático não é o tamanho, é o que ela impede: no Deriva, testar a resolução de turno exigia um terminal, porque desenhar estava na mesma classe.

**Herança múltipla** (Cap. 17): Capacidade de uma classe derivar de mais de uma classe base; C++ a suporta, Java e C# a restringem a interfaces. O caso seguro em C++ é o de interfaces puras, sem dado na base, que não produz diamante.

**Herança virtual** (Cap. 17): Mecanismo de C++ para resolver o problema do diamante: garante que a classe base compartilhada tenha apenas um subobjeto na hierarquia.

**`if constexpr`** (Cap. 19): Construção de C++17 que decide o ramo em tempo de compilação. O ramo descartado é removido antes da instanciação, e portanto **não precisa nem ser válido** para o tipo em questão, o que é a propriedade que a distingue do `if` comum e a que a faz substituir SFINAE.

**Instrumentação de ciclo de vida** (Cap. 8): Segunda das três técnicas que substituem o sanitizer ausente: construtores, destrutores, cópia e movimento imprimindo a própria execução, de forma que a ordem de construção e de destruição fique observável. No Deriva é `src/instrumento.cpp`, e a opção `--traco` imprime o traço no fim.

**ISP** (Cap. 24): *Interface Segregation Principle*: interfaces pequenas e específicas, e clientes que não dependem de métodos que não usam. O sintoma da violação é o método virtual puro implementado com corpo vazio.

**Lambda** (Cap. 21): Expressão que produz um objeto invocável. Na leitura mais útil aqui, é açúcar sintático para uma classe anônima: a lista de captura são os membros, e o corpo é o `operator()`, que é `const` por padrão, o que é por que modificar uma captura por cópia exige `mutable`. Captura por referência é segura enquanto vive o escopo capturado.

**Ligações estruturadas** (Cap. 3): Construção de C++17 que decompõe um agregado, um par ou uma tupla em nomes: `for (const auto& [nome, delta] : tabela)`. Sem o `&` a ligação copia o elemento.

**LLM** (Cap. 4): *Large Language Model*: modelo de linguagem de grande escala treinado em texto e código, usado como assistente de programação. Nesta disciplina ele vem acompanhado de uma rubrica de revisão, que é o instrumento das três caças ao bug.

**LSP** (Cap. 24): *Liskov Substitution Principle*: objetos de uma subclasse devem poder substituir a superclasse sem alterar o comportamento correto do programa. A regra prática tem duas metades: a derivada não pode exigir mais que a base, nem prometer menos. Não é sobre assinatura, e portanto o compilador não a verifica.

**lvalue** (Cap. 14): Expressão com identidade e endereço acessível, que pode aparecer à esquerda de uma atribuição.

**`[[nodiscard]]`** (Cap. 3): Atributo de C++17 que faz o compilador avisar quando o valor devolvido é descartado. Vale no que devolve status ou recurso, e o aviso que ele provoca é o objetivo.

**`noexcept`** (Caps. 14 e 20): Especificador que promete que a função não lança. É verificado em execução, e quebrar a promessa chama `std::terminate`. Num construtor de movimento a marca muda o comportamento, e não só a documentação: `std::vector` só usa movimento ao realocar se ele for `noexcept`.

**`nullptr`** (Cap. 3): Literal de tipo `std::nullptr_t`, introduzido em C++11 para representar ponteiro nulo, em lugar de `NULL`, que é apenas o inteiro zero.

**Observer** (Cap. 25): Padrão em que interessados são notificados quando o estado de outro objeto muda. O defeito clássico da versão escrita à mão é o observador pendurado, e as três respostas são a desinscrição no destrutor, o `weak_ptr`, e a garantia de tempo de vida documentada. Signals e slots do Qt são este padrão implementado pelo framework.

**OCP** (Cap. 24): *Open/Closed Principle*: classes abertas para extensão e fechadas para modificação. Fechar para modificação custa uma hierarquia e uma indireção, e só se paga quando o conjunto de casos precisa crescer.

**Otimização de string curta** (Cap. 14): A `std::string` guarda cadeias curtas dentro do próprio objeto, sem alocar no heap - até 15 caracteres, neste alvo. A consequência prática, medida em `testes/test_move_string.cpp`: mover uma string curta **copia os bytes**, porque não há ponteiro a roubar, enquanto mover uma longa transfere o ponteiro de heap sem copiar conteúdo algum. Em nenhum dos dois casos a origem fica intacta nesta libstdc++ - ela esvazia nos quatro -, e é justamente por isso que o teste errado passa: a origem de um movimento fica em estado **válido mas não-especificado**, que não é obrigatoriamente vazio, e depender do vazio é depender de detalhe de implementação.

**`override`** (Cap. 11): Especificador de C++11 que faz o compilador confirmar que a função realmente sobrescreve um virtual da base. Escrevê-lo corretamente não é o mesmo que respeitar a substituição de Liskov.

**Padding** (Cap. 7): Bytes que o compilador insere entre membros, e no fim do objeto, para respeitar o alinhamento exigido por cada tipo. A ordem de declaração é sua, o alinhamento não é, e da combinação sai o `sizeof`: a `celula` do Deriva ocupa 12 bytes agrupada por tamanho e 16 na ordem em que se pensa nela.

**Polimorfismo** (Cap. 11): Capacidade de objetos de tipos diferentes responderem à mesma mensagem de maneiras distintas. Na forma dinâmica, a chamada resolve pelo tipo dinâmico do objeto, e não pelo tipo do ponteiro através do qual se chega até ele; custa um `vptr` por objeto e uma indireção por chamada. Sem `virtual`, a decisão passa ao tipo estático, sem que o compilador emita aviso.

**Portão `make verifica`** (Cap. 2): As quatro condições que toda entrega do Deriva satisfaz: zero aviso com `-Wall -Wextra -Wpedantic`; todos os testes verdes no `ctest`; despejo de replay idêntico byte a byte com semente fixa; e o contador de instâncias vivas fechando em zero. Nenhuma das quatro depende de sanitizer, e isso é deliberado.

**RAII** (Cap. 8): *Resource Acquisition Is Initialization*: o construtor adquire, o destrutor libera, e a garantia vem da ordem de destruição, inversa à de construção e válida inclusive quando é uma exceção que desenrola a pilha. No Deriva ele tem consequência física: `terminal_bruto` sem destrutor deixa o terminal do estudante inutilizável **depois** que o programa sai.

**Ranges (C++20)** (Anexo A): Biblioteca que generaliza os algoritmos da STL para trabalhar com views preguiçosas e composição funcional. Fora do padrão-alvo. Uma view não possui os elementos que enxerga, o que é a mesma armadilha do `std::string_view`.

**Regra do Zero** (Cap. 9): Se a classe não gerencia recurso, nenhuma das operações especiais deve ser declarada: as que o compilador gera são corretas e não envelhecem quando um membro é acrescentado. A `grade` do Deriva é a regra do zero em forma pura, e o que vale ler nela é o que **não** está escrito.

**Regra dos Cinco** (Cap. 14): Ao declarar uma das cinco operações especiais, decida sobre as outras quatro. Declarar o destrutor e esquecer a cópia é o caminho pelo qual se produz cópia rasa silenciosa, que é a caça ao bug 1 do semestre.

**Regra dos Três** (Cap. 9): Classe que gerencia um recurso manualmente precisa das três operações juntas: destrutor, construtor de cópia e operador de atribuição por cópia. A forma curta de cumpri-la é declarar as duas operações de cópia `= delete`, e ela cabe quando o recurso é único por natureza, como o terminal.

**Replay determinístico** (Cap. 16): Semente fixa e roteiro gravado produzem despejo idêntico byte a byte, o que dá o oráculo com que se afirma que uma refatoração não alterou o comportamento observável. Ele preserva inclusive o defeito, e é essa indiferença que o torna oráculo de refatoração, e o que o distingue do teste unitário.

**Semântica de movimento** (Cap. 14): Transferência de recurso em lugar de cópia. O `std::move` não move nada por si: ele muda a categoria de valor do argumento, de forma que a sobrecarga escolhida seja a que rouba o recurso. A origem permanece em estado **válido mas não-especificado**, que não é necessariamente vazio, e a otimização de string curta é o caso em que isso se percebe.

**`shared_ptr`** (Cap. 13): Ponteiro inteligente de posse compartilhada, com contagem de referências; libera o objeto quando a última cópia é destruída. Dois objetos que se apontam formam um ciclo que nunca é liberado, e no Deriva ele prende 160 bytes, medidos.

**Singleton** (Cap. 25): Padrão que garante uma única instância com ponto de acesso global. A forma correta em C++ é a variável `static` local na função de acesso. Traz quatro custos: estado global entre testes, dependência implícita na assinatura, impossibilidade de injetar substituto, e dado compartilhado entre threads.

**SOLID** (Cap. 24): Cinco princípios de projeto orientado a objetos: SRP, OCP, LSP, ISP e DIP. Nenhum deles diz como saber se a refatoração foi correta, e é o replay que responde a isso.

**SRP** (Cap. 24): *Single Responsibility Principle*: uma classe deve ter apenas um motivo para mudar. A formulação por motivo é mais útil que a por "faz uma coisa só", porque é verificável: pergunte quem pede a mudança.

**`std::clamp`** (Cap. 21): Função de C++17 que devolve o valor limitado a um intervalo. Substitui o par `min`/`max` aninhado, e devolve **referência**: ligar o resultado a uma referência quando um dos limites é temporário produz referência pendurada.

**`std::filesystem`** (Cap. 20): Biblioteca de C++17 para caminhos e consulta ao sistema de arquivos. Cada função tem duas formas, uma que lança e outra que recebe um `std::error_code`, e quem escolhe é o chamador. Verificar a existência e abrir são duas operações, e a corrida entre elas é real.

**`std::optional`** (Caps. 9 e 20): Tipo de C++17 que modela **ausência de resultado**, e não falha. `mapa::carregar` o devolve: arquivo inexistente é ausência; permissão negada é exceção. `value()` lança quando vazio, e `operator*` não verifica.

**`std::string_view`** (Cap. 3): Tipo de C++17 que enxerga uma sequência de caracteres sem possuí-la. Um `string_view` guardado além da vida da `string` de origem fica pendurado, e o compilador não avisa.

**`std::variant`** (Cap. 20): Tipo de C++17 que armazena exatamente um de vários tipos possíveis, consultado com `std::visit`, que cobra o tratamento de todas as alternativas em compilação. Serve a resultado **ou** erro, quando o motivo da falha importa e lançar seria pesado demais.

**Strategy** (Cap. 25): Padrão que encapsula algoritmos intercambiáveis, de forma que o contexto não saiba qual está em uso. Em C++ moderno a mecânica é a lambda, e não a hierarquia: uma operação e nenhum estado é função. Command, que tem duas operações e estado, continua sendo classe.

**Template** (Cap. 19): Mecanismo de C++ para código genérico parametrizado por tipo, instanciado pelo compilador uma vez para cada tipo usado de fato. Cada instanciação é uma classe distinta, e é por isso que `contador_de_instancias<mapa>` e `contador_de_instancias<terminal_bruto>` têm variáveis estáticas separadas.

**`this`** (Cap. 7): Ponteiro implícito dentro de todo método não-estático, que aponta para o objeto sobre o qual o método foi chamado. Os dois usos que o Deriva tem estão no operador de atribuição: a guarda `if (this != &o)` e o `return *this`.

**`typeid`** (Cap. 18): Operador de RTTI que devolve informação de tipo em execução; para que o tipo dinâmico seja consultado, a classe precisa ter pelo menos uma função virtual.

**UML** (Cap. 6): *Unified Modeling Language*: notação gráfica para modelagem de software, usada nesta disciplina em diagramas de classes e de sequência do Deriva.

**UndefinedBehaviorSanitizer (UBSan)** (Cap. 2): Instrumentação que detecta comportamento indefinido em execução: estouro de inteiro, desreferência de nulo, desalinhamento. Como o ASan, é ferramenta de aula e não portão de aceitação nesta disciplina.

**`unique_ptr`** (Cap. 12): Ponteiro inteligente de posse exclusiva; não é copiável, apenas movível, e não custa espaço em relação ao ponteiro cru. Posse exclusiva torna certos defeitos impossíveis de construir, e é por isso que o Composite do Cap. 25 a usa: um item não pode estar em dois lugares, logo não há ciclo.

**Variante deliberadamente quebrada** (Anexo C): Cópia de uma versão do Deriva com um defeito plantado, plausível, e com a propriedade que decide tudo: o compilador não avisa. Elas ensinam que o portão de compilação é necessário e não suficiente.

**`virtual`** (Cap. 11): Palavra-chave que indica que um método pode ser sobrescrito em classes derivadas e é resolvido em tempo de execução através da vtable.

**vtable e `vptr`** (Cap. 11): A vtable é a tabela de ponteiros para funções virtuais que o compilador gera para cada classe polimórfica; o `vptr` é o ponteiro para ela, que passa a ser o primeiro campo de cada objeto. São 8 bytes por **objeto**, e não por classe, aferidos por `static_assert` em `include/deriva/leiaute.hpp`.

**`weak_ptr`** (Cap. 13): Ponteiro inteligente observador, que não incrementa a contagem de referências; usado para quebrar ciclos e para verificar, antes de notificar, se o observado ainda existe.
