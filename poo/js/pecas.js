/* =============================================================
   POO v2 · pecas.js
   As seis peças canônicas. Cada uma é uma dobra pura:
   (cenário, passo) → { palco, estado, legenda }.
   Todo número aqui é o que g++ x86-64 realmente produz - os
   tamanhos e offsets foram escolhidos para bater com Itanium ABI,
   não para caber no desenho.
   ============================================================= */
(function () {
  "use strict";
  var P = window.POO, c = P.caixa, esc = P.esc;

  function bytes(mapa) {   /* mapa: [[qtd, tipo], ...] */
    var h = "";
    mapa.forEach(function (par) {
      for (var k = 0; k < par[0]; k++) h += '<i data-b="' + par[1] + '"></i>';
    });
    return '<div class="bytes" aria-hidden="true">' + h + "</div>";
  }

  /* ===========================================================
     1 · INSPETOR DE OBJETO - layout, padding, pilha × heap
     A ordem de declaração muda o sizeof. Isso surpreende todo
     mundo na primeira vez, e é medível.
     =========================================================== */
  var ORD = {
    ruim: [
      { n: "char glifo", t: "char", tam: 1, off: 0, pad: 3 },
      { n: "int energia", t: "int", tam: 4, off: 4, pad: 0 },
      { n: "char sigla", t: "char", tam: 1, off: 8, pad: 3 },
      { n: "int massa", t: "int", tam: 4, off: 12, pad: 0 }
    ],
    boa: [
      { n: "int energia", t: "int", tam: 4, off: 0, pad: 0 },
      { n: "int massa", t: "int", tam: 4, off: 4, pad: 0 },
      { n: "char glifo", t: "char", tam: 1, off: 8, pad: 0 },
      { n: "char sigla", t: "char", tam: 1, off: 9, pad: 2 }
    ]
  };
  P.registrar("inspetor", {
    titulo: "INSPETOR DE OBJETO",
    nota: "celula × celula_ingenua · g++ x86-64",
    cenarios: [
      { id: "ruim", rotulo: "ORDEM INGÊNUA · 16 B", tipo: "falha" },
      { id: "boa", rotulo: "AGRUPADA POR TAMANHO · 12 B", tipo: "ok" }
    ],
    passos: function (cen) { return ORD[cen].length; },
    quadro: function (cen, i) {
      var ms = ORD[cen], total = cen === "ruim" ? 16 : 12;
      var mapa = [], linhas = "";
      ms.forEach(function (m, k) {
        var viva = k < i;
        if (viva) { mapa.push([m.tam, "m"]); if (m.pad) mapa.push([m.pad, "p"]); }
        linhas += '<div style="color:' + (viva ? "var(--leitura)" : "var(--fantasma)") + '">' +
          (viva ? "✓" : " ") + " " + esc(m.n) + ";" +
          '<span style="color:var(--fantasma)">   // off ' + m.off + ", " + m.tam + " B" +
          (m.pad ? ' <span style="color:var(--falha)">+' + m.pad + " pad</span>" : "") + "</span></div>";
      });
      var usados = ms.slice(0, i).reduce(function (a, m) { return a + m.tam; }, 0);
      var pads = ms.slice(0, i).reduce(function (a, m) { return a + m.pad; }, 0);
      return {
        palco: '<div class="fila">' +
          c({ cab: "DECLARAÇÃO", corpo: linhas, estilo: "flex:1 1 320px" }) +
          c({
            cab: "MEMÓRIA (pilha)", cabDir: (usados + pads) + " / " + total + " B",
            realce: pads > 0 ? "falha" : (i === ms.length ? "ok" : ""),
            corpo: bytes(mapa.length ? mapa : [[0, "m"]]) +
              '<div style="margin-top:6px;color:var(--apagado)">' +
              '<i data-b="m" class="bytes" style="display:inline-block;width:11px;height:11px;background:var(--fosforo)"></i> membro   ' +
              '<span style="color:var(--falha)">░ padding</span></div>',
            estilo: "flex:1 1 260px"
          }) + "</div>",
        estado: [
          ["membros na declaração", i + " de " + ms.length + " declarados"],
          ["bytes úteis", "<b>" + usados + "</b> B"],
          ["padding", pads ? '<span class="aviso">' + pads + " B desperdiçados</span>" : '<span class="bom">0 B</span>'],
          [cen === "ruim" ? "sizeof(celula_ingenua)" : "sizeof(celula)", i === ms.length ? "<b>" + total + "</b> B" + (cen === "ruim" ? ' <span class="aviso">▲ 33% a mais</span>' : ' <span class="bom">✓ mínimo</span>') : " - (incompleto)"],
          ["alinhamento", "4 B (o maior membro manda)"],
          ["onde vive", "pilha - <span style=\"color:var(--fantasma)\">celula c; dentro de função</span>"]
        ],
        legenda: i === 0
          ? "Avance um membro por vez e olhe a faixa de memória, não a declaração: o compilador insere padding entre os campos para manter cada int em endereço múltiplo de 4, e esse enchimento entra no sizeof sem aparecer em nenhuma linha que você escreveu."
          : (i === ms.length
            ? (cen === "ruim"
              ? "Quatro membros, 10 bytes de dados e 16 bytes de objeto: os 6 marcados são padding, e existem apenas para que cada int comece num endereço alinhado. Troque o cenário e compare, porque o ganho vem de reordenar a declaração, sem remover um único campo."
              : "Os mesmos quatro membros, agora agrupados por tamanho, fecham em 12 bytes, com os 2 de padding empurrados para o fim do objeto. Nada mudou no significado do código, apenas a ordem em que os campos foram declarados - e é este arranjo que o static_assert de celula.hpp trava.")
            : "Cada int tem de começar num endereço múltiplo de 4, de forma que, se o membro anterior deixou o cursor em 1, o compilador pula 3 bytes até o próximo múltiplo, e aquele buraco é seu, pago no sizeof de cada célula da grade.")
      };
    }
  });

  /* ===========================================================
     2 · RASTREADOR DE CICLO DE VIDA
     Ordem exata de construção e destruição, e o desenrolar da
     pilha quando uma exceção passa por escopos com objetos.
     =========================================================== */
  var CICLO = {
    normal: [
      ["+", "mapa", "escopo 1"], ["+", "term", "escopo 1"],
      ["{", "escopo 2", ""], ["+", "sonda", "escopo 2"], ["+", "drone", "escopo 2"],
      ["}", "escopo 2", ""], ["-", "drone", "escopo 2"], ["-", "sonda", "escopo 2"],
      ["fim", "", ""], ["-", "term", "escopo 1"], ["-", "mapa", "escopo 1"]
    ],
    excecao: [
      ["+", "mapa", "escopo 1"], ["+", "term", "escopo 1"],
      ["{", "escopo 2", ""], ["+", "sonda", "escopo 2"], ["+", "drone", "escopo 2"],
      ["!", "throw std::runtime_error", ""],
      ["-", "drone", "escopo 2"], ["-", "sonda", "escopo 2"],
      ["-", "term", "escopo 1"], ["-", "mapa", "escopo 1"],
      ["catch", "", ""]
    ]
  };
  P.registrar("ciclo", {
    titulo: "CICLO DE VIDA",
    nota: "construção · destruição · desenrolar",
    cenarios: [
      { id: "excecao", rotulo: "EXCEÇÃO NO MEIO", tipo: "falha" },
      { id: "normal", rotulo: "SAÍDA NORMAL", tipo: "ok" }
    ],
    passos: function (cen) { return CICLO[cen].length; },
    quadro: function (cen, i) {
      var ps = CICLO[cen], vivos = [], log = "", lancou = false;
      ps.slice(0, i).forEach(function (p, k) {
        if (p[0] === "+") vivos.push(p[1]);
        if (p[0] === "-") vivos = vivos.filter(function (v) { return v !== p[1]; });
        if (p[0] === "!") lancou = true;
        var cor = p[0] === "+" ? "var(--ok)" : p[0] === "-" ? "var(--fosforo)" :
          p[0] === "!" ? "var(--falha)" : "var(--apagado)";
        var txt = p[0] === "+" ? "celula::celula()   " + p[1] :
          p[0] === "-" ? "celula::~celula()  " + p[1] :
          p[0] === "!" ? "▲ " + p[1] :
          p[0] === "catch" ? "✓ catch - pilha desenrolada, nenhum recurso vazou" :
          p[0] === "{" ? "{ abre " + p[1] : "} fecha " + p[1];
        log += '<div style="color:' + cor + '">' + String(k + 1).padStart(2, "0") + "  " + esc(txt) + "</div>";
      });
      var pilha = vivos.slice().reverse().map(function (v, k) {
        return '<div style="color:var(--leitura)">' + (k === 0 ? "▸" : " ") + " " + esc(v) +
          '<span style="color:var(--fantasma)"> @ 0x7ffd' + (52 - vivos.length + k).toString(16) + "8</span></div>";
      }).join("") || '<div style="color:var(--fantasma)">(vazia)</div>';
      return {
        palco: '<div class="fila">' +
          c({ cab: "PILHA (topo primeiro)", cabDir: vivos.length + " vivo(s)", realce: lancou ? "falha" : "", corpo: pilha, estilo: "flex:1 1 240px" }) +
          c({ cab: "TRAÇO", corpo: log || '<div style="color:var(--fantasma)"> - </div>', estilo: "flex:2 1 380px" }) +
          "</div>",
        estado: [
          ["objetos vivos", vivos.length ? vivos.map(esc).join(", ") : " - "],
          ["contador vivos", String(vivos.length)],
          ["exceção em voo", lancou && i < ps.length ? '<span class="aviso">sim - desenrolando</span>' : (lancou ? '<span class="bom">tratada</span>' : "não")],
          ["ordem de destruição", "inversa à de construção, sempre"],
          ["vazamento", i === ps.length ? '<span class="bom">✓ nenhum - destrutores rodaram</span>' : " - "]
        ],
        legenda: i === 0
          ? "Avance e leia a coluna da pilha, não o traço: o que se demonstra aqui é que a ordem de destruição é exatamente a inversa da de construção, e que ela vale sem que nenhuma linha do seu código tenha pedido por isso."
          : (lancou
            ? "A exceção não salta os destrutores: ao desenrolar a pilha, ela os chama um a um, de dentro para fora, até encontrar o catch. É por isso que RAII sustenta a liberação de recurso, e um delete escrito na última linha da função não sustenta - aquela linha nunca chega a ser alcançada."
            : "Cada } fecha um escopo e destrói o que nasceu dentro dele, na ordem inversa à de criação; o compilador emite tais chamadas de destrutor por você, e é sobre essa garantia que o contador vivos do Deriva consegue fechar em zero no fim de main.")
      };
    }
  });

  /* ===========================================================
     3 · DESPACHANTE VIRTUAL - vptr, vtable, estático × dinâmico
     Sem `virtual` a chamada resolve pelo tipo ESTÁTICO e vai
     para o lugar errado. Isso fica visível no glifo desenhado.
     =========================================================== */
  var TIPOS = [
    { n: "sonda", glifo: "@", vt: "vtable(sonda)", corpo: "sonda::desenhar()" },
    { n: "drone", glifo: "d", vt: "vtable(drone)", corpo: "drone::desenhar()" },
    { n: "item", glifo: "!", vt: "vtable(item)", corpo: "item::desenhar()" }
  ];
  P.registrar("virtual", {
    titulo: "DESPACHANTE VIRTUAL",
    nota: "entidade* → desenhar()",
    cenarios: [
      { id: "sem", rotulo: "SEM virtual", tipo: "falha" },
      { id: "com", rotulo: "COM virtual", tipo: "ok" }
    ],
    passos: function () { return 4; },
    quadro: function (cen, i) {
      var virt = cen === "com";
      var alvo = TIPOS[1];               /* o objeto é um drone   */
      var etapas = [
        "o ponteiro entidade* passa a apontar o drone",
        virt ? "lê o vptr, primeiro campo do objeto" : "não há vptr a ler neste objeto",
        virt ? "indexa a vtable no slot de desenhar()" : "resolve pelo tipo ESTÁTICO, entidade",
        virt ? "chama " + alvo.corpo : "chama entidade::desenhar()"
      ];
      var atual = i;
      function pass(k) { return atual >= k; }
      var vtRows = ["desenhar()", "agir()", "~entidade()"].map(function (m, k) {
        var sel = virt && pass(3) && k === 0;
        return '<div style="color:' + (sel ? "var(--fosforo-alto)" : "var(--apagado)") +
          ';background:' + (sel ? "var(--fosforo-lav)" : "transparent") + '">[' + k + "] " +
          (virt ? "drone::" : "entidade::") + esc(m) + "</div>";
      }).join("");
      var glifo = pass(4) ? (virt ? alvo.glifo : "·") : "?";
      return {
        palco: '<div class="fila" style="align-items:center">' +
          c({ cab: "CHAMADA", realce: pass(1) ? "1" : "", corpo:
            '<div style="color:var(--leitura)">entidade* e = &amp;d;</div>' +
            '<div style="color:' + (pass(1) ? "var(--fosforo)" : "var(--fantasma)") + '">e-&gt;desenhar();</div>' +
            '<div style="margin-top:6px;color:var(--fantasma)">estático: entidade<br>dinâmico: drone</div>', estilo: "flex:0 1 190px" }) +
          '<span class="seta" data-t="' + (virt ? "" : "falha") + '">──▶</span>' +
          c({ cab: "OBJETO d (drone)", cabDir: virt ? "16 B" : "8 B", realce: pass(2) && virt ? "1" : "", corpo:
            '<div style="color:' + (virt ? (pass(2) ? "var(--frio)" : "var(--apagado)") : "var(--fantasma)") + '">' +
            (virt ? "[vptr] → " + alvo.vt : "(sem vptr - classe não-polimórfica)") + "</div>" +
            '<div style="color:var(--leitura)">[pos] {4, 7}</div>', estilo: "flex:1 1 210px" }) +
          '<span class="seta" data-t="' + (virt ? "" : "falha") + '">' + (virt ? "──▶" : "┄┄▶") + "</span>" +
          c({ cab: virt ? esc(alvo.vt) : "RESOLUÇÃO ESTÁTICA", realce: pass(3) ? (virt ? "1" : "falha") : "",
            corpo: vtRows, estilo: "flex:1 1 210px" }) +
          '<span class="seta" data-t="' + (virt ? "" : "falha") + '">──▶</span>' +
          c({ cab: "SAÍDA NO TERMINAL", realce: pass(4) ? (virt ? "ok" : "falha") : "",
            corpo: '<div style="font-size:1.6em;line-height:1.2;color:' + (virt ? "var(--ok)" : "var(--falha)") + '">' +
              esc(glifo) + "</div>" +
              '<div style="color:var(--fantasma)">esperado: ' + esc(alvo.glifo) + "</div>", estilo: "flex:0 1 140px" }) +
          "</div>",
        estado: [
          ["tipo estático", "entidade*"],
          ["tipo dinâmico", "drone"],
          ["vptr", virt ? (pass(2) ? "<b>0x4a10</b> → " + esc(alvo.vt) : "não lido ainda") : '<span class="aviso">não existe - sem método virtual, sem vptr</span>'],
          ["sizeof(drone)", virt ? "16 B <span style=\"color:var(--fantasma)\">(8 do vptr + 8 da posição)</span>" : "8 B <span style=\"color:var(--fantasma)\">(só a posição)</span>"],
          ["drone com carga própria", virt ? "24 B <span style=\"color:var(--fantasma)\">(vptr 8 + pos 8 + carga 4 + padding 4) - o custo do vptr se soma, não desaparece</span>" : "12 B <span style=\"color:var(--fantasma)\">(pos 8 + carga 4)</span>"],
          ["etapa", (i === 0 ? " - " : esc(etapas[i - 1]))],
          ["função chamada", pass(4) ? (virt ? '<span class="bom">✓ drone::desenhar()</span>' : '<span class="aviso">▲ entidade::desenhar() - a base</span>') : " - "]
        ],
        legenda: i === 0
          ? "O objeto é um drone e o ponteiro é entidade*, de forma que os dois tipos discordam de propósito. Avance os quatro passos acompanhando por onde a chamada passa, e compare com o lugar onde ela chega."
          : (pass(4)
            ? (virt
              ? "Com virtual, a chamada sai do ponteiro, entra no objeto, lê o vptr, indexa a vtable no slot de desenhar() e chega em drone::desenhar(). O tipo do ponteiro serviu para alcançar o objeto, porém não decidiu qual função rodaria."
              : "Sem virtual não existe vptr no objeto, e o compilador já resolveu a chamada pelo tipo do ponteiro, ainda na compilação. O drone saiu desenhado como ·, o programa terminou com sucesso, e -Wall -Wextra -Wpedantic não disseram uma palavra.")
            : (virt ? esc(etapas[i - 1]) + ". O vptr ocupa o primeiro campo do objeto, e é por isso que sizeof(drone) sai de 8 para 16 bytes: são 8 bytes por OBJETO criado, não por classe declarada."
                    : esc(etapas[i - 1]) + ". Repare que o caminho tracejado nunca entra no objeto, porque sem método virtual não há o que consultar em tempo de execução."))
      };
    }
  });

  /* ===========================================================
     4 · COPIAR × MOVER - o estado da ORIGEM depois
     Duas afirmações erradas convivem no material herdado. O
     livro v1 ensina que a origem fica vazia. O documento de
     design ensina o contrário para string curta: que a SSO faria
     a libstdc++ deixar a origem intacta.
     Nenhuma das duas se reproduz aqui. Medido em
     exemplos/deriva/testes/test_move_string.cpp, com g++ 13 e
     libstdc++: a origem esvazia nos QUATRO casos - curta e
     longa, construção e atribuição -, porque o construtor de
     movimento termina chamando _M_set_length(0) em ambos os
     ramos.
     A lição não enfraquece, endurece: é porque
     REQUIRE(origem.empty()) PASSA aqui que o folclore sobrevive
     e o bug embarca. O que de fato distingue curta de longa é se
     algum byte foi copiado - e é esse o fato que a peça mostra,
     porque é o único que se reproduz.
     =========================================================== */
  var MOVE = {
    curta: { txt: "sonda-01", n: 8, sso: true, end: "0x7ffd4a20 (dentro do objeto)" },
    longa: { txt: "sonda-de-inspecao-orbital-01", n: 28, sso: false, end: "0x55f2a0 (heap)" }
  };
  P.registrar("move", {
    titulo: "COPIAR × MOVER",
    nota: "std::string · g++ 13 · libstdc++ · SSO até 15 ch",
    cenarios: [
      { id: "confia", rotulo: "CONFIA NO VAZIO", tipo: "falha" },
      { id: "respeita", rotulo: "TRATA COMO NÃO-ESPECIFICADO", tipo: "ok" }
    ],
    passos: function () { return 3; },
    quadro: function (cen, i) {
      var confia = cen === "confia";
      var movido = i >= 1, usado = i >= 3;

      function coluna(k) {
        var d = MOVE[k];
        var origem = movido ? "" : d.txt;
        var rotuloEnd = movido
          ? (d.sso ? "mesmo endereço, buffer interno" : "voltou ao buffer interno")
          : d.end;
        var destinoEnd = movido
          ? (d.sso ? "COPIOU " + d.n + " bytes" : "recebeu o MESMO ponteiro de heap")
          : "vazio";
        return '<div class="col" style="flex:1 1 300px">' +
          '<div style="font-family:var(--maquina);font-size:var(--t-rot);letter-spacing:.12em;color:' +
            (d.sso ? "var(--fosforo)" : "var(--frio)") + '">' +
            (d.sso ? "CURTA · 8 ch · cabe no objeto" : "LONGA · 28 ch · vai ao heap") + "</div>" +
          c({ cab: "ORIGEM  a", cabDir: "size " + (movido ? 0 : d.n),
              realce: movido ? (confia && usado ? "falha" : "1") : "",
              corpo: '<div style="color:var(--leitura)">"' + esc(origem) + '"</div>' +
                '<div style="color:var(--fantasma);margin-top:4px">' + rotuloEnd + "</div>" }) +
          '<div style="text-align:center;font-family:var(--maquina);color:' +
            (movido ? "var(--fosforo)" : "var(--fantasma)") + '">' +
            (movido ? "▼ std::move" : "│") + "</div>" +
          c({ cab: "DESTINO b", cabDir: "size " + (movido ? d.n : 0),
              realce: movido ? "ok" : "",
              corpo: '<div style="color:var(--leitura)">"' + esc(movido ? d.txt : "") + '"</div>' +
                '<div style="color:var(--fantasma);margin-top:4px">' + destinoEnd + "</div>" }) +
          "</div>";
      }

      var linhaFinal = "";
      if (usado) {
        linhaFinal = '<div style="flex:1 1 100%">' + c({
          cab: confia ? "O TESTE QUE O ESTUDANTE ESCREVE" : "O QUE O CONTRATO PERMITE",
          realce: confia ? "falha" : "ok",
          corpo: confia
            ? '<div style="color:var(--leitura)">REQUIRE(a.empty());</div>' +
              '<div style="color:var(--falha)">▲ passa. Nos dois casos, neste compilador, hoje.</div>' +
              '<div style="color:var(--fantasma)">O padrão não prometeu isso. O teste verde é o que faz o bug embarcar.</div>'
            : '<div style="color:var(--leitura)">a = "sonda-02";   a.clear();   // e nada de ler</div>' +
              '<div style="color:var(--ok)">✓ válido em qualquer implementação, hoje e depois.</div>' +
              '<div style="color:var(--fantasma)">Atribuir, destruir e chamar método sem precondição: é o contrato inteiro.</div>'
        }) + "</div>";
      }

      return {
        palco: '<div class="fila" style="align-items:flex-start">' +
          coluna("curta") + coluna("longa") + linhaFinal + "</div>",
        estado: [
          ["operação", i === 0 ? "as duas strings construídas"
            : (i === 1 ? "std::string b = std::move(a);"
                       : (i === 2 ? "onde os bytes foram parar" : "o que o código faz com a origem"))],
          ["a.size() depois", movido
            ? '<span class="mudou">0</span> nas duas <span style="color:var(--fantasma)">- medido nos 4 casos: curta e longa, construção e atribuição</span>'
            : "8 e 28"],
          ["bytes de conteúdo copiados", i >= 2
            ? 'curta <span class="aviso">8</span> · longa <span class="bom">0</span>'
            : " - "],
          ["a origem é a mesma memória?", i >= 2
            ? 'curta <b>sim</b> - não havia ponteiro a roubar · longa <b>não</b> - o ponteiro trocou de dono'
            : " - "],
          ["o que o padrão promete", '<span class="aviso">válido, mas NÃO-ESPECIFICADO</span> - nunca vazio'],
          ["o que é seguro fazer com a", 'atribuir, destruir, chamar clear() · <span class="aviso">nunca LER o valor</span>']
        ],
        legenda: i === 0
          ? "Duas strings, uma que cabe dentro do objeto e uma que não. Avance e compare o que acontece com a memória de cada uma, não com o valor que a caixa mostra."
          : (i === 1
            ? "As duas ficaram vazias, e esse é o problema: a origem esvaziar não é promessa do padrão, é escolha desta libstdc++. Avance para ver o que de fato mudou."
            : (i === 2
              ? "Aqui está a diferença que se reproduz: mover a string curta copiou oito bytes, porque não havia ponteiro a roubar; mover a longa não copiou conteúdo algum, só transferiu o dono do bloco de heap. `std::move` não move nada por conta própria - quem decide é o construtor de movimento do tipo, e ele pode legitimamente copiar."
              : (confia
                ? "O teste passa, neste compilador, hoje. É exatamente isso que faz o folclore sobreviver: quem aprendeu que o move esvazia escreve a asserção, vê verde, e embarca um código que depende de detalhe de implementação. Quebra na próxima versão da biblioteca, ou na primeira máquina com libc++."
                : "Atribuir, destruir e chamar método sem precondição são o contrato inteiro. Repare no que o cenário de falha tem de pior: ele não falha. Um teste verde sobre garantia que não existe é mais caro que um teste vermelho.")))
      };
    }
  });

  /* ===========================================================
     5 · GRAFO DE POSSE - unique_ptr, shared_ptr, o ciclo
     =========================================================== */
  var POSSE = {
    ciclo: [
      "shared_ptr<no> a = make_shared<no>(\"eclusa\");",
      "shared_ptr<no> b = make_shared<no>(\"corredor\");",
      "a->vizinho = b;   // shared_ptr",
      "b->vizinho = a;   // shared_ptr  ▲ fecha o ciclo de posse",
      "a.reset(); b.reset();   // sai de escopo"
    ],
    weak: [
      "shared_ptr<no> a = make_shared<no>(\"eclusa\");",
      "shared_ptr<no> b = make_shared<no>(\"corredor\");",
      "a->vizinho = b;   // shared_ptr",
      "b->volta = a;     // weak_ptr  ✓ não conta na posse",
      "a.reset(); b.reset();   // sai de escopo"
    ]
  };
  P.registrar("posse", {
    titulo: "GRAFO DE POSSE",
    nota: "contagem de referências ao vivo",
    cenarios: [
      { id: "ciclo", rotulo: "CICLO DE shared_ptr", tipo: "falha" },
      { id: "weak", rotulo: "weak_ptr QUEBRA O CICLO", tipo: "ok" }
    ],
    passos: function () { return 5; },
    quadro: function (cen, i) {
      var ciclo = cen === "ciclo";
      var ca = 0, cb = 0, wa = 0;
      if (i >= 1) ca = 1;
      if (i >= 2) cb = 1;
      if (i >= 3) cb += 1;
      if (i >= 4) { if (ciclo) ca += 1; else wa += 1; }
      if (i >= 5) { ca -= 1; cb -= 1; }
      var vivoA = ca > 0, vivoB = cb > 0;
      var fim = i >= 5;
      var log = POSSE[cen].slice(0, i).map(function (l, k) {
        var mau = k === 3 && ciclo, bom = k === 3 && !ciclo;
        return '<div style="color:' + (mau ? "var(--falha)" : bom ? "var(--ok)" : "var(--leitura)") + '">' +
          String(k + 1).padStart(2, "0") + "  " + esc(l) + "</div>";
      }).join("") || '<div style="color:var(--fantasma)"> - </div>';
      function no(rot, nome, use, weak, vivo) {
        return c({
          cab: rot, cabDir: vivo ? "use_count " + use : "destruído",
          realce: fim ? (vivo ? "falha" : "ok") : (use ? "1" : ""), morta: !vivo && i >= 1,
          corpo: '<div style="color:var(--leitura)">no{"' + esc(nome) + '"}</div>' +
            '<div style="color:var(--frio)">use_count = ' + use + "</div>" +
            (weak ? '<div style="color:var(--outro)">weak_count = ' + weak + "</div>" : "") +
            '<div style="color:var(--fantasma)">@ 0x55f' + (nome === "eclusa" ? "2a0" : "310") + "</div>"
        });
      }
      return {
        palco: '<div class="fila" style="align-items:flex-start">' +
          c({ cab: "CÓDIGO", corpo: log, estilo: "flex:1 1 340px" }) +
          '<div class="col" style="flex:1 1 300px">' +
            no("NÓ a", "eclusa", ca, 0, vivoA || i < 1) +
            '<div style="text-align:center;font-family:var(--maquina);color:' +
              (i >= 3 ? "var(--fosforo)" : "var(--fantasma)") + '">│ shared ▼</div>' +
            no("NÓ b", "corredor", cb, wa, vivoB || i < 2) +
            (i >= 4 ? '<div style="text-align:center;font-family:var(--maquina);color:' +
              (ciclo ? "var(--falha)" : "var(--outro)") + '">▲ ' +
              (ciclo ? "shared - ciclo fechado │" : "weak - observa sem possuir │") + "</div>" : "") +
          "</div></div>",
        estado: [
          ["a.use_count()", String(ca)],
          ["b.use_count()", String(cb) + (wa ? ' <span style="color:var(--outro)">(+ ' + wa + " weak)</span>" : "")],
          ["objetos vivos", fim ? (ciclo ? '<span class="aviso">2 - e sem ninguém apontando para eles</span>' : '<span class="bom">0</span>') : String((vivoA ? 1 : 0) + (vivoB ? 1 : 0))],
          ["vazamento", fim ? (ciclo ? '<span class="aviso">▲ 160 B presos - 2 × (64 do nó + 16 do bloco de controle)</span>' : '<span class="bom">✓ nenhum</span>') : " - "],
          ["quem destrói", "quem levar a contagem a zero - e ninguém mais"]
        ],
        legenda: i === 0
          ? "Acompanhe as duas contagens de referência, não as setas do desenho: shared_ptr não é coletor de lixo, ele destrói o objeto no instante em que a contagem chega a zero, e um ciclo garante que ela nunca chegue."
          : (fim
            ? (ciclo
              ? "Os dois shared_ptr locais saíram de escopo, porém cada nó continua segurando o outro, e as contagens param em 1 e 1. Nenhum destrutor roda, nenhum ponteiro do programa alcança mais aqueles objetos, e o processo termina com 160 bytes presos sem que o compilador ou os testes digam qualquer coisa."
              : "Trocar uma das pontas por weak_ptr fez as contagens caírem a zero em cascata, e os dois destrutores rodaram. weak_ptr observa sem possuir, e é a partir dessa distinção que se decide qual aresta do grafo pode ser de posse.")
            : (i === 4 && ciclo
              ? "Esta linha é a causa do vazamento, e ela executa quatro passos antes de o vazamento existir. Avance e observe o momento em que a contagem deixa de poder cair."
              : "Cada shared_ptr novo que passa a apontar um nó incrementa a contagem daquele nó, e cada um que morre a decrementa."))
      };
    }
  });

  /* ===========================================================
     6 · DIFERENCIADOR DE REFATORAÇÃO - acoplamento como grafo
     =========================================================== */
  var REF = {
    antes: {
      nos: [["mundo", 6, "god class"], ["render", 0, ""], ["entrada", 0, ""], ["arquivo", 0, ""], ["ia", 0, ""], ["log", 0, ""], ["spawn", 0, ""]],
      arestas: 6, motivos: "render, entrada, arquivo, IA, log e spawn",
      srp: false
    },
    depois: {
      nos: [["mundo", 2, "só estado do domínio"], ["i_render", 0, "interface"], ["i_entrada", 0, "interface"], ["render_tui", 0, ""], ["render_qt", 0, ""], ["comando", 0, ""], ["observador", 0, ""]],
      arestas: 2, motivos: "duas interfaces, e nada além delas",
      linhas: 168, srp: true
    }
  };
  P.registrar("refator", {
    titulo: "DIFERENCIADOR DE REFATORAÇÃO",
    nota: "SOLID · v2.6-antes → v2.6",
    cenarios: [
      { id: "antes", rotulo: "v2.6-antes · GOD CLASS", tipo: "falha" },
      { id: "depois", rotulo: "v2.6 · SOLID", tipo: "ok" }
    ],
    passos: function () { return 4; },
    quadro: function (cen, i) {
      var d = REF[cen], antes = cen === "antes";
      var vis = d.nos.slice(0, Math.max(1, Math.ceil(d.nos.length * (i / 4))));
      var nos = vis.map(function (n, k) {
        var hub = k === 0;
        return c({
          cab: esc(n[0]), cabDir: n[2] ? esc(n[2]) : "",
          realce: hub ? (antes ? "falha" : "ok") : "",
          corpo: '<div style="color:var(--fantasma)">' +
            (hub ? "depende de " + n[1] : "depende de 0") + "</div>",
          estilo: "flex:0 1 " + (hub ? "180px" : "140px")
        });
      }).join("");
      return {
        palco: '<div class="fila">' + nos + "</div>" +
          '<div style="font-family:var(--maquina);font-size:var(--t-rot);color:' +
          (antes ? "var(--falha)" : "var(--ok)") + ';letter-spacing:.1em">' +
          (antes ? "▲ tudo passa por mundo - " : "✓ mundo conhece ") + esc(d.motivos) + "</div>",
        estado: [
          ["classes", String(d.nos.length) + ' <span style="color:var(--fantasma)"> - igual nos dois cenários</span>'],
          ["dependências de saída do nó central", antes ? '<span class="aviso">' + d.arestas + "</span>" : '<span class="bom">' + d.arestas + "</span>"],
          ["motivos para mudar mundo", antes ? '<span class="aviso">6 - viola SRP</span>' : '<span class="bom">1</span>'],
          ["trocar a TUI pelo Qt exige", antes ? '<span class="aviso">editar mundo.cpp</span>' : '<span class="bom">uma nova classe - mundo não muda</span>'],
          ["padrões aplicados", antes ? " - " : "Command, State, Observer, Factory, Strategy, Composite"]
        ],
        legenda: i === 0
          ? "Avance para revelar as classes e, em vez de contar quantas são, conte quantas dependências saem do nó central: é esse grau de saída que diz se o desenho aguenta a Aula 26, quando um segundo front-end entra no sistema."
          : (antes
            ? "Seis motivos independentes para editar o mesmo arquivo, o que é a definição operacional de violar o SRP. Quando o Qt entrar como segundo front-end, ele entra dentro desta classe, e a separação entre domínio e interface deixa de existir na prática, por mais que continue desenhada no diagrama."
            : "Sete classes antes e sete depois, porque o total nunca foi a métrica: o que caiu de 6 para 2 foi o grau de saída do nó central. É a partir dessa queda que render_tui e render_qt passam a ser irmãos sobre a mesma interface, com o núcleo do domínio sem saber qual dos dois está montado.")
      };
    }
  });
})();
