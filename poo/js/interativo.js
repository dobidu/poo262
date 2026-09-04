/* =============================================================
   POO v2 · interativo.js
   O MOTOR e a MOLDURA (T2). Os oito interativos não repetem
   estrutura: registram uma peça e ganham moldura, controles,
   painel de estado, legenda, teclado e fallback estático.

   Contrato de peça - herdado da spec de LPII e obrigatório:
     titulo      rótulo embutido na moldura superior
     cenarios[]  { id, rotulo, tipo: "falha" | "ok" }  (≥1 de cada)
     passos(cen) quantos passos o cenário tem
     quadro(cen, i) -> { palco, estado: [[rótulo, html]], legenda }

   Regras que o motor garante, para nenhuma peça poder violá-las:
   · estado é FUNÇÃO de (cenário, passo) - dobra pura, sem mutação
     acumulada e sem Math.random: voltar é exato, não animação
     reversa;
   · nunca há autoplay nem botão de play - o passo é do aluno;
   · prefers-reduced-motion desenha o ÚLTIMO passo, com todo o
     estado presente: nenhuma informação depende de movimento.
   ============================================================= */
(function () {
  "use strict";

  var API = (window.POO = window.POO || {});
  var pecas = {};

  /* moldura de box-drawing: caracteres reais, título embutido -- */
  API.moldura = function (titulo, nota, opc) {
    opc = opc || {};
    var e = opc.arredondada;
    var base = opc.base;
    var ce = base ? (e ? "╰" : "└") : (e ? "╭" : "┌");
    var cd = base ? (e ? "╯" : "┘") : (e ? "╮" : "┐");
    var t = titulo
      ? '<span class="moldura__canto">─┤</span>' +
        '<span class="moldura__titulo">' + titulo + '</span>' +
        '<span class="moldura__canto">├</span>'
      : "";
    var n = nota ? '<span class="moldura__nota">┤ ' + nota + ' ├</span>' : "";
    var regua = '<span class="moldura__regua" aria-hidden="true">' + new Array(120).join("─") + "</span>";
    return '<div class="moldura' + (opc.sistema ? " moldura--sistema" : "") + '" aria-hidden="true">' +
      '<span class="moldura__canto">' + ce + "─</span>" + t + regua + n +
      '<span class="moldura__canto">─' + cd + "</span></div>";
  };

  API.registrar = function (slug, peca) { pecas[slug] = peca; };

  /* utilitários que as peças usam para desenhar o palco -------- */
  API.esc = function (s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  };
  API.caixa = function (o) {
    return '<div class="caixa"' +
      (o.realce ? ' data-realce="' + o.realce + '"' : "") +
      (o.morta ? ' data-morta="1"' : "") +
      (o.estilo ? ' style="' + o.estilo + '"' : "") + ">" +
      (o.cab ? '<div class="caixa__cab"><span>' + o.cab + "</span>" +
        (o.cabDir ? "<span>" + o.cabDir + "</span>" : "") + "</div>" : "") +
      '<div class="caixa__corpo">' + o.corpo + "</div></div>";
  };

  function montar(raiz) {
    var slug = raiz.getAttribute("data-int");
    var peca = pecas[slug];
    if (!peca) { return; }

    var reduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var cen = peca.cenarios[0].id;
    var i = 0;

    raiz.classList.add("interativo");
    raiz.setAttribute("role", "group");
    raiz.setAttribute("aria-label", "Exemplo interativo: " + peca.titulo);

    raiz.innerHTML =
      API.moldura(peca.titulo, peca.nota || null, { sistema: true }) +
      '<div class="int__palco" data-palco></div>' +
      '<div class="int__controles">' +
        '<div class="grupo">' +
          '<button class="bt" type="button" data-a="volta" aria-label="Passo anterior">◀ VOLTA</button>' +
          '<button class="bt bt--primario" type="button" data-a="passo">PASSO ▶</button>' +
          '<button class="bt" type="button" data-a="reinicia" aria-label="Reiniciar" title="Reiniciar (R)">↺</button>' +
        "</div>" +
        '<div class="cenarios" role="group" aria-label="Cenário">' +
          '<span class="cenarios__rot">CENÁRIO</span>' +
          peca.cenarios.map(function (c) {
            return '<button class="cen" type="button" data-cen="' + c.id + '" data-t="' + c.tipo +
              '" aria-pressed="false">' + (c.tipo === "falha" ? "▲" : "✓") + " " + c.rotulo + "</button>";
          }).join("") +
        "</div>" +
        '<div class="medidor"><span>PASSO <b data-passo>0</b></span></div>' +
      "</div>" +
      '<div class="int__estado" data-estado aria-live="polite"></div>' +
      '<div class="int__legenda"><span class="rot">ONDE OLHAR</span><p data-legenda></p></div>' +
      API.moldura(null, null, { sistema: true, base: true });

    var elPalco = raiz.querySelector("[data-palco]");
    var elEstado = raiz.querySelector("[data-estado]");
    var elLegenda = raiz.querySelector("[data-legenda]");
    var elPasso = raiz.querySelector("[data-passo]");
    var btVolta = raiz.querySelector('[data-a="volta"]');
    var btPasso = raiz.querySelector('[data-a="passo"]');

    function pintar() {
      var n = peca.passos(cen);
      var q = peca.quadro(cen, i);
      elPalco.innerHTML = q.palco;
      elEstado.innerHTML = "<table><tbody>" + q.estado.map(function (l) {
        return "<tr><th>" + l[0] + "</th><td>" + l[1] + "</td></tr>";
      }).join("") + "</tbody></table>";
      elLegenda.textContent = q.legenda;
      elPasso.textContent = i + " / " + n;
      btVolta.setAttribute("aria-disabled", i === 0 ? "true" : "false");
      btPasso.setAttribute("aria-disabled", i >= n ? "true" : "false");
      Array.prototype.forEach.call(raiz.querySelectorAll("[data-cen]"), function (b) {
        b.setAttribute("aria-pressed", b.getAttribute("data-cen") === cen ? "true" : "false");
      });
    }

    function andar(d) {
      var n = peca.passos(cen);
      var novo = Math.max(0, Math.min(n, i + d));
      if (novo === i) return;
      i = novo; pintar();
    }

    raiz.addEventListener("click", function (ev) {
      var b = ev.target.closest("button");
      if (!b) return;
      var a = b.getAttribute("data-a");
      if (a === "passo") andar(1);
      else if (a === "volta") andar(-1);
      else if (a === "reinicia") { i = 0; pintar(); }
      else if (b.hasAttribute("data-cen")) {
        cen = b.getAttribute("data-cen");
        i = reduzido ? peca.passos(cen) : 0;
        pintar();
      }
    });

    /* teclado: só quando o foco está DENTRO da peça, para não
       roubar as setas de outra peça na mesma página            */
    raiz.addEventListener("keydown", function (ev) {
      if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
      if (ev.key === "ArrowRight") { ev.preventDefault(); andar(1); }
      else if (ev.key === "ArrowLeft") { ev.preventDefault(); andar(-1); }
      else if (ev.key === "r" || ev.key === "R") { i = 0; pintar(); }
    });

    if (reduzido) i = peca.passos(cen);   /* estado final, completo */
    pintar();
  }

  API.montarTodos = function () {
    Array.prototype.forEach.call(document.querySelectorAll("[data-int]"), montar);
  };

  document.addEventListener("DOMContentLoaded", API.montarTodos);
})();
