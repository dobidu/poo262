/* =============================================================
   POO v2 · pecas-extra.js
   As três peças que o plano v2 acrescentou aos seis originais
   (PLANO-MATERIAL §5):

     7 · expansor de compilação e template
     8 · revisor com rubrica
     9 · corrida de dados  (reaproveitada de LPII, legenda trocada)

   Mesmo contrato, mesmo motor: dobra pura de (cenário, passo),
   sem autoplay, sem Math.random, com fallback no último passo.
   ============================================================= */
(function () {
  "use strict";
  var P = window.POO, c = P.caixa, esc = P.esc;

  /* ===========================================================
     7 · EXPANSOR DE COMPILAÇÃO E TEMPLATE
     Duas perguntas na mesma peça, porque são a mesma confusão:
     "em que etapa este erro aparece?" e "o que o compilador
     realmente gerou?".
     =========================================================== */
  var ETAPAS = [
    ["pré-processador", "cpp", "inclui cabeçalho e expande macro, sem conhecer tipo nenhum ainda"],
    ["compilação", "g++ -c", "verifica tipos, instancia template, e emite o .o desta unidade"],
    ["montagem", "as", "traduz para código de máquina; erro aqui é raro, e raramente é seu"],
    ["ligação", "ld", "resolve símbolo entre os .o, e é aqui que definição ausente aparece"]
  ];

  var EXP = {
    ligador: {
      rot: "DECLAROU, NÃO DEFINIU", tipo: "falha", n: 4,
      fonte: [
        "// entidade.hpp",
        "struct entidade {",
        "  virtual ~entidade();        // declarado",
        "  virtual void desenhar() const = 0;",
        "};",
        "// entidade.cpp - o ~entidade() nunca foi definido"
      ],
      falha_em: 4,
      erro: "undefined reference to `vtable for entidade'",
      dica: "um destrutor virtual declarado e nunca definido derruba a vtable inteira"
    },
    definido: {
      rot: "DEFINIÇÃO NO LUGAR", tipo: "ok", n: 4,
      fonte: [
        "// entidade.hpp",
        "struct entidade {",
        "  virtual ~entidade();",
        "  virtual void desenhar() const = 0;",
        "};",
        "// entidade.cpp",
        "entidade::~entidade() = default;   // definido"
      ],
      falha_em: 0,
      erro: null,
      dica: "uma linha no .cpp, e a vtable passa a ter onde morar"
    },
    poda: {
      rot: "if constexpr PODA O RAMO", tipo: "ok", n: 3,
      fonte: [
        "template <class T>",
        "void grade<T>::despejar() const {",
        "  if constexpr (std::is_integral_v<T>)",
        "    std::cout << int(v);      // T = int   → FICA",
        "  else",
        "    std::cout << v.glifo();   // T = celula → DESCARTADO",
        "}",
        "// instanciado com T = int"
      ],
      falha_em: 0,
      erro: null,
      dica: "o ramo descartado não precisa nem ser compilado para T = int"
    }
  };

  P.registrar("expansor", {
    titulo: "EXPANSOR DE COMPILAÇÃO",
    nota: "cpp → g++ -c → as → ld",
    cenarios: [
      { id: "ligador", rotulo: "ERRO SÓ NA LIGAÇÃO", tipo: "falha" },
      { id: "definido", rotulo: "DEFINIÇÃO NO LUGAR", tipo: "ok" },
      { id: "poda", rotulo: "if constexpr PODA", tipo: "ok" }
    ],
    passos: function (cen) { return EXP[cen].n; },
    quadro: function (cen, i) {
      var d = EXP[cen];
      var poda = cen === "poda";

      var fonte = d.fonte.map(function (l, k) {
        var descartado = poda && i >= 3 && k === 5;
        var mantido = poda && i >= 3 && k === 3;
        var cor = descartado ? "var(--fantasma)" : mantido ? "var(--ok)" : "var(--leitura)";
        return '<div style="color:' + cor + (descartado ? ";text-decoration:line-through" : "") +
          '">' + esc(l) + "</div>";
      }).join("");

      var etapas;
      if (poda) {
        var passos = [
          ["template lido", "o corpo ainda não é código: é um molde, sem T concreto"],
          ["substituição de T", "T = int, e std::is_integral_v<int> vale true"],
          ["poda do ramo", "o ramo else é DESCARTADO, e não apenas deixado sem executar"]
        ];
        etapas = passos.map(function (p, k) {
          var aceso = i >= k + 1;
          return c({
            cab: p[0].toUpperCase(),
            realce: aceso ? (k === 2 ? "ok" : "1") : "",
            corpo: '<div style="color:' + (aceso ? "var(--leitura)" : "var(--fantasma)") +
              '">' + esc(p[1]) + "</div>",
            estilo: "flex:1 1 190px"
          });
        }).join('<span class="seta">──▶</span>');
      } else {
        etapas = ETAPAS.map(function (e, k) {
          var aceso = i >= k + 1;
          var quebra = d.falha_em === k + 1 && i >= k + 1;
          return c({
            cab: e[0].toUpperCase(), cabDir: e[1],
            realce: quebra ? "falha" : (aceso ? "1" : ""),
            corpo: '<div style="color:' + (aceso ? "var(--leitura)" : "var(--fantasma)") + '">' +
              esc(e[2]) + "</div>" +
              (quebra ? '<div style="color:var(--falha);margin-top:4px">▲ ' + esc(d.erro) + "</div>"
                      : (aceso ? '<div style="color:var(--ok);margin-top:4px">✓ passou</div>' : "")),
            estilo: "flex:1 1 165px"
          });
        }).join('<span class="seta" data-t="' + (d.falha_em ? "falha" : "") + '">──▶</span>');
      }

      var est = poda ? [
        ["instanciação", i >= 2 ? "<b>grade&lt;int&gt;</b>" : " - nenhuma ainda"],
        ["is_integral_v&lt;T&gt;", i >= 2 ? '<span class="bom">true</span>' : " - "],
        ["ramo mantido", i >= 3 ? '<span class="bom">std::cout &lt;&lt; int(v)</span>' : " - "],
        ["ramo descartado", i >= 3 ? '<span class="morto">v.glifo()</span> - nem chega a ser compilado' : " - "],
        ["por que não serve um if comum", "um <code>if</code> comum exigiria que <b>as duas</b> chamadas fossem válidas para T"],
        ["binário gerado", i >= 3 ? "um só ramo - nenhum teste em execução" : " - "]
      ] : [
        ["etapa", i === 0 ? " - " : esc(ETAPAS[i - 1][0]) + " (" + ETAPAS[i - 1][1] + ")"],
        ["unidade de tradução", i >= 1 ? "entidade.cpp + entidade.hpp" : " - "],
        ["símbolos pendentes", (i >= 2 && d.falha_em)
          ? '<span class="aviso">vtable for entidade</span>'
          : (i >= 2 ? '<span class="bom">nenhum</span>' : " - ")],
        ["erro", (d.falha_em && i >= d.falha_em)
          ? '<span class="aviso">▲ ' + esc(d.erro) + "</span>"
          : (i >= 4 ? '<span class="bom">✓ nenhum - binário ligado</span>' : " - ")],
        ["em que etapa aparece", d.falha_em
          ? "<b>ligação</b> - três etapas depois de onde está a causa"
          : " - "],
        ["o que o compilador avisou antes", d.falha_em
          ? '<span class="aviso">nada. -Wall -Wextra -Wpedantic ficam calados</span>'
          : '<span class="bom">nada a avisar</span>']
      ];

      return {
        palco: '<div class="fila" style="align-items:flex-start">' +
          c({ cab: poda ? "TEMPLATE" : "FONTE", cabDir: poda ? "grade<T>" : "entidade",
              corpo: fonte, estilo: "flex:1 1 100%" }) +
          "</div>" +
          '<div class="fila" style="align-items:stretch">' + etapas + "</div>",
        estado: est,
        legenda: i === 0
          ? (poda
            ? "Avance e observe qual das duas linhas desaparece do código gerado. O ramo que if constexpr descarta não fica apenas sem executar: ele não chega a ser compilado para este T, e por isso pode conter chamada que o tipo nem oferece."
            : "Avance uma etapa por vez e repare em qual delas o erro aparece, porque a distância entre a causa, escrita no cabeçalho, e a mensagem, emitida pelo ld, é o que faz erro de ligação parecer sem explicação.")
          : (poda
            ? (i >= 3
              ? "Com T = int, is_integral_v vale true, o ramo else é descartado, e v.glifo() nunca precisa existir para inteiro. Um if comum exigiria que as duas chamadas fossem válidas, de forma que o mesmo template deixaria de compilar tanto para int quanto para celula."
              : "Ainda é molde: nada aqui foi verificado contra um T concreto, e nenhuma linha de código de máquina existe.")
            : (d.falha_em && i >= d.falha_em
              ? "O erro aparece na ligação, porém a causa está no cabeçalho, três etapas antes: " + esc(d.dica) + ". Nenhum aviso de compilação apontou para aquela linha."
              : esc(ETAPAS[i - 1][2]) + "."))
      };
    }
  });

  /* ===========================================================
     8 · REVISOR COM RUBRICA
     Um trecho que um modelo produz para "uma hierarquia de
     entidades com inventário". Plausível, compila, passa nos
     testes que o próprio modelo escreveu - e tem três defeitos.
     Cada item da rubrica acende o seu.
     =========================================================== */
  var CODIGO_GERADO = [
    "struct entidade {",
    "  entidade(std::string nome) : nome_(nome) {}",
    "  ~entidade() { }                       // R2",
    "  virtual void desenhar() { }",
    "  std::string nome() { return nome_; }  // R3",
    "  std::vector<item*> itens;             // R1",
    "protected:",
    "  std::string nome_;",
    "};",
    "",
    "struct sonda : entidade {",
    "  sonda(std::string n) : entidade(n) {}",
    "  ~sonda() { for (auto* i : itens) delete i; }  // R1 R2",
    "  void desenhar() override { }",
    "};",
    "",
    "TEST_CASE(\"sonda tem nome\") {",
    "  sonda s(\"s-01\");",
    "  REQUIRE(s.nome() == \"s-01\");        // R7",
    "}"
  ];
  var CODIGO_REVISTO = [
    "struct entidade {",
    "  explicit entidade(std::string_view nome) : nome_(nome) {}",
    "  virtual ~entidade() = default;                    // R2 ✓",
    "  virtual void desenhar() const = 0;                // R6 ✓",
    "  [[nodiscard]] std::string_view nome() const {     // R3 ✓",
    "    return nome_;",
    "  }",
    "  std::vector<std::unique_ptr<item>> itens;         // R1 ✓",
    "protected:",
    "  std::string nome_;",
    "};",
    "",
    "struct sonda final : entidade {",
    "  using entidade::entidade;",
    "  // sem destrutor: regra do zero                   // R4 ✓",
    "  void desenhar() const override { }",
    "};",
    "",
    "TEST_CASE(\"deletar por entidade* destrói a derivada\") {",
    "  {  std::unique_ptr<entidade> e = std::make_unique<sonda>(\"s-01\");  }",
    "  REQUIRE(entidade::vivos == 0);                    // R7 ✓",
    "}"
  ];
  var ITENS = [
    ["R1", "Posse", "contêiner público com posse; `delete` no código do estudante; `shared_ptr` onde bastava `unique_ptr`",
      [5, 12]],
    ["R2", "Operações especiais", "destrutor declarado e cópia esquecida - cópia rasa silenciosa",
      [2, 12]],
    ["R3", "const-correctness", "getter não-const; retorno ignorado sem `[[nodiscard]]`",
      [4]],
    ["R4", "Limites e ausência", "índice sem verificação e sem pré-condição escrita; -1 como \"não achei\"",
      [1]],
    ["R5", "Hierarquia", "hierarquia sem `~base()` virtual - o teste passa e o objeto vaza, e com `unique_ptr` nem aviso aparece",
      [2, 12]],
    ["R6", "Invariante e estado", "campo público mutável; `assert(origem.empty())` depois do move",
      [3]],
    ["R7", "Prova e justificativa", "teste que afirma detalhe interno; função de C++20 chamada como se fosse C++17; nenhuma justificativa escrita",
      [17, 18]],
  ];

  P.registrar("revisor", {
    titulo: "REVISOR COM RUBRICA",
    nota: "7 itens · 3 defeitos que passam nos testes",
    cenarios: [
      { id: "gerado", rotulo: "COMO A IA ENTREGOU", tipo: "falha" },
      { id: "revisto", rotulo: "DEPOIS DA RUBRICA", tipo: "ok" }
    ],
    passos: function () { return ITENS.length; },
    quadro: function (cen, i) {
      var gerado = cen === "gerado";
      var fonte = gerado ? CODIGO_GERADO : CODIGO_REVISTO;
      var acesas = {};
      ITENS.slice(0, i).forEach(function (it) {
        if (gerado) it[3].forEach(function (l) { acesas[l] = it[0]; });
      });

      var linhas = fonte.map(function (l, k) {
        var marca = acesas[k];
        return '<div' + (marca ? ' style="background:var(--falha-lav);box-shadow:inset 3px 0 0 var(--falha)"' : "") +
          '><span style="color:var(--fantasma)">' + String(k + 1).padStart(2, "0") + "</span>  " +
          '<span style="color:' + (marca ? "var(--leitura)" : gerado ? "var(--apagado)" : "var(--leitura)") + '">' +
          esc(l) + "</span>" +
          (marca ? '<span style="color:var(--falha)">   ◀ ' + marca + "</span>" : "") + "</div>";
      }).join("");

      var check = ITENS.map(function (it, k) {
        var visto = k < i;
        var achou = visto && gerado;
        return '<div style="color:' + (visto ? (achou ? "var(--falha)" : "var(--ok)") : "var(--fantasma)") + '">' +
          (visto ? (achou ? "▲" : "✓") : "·") + " " + it[0] + " " + esc(it[1]) +
          (visto ? '<div style="color:var(--apagado);padding-left:1.6em">' +
            (achou ? it[2] : "atendido") + "</div>" : "") + "</div>";
      }).join("");

      var achados = gerado ? i : 0;
      return {
        palco: '<div class="fila" style="align-items:flex-start">' +
          c({ cab: gerado ? "CÓDIGO GERADO" : "CÓDIGO REVISTO",
              cabDir: gerado ? "compila · 1 teste verde" : "compila · 2 testes verdes",
              realce: gerado && i > 0 ? "falha" : (gerado ? "" : "ok"),
              corpo: linhas, estilo: "flex:1 1 420px" }) +
          c({ cab: "RUBRICA", cabDir: i + " / 7 aplicados",
              corpo: check, estilo: "flex:1 1 300px" }) +
          "</div>",
        estado: [
          ["itens aplicados", i + " de 7"],
          ["defeitos encontrados", achados
            ? '<span class="aviso">' + achados + "</span>"
            : (gerado ? " - comece pelo R1" : '<span class="bom">0</span>')],
          ["compila", '<span class="bom">✓ sim, sem warning</span>'],
          ["testes do próprio modelo", gerado
            ? '<span class="aviso">✓ verdes - e nenhum deles toca no que importa</span>'
            : '<span class="bom">✓ verdes, e um deles falharia antes da correção</span>'],
          ["entidade::vivos no fim", gerado
            ? '<span class="aviso">▲ 1 - ~sonda() não rodou</span>'
            : '<span class="bom">0</span>'],
          ["o que a revisão custou", gerado ? " - " : "sete linhas trocadas e um teste novo"]
        ],
        legenda: i === 0
          ? "Este trecho compila sem um único aviso e passa no teste que veio junto com ele. Aplique a rubrica item por item e conte quantas linhas acendem, porque em revisão de código gerado a pergunta nunca foi se aquilo roda."
          : (gerado
            ? (i >= 7
              ? "Sete itens aplicados, e os defeitos se concentram em duas linhas: o destrutor não virtual da base e a posse crua no vector. O teste que acompanhava o código não tinha como alcançar nenhum dos dois, porque afirmava o que já se sabia, e é assim que entidade::vivos termina em 1."
              : "R" + i + " · " + ITENS[i - 1][1] + ". Repare que a linha acesa não tem nada de estranho à primeira vista: é código plausível, escrito na convenção que todo mundo reconhece, e passa em revisão apressada exatamente por isso.")
            : "Depois da rubrica: destrutor virtual na base, posse em unique_ptr, desenhar() puramente virtual, regra do zero na derivada, e um teste que falharia na versão anterior. Troque o cenário e compare linha por linha, porque a diferença inteira cabe em sete linhas.")
      };
    }
  });

  /* ===========================================================
     9 · CORRIDA DE DADOS - reaproveitada de LPII
     Mesma peça, legenda trocada: aqui o contador é `vivos`, o
     mesmo da Aula 07, e a corrida acontece porque duas threads
     do Deriva (entrada e render) criam entidades ao mesmo tempo.
     =========================================================== */
  var CORRIDA = [
    ["A", "lê vivos", 0],
    ["B", "lê vivos", 0],
    ["A", "soma 1", 1],
    ["B", "soma 1", 1],
    ["A", "escreve vivos", 1],
    ["B", "escreve vivos", 1]
  ];

  P.registrar("corrida", {
    titulo: "CORRIDA DE DADOS",
    nota: "vivos++ em duas threads · reaproveitado de LPII",
    cenarios: [
      { id: "sem", rotulo: "SEM mutex", tipo: "falha" },
      { id: "com", rotulo: "COM lock_guard", tipo: "ok" }
    ],
    passos: function (cen) { return cen === "sem" ? 6 : 6; },
    quadro: function (cen, i) {
      var protegido = cen === "com";
      var vivos = 0, regA = null, regB = null, log = "", esperado = 0;

      /* com mutex, a intercalação some: A completa antes de B começar */
      var seq = protegido
        ? [["A", "trava", null], ["A", "vivos = 0 + 1", 1], ["A", "destrava", 1],
           ["B", "trava", 1], ["B", "vivos = 1 + 1", 2], ["B", "destrava", 2]]
        : CORRIDA;

      for (var k = 0; k < i; k++) {
        var p = seq[k];
        if (!protegido) {
          if (p[1] === "lê vivos") { if (p[0] === "A") regA = vivos; else regB = vivos; }
          if (p[1] === "soma 1") { if (p[0] === "A") regA += 1; else regB += 1; }
          if (p[1] === "escreve vivos") { vivos = p[0] === "A" ? regA : regB; }
        } else if (p[2] !== null) {
          vivos = p[2];
        }
        var cor = p[0] === "A" ? "var(--fosforo)" : "var(--frio)";
        log += '<div style="color:' + cor + '">' + String(k + 1).padStart(2, "0") +
          "  thread " + p[0] + "  " + esc(p[1]) + "</div>";
      }
      esperado = i >= 6 ? 2 : (i >= 3 ? 1 : 0);
      var perdeu = !protegido && i >= 6 && vivos < 2;

      function thread(nome, reg, cor) {
        return c({
          cab: "THREAD " + nome, cabDir: protegido ? "serializada" : "livre",
          realce: perdeu && nome === "A" ? "falha" : "",
          corpo: '<div style="color:' + cor + '">registrador: ' +
            (reg === null ? " - " : reg) + "</div>" +
            '<div style="color:var(--fantasma)">' +
            (protegido ? "espera o mutex" : "não espera por ninguém") + "</div>"
        });
      }

      return {
        palco: '<div class="fila" style="align-items:flex-start">' +
          c({ cab: "INTERCALAÇÃO", corpo: log || '<div style="color:var(--fantasma)"> - </div>',
              estilo: "flex:1 1 330px" }) +
          '<div class="col" style="flex:1 1 260px">' +
            thread("A", protegido ? null : regA, "var(--fosforo)") +
            thread("B", protegido ? null : regB, "var(--frio)") +
            c({ cab: "entidade::vivos", cabDir: "compartilhado",
                realce: i >= 6 ? (perdeu ? "falha" : "ok") : "1",
                corpo: '<div style="font-size:1.5em;color:' +
                  (perdeu ? "var(--falha)" : "var(--leitura)") + '">' + vivos + "</div>" +
                  '<div style="color:var(--fantasma)">esperado: ' + esperado + "</div>" }) +
          "</div></div>",
        estado: [
          ["operação", "<code>vivos++</code> - <b>não</b> é atômica: lê, soma, escreve"],
          ["vivos", i >= 6 ? (perdeu
            ? '<span class="aviso mudou">' + vivos + "</span> - uma soma sumiu"
            : '<span class="bom">' + vivos + "</span>") : String(vivos)],
          ["esperado", String(esperado)],
          ["atualização perdida", perdeu
            ? '<span class="aviso">▲ sim - as duas threads leram 0</span>'
            : (i >= 6 ? '<span class="bom">✓ nenhuma</span>' : " - ")],
          ["como isso aparece no Deriva", "o contador <code>vivos</code> da Aula 07 não fecha "
            + "em zero, e o portão acusa <span class=\"aviso\">de vez em quando</span>"],
          ["por que é pior que um bug comum", "some sob carga leve e volta em produção; "
            + "o replay determinístico da Aula 16 <b>não</b> o reproduz"],
          ["numa corrida de verdade", "duas threads somando 100 mil cada, dez execuções em "
            + "g++ 13.3: <b>oito não perderam nada</b>, e a pior perdeu 5.547 de 200 mil. "
            + "A distribuição é a lição, não a média - medido em "
            + "<code>testes/test_corrida.cpp</code>"]
        ],
        legenda: i === 0
          ? "Avance e olhe os dois registradores, não o contador compartilhado: a corrida não nasce na escrita, ela nasce porque as duas threads leram o mesmo valor de vivos antes de qualquer uma delas escrever."
          : (protegido
            ? (i >= 6
              ? "Com lock_guard não há intercalação a observar, porque a segunda thread espera na entrada da seção crítica. O contador fecha em 2, já que cada soma leu o resultado da anterior, e o custo é a espera - aqui, o preço certo por um vivos que fecha em zero no fim de main."
              : "O mutex serializa a seção crítica, de forma que a thread B não entra enquanto A não destrava, e a intercalação deixa de ser possível.")
            : (perdeu
              ? "Duas somas e um único incremento: o contador vivos do Deriva perdeu uma entidade de vista, e o portão vai acusar contador diferente de zero no fim de main. Nenhuma das duas threads fez algo errado isoladamente, e é isso que torna a corrida difícil de achar - o defeito está na ausência de ordem entre elas, não numa linha que se possa apontar."
              : "Ainda dá tempo: se B só ler depois de A escrever, o resultado sai certo, e é por isso que este defeito desaparece justamente quando você tenta reproduzi-lo."))
      };
    }
  });
})();
