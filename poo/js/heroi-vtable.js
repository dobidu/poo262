/* =============================================================
   POO v2 · heroi-vtable.js
   A animação da capa: uma chamada descendo pelo vptr até a
   vtable - e indo para o lugar errado quando falta `virtual`.

   Não é enfeite: o glifo desenhado no terminal da Deriva é
   consequência de qual função foi resolvida. Com `virtual`
   desligado, as três entidades saem como `·`, porque a chamada
   resolveu pelo tipo do PONTEIRO. Isso é o Cap. 11 inteiro numa
   linha de saída.

   A capa é o único lugar do site com movimento contínuo, e mesmo
   aqui há botão de passo a passo. Sob prefers-reduced-motion
   nasce parada, no quadro em que o erro já é visível.
   ============================================================= */
(function () {
  "use strict";

  var ENT = [
    { n: "sonda", g: "@", cor: "var(--fosforo)" },
    { n: "drone", g: "d", cor: "var(--frio)" },
    { n: "item", g: "!", cor: "var(--ok)" }
  ];
  var SLOTS = ["desenhar()", "agir()", "~entidade()"];
  var ETAPAS = ["e = &objeto", "lê o vptr", "indexa vtable[0]", "chama"];

  function montar(raiz) {
    var reduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var elPalco = raiz.querySelector("[data-heroi-palco]");
    var elSaida = raiz.querySelector("[data-heroi-saida]");
    var elEst = raiz.querySelector("[data-heroi-est]");
    var btVirt = raiz.querySelector('[data-heroi="virtual"]');
    var btModo = raiz.querySelector('[data-heroi="modo"]');
    var btPasso = raiz.querySelector('[data-heroi="passo"]');
    if (!elPalco) return;

    var st = { virt: true, ent: 0, etapa: 0, auto: !reduzido, desenhados: [] };
    var timer = 0, visivel = true;

    function pintar() {
      var e = ENT[st.ent], p = st.etapa;
      var vt = st.virt ? "vtable(" + e.n + ")" : " - ";

      elPalco.innerHTML =
        bloco("PONTEIRO DE BASE", p >= 1, [
          ["entidade* e", "var(--leitura)"],
          ["→ &amp;" + e.n, p >= 1 ? "var(--fosforo)" : "var(--fantasma)"],
          ["e-&gt;desenhar()", p >= 1 ? "var(--fosforo-alto)" : "var(--fantasma)"]
        ]) +
        conector(p >= 2, st.virt) +
        bloco("OBJETO " + e.n, p >= 2 && st.virt, st.virt ? [
          ["[vptr] → " + vt, p >= 2 ? "var(--frio)" : "var(--fantasma)"],
          ["[pos]  {4,7}", "var(--apagado)"],
          ["16 bytes", "var(--fantasma)"]
        ] : [
          ["(não há vptr)", "var(--falha)"],
          ["[pos]  {4,7}", "var(--apagado)"],
          ["8 bytes", "var(--fantasma)"]
        ]) +
        conector(p >= 3, st.virt) +
        bloco(st.virt ? vt : "RESOLUÇÃO ESTÁTICA", p >= 3, SLOTS.map(function (s, k) {
          var sel = p >= 3 && k === 0;
          return [(sel ? "▸" : " ") + "[" + k + "] " + (st.virt ? e.n : "entidade") + "::" + s,
            sel ? (st.virt ? "var(--fosforo-alto)" : "var(--falha)") : "var(--fantasma)"];
        })) +
        conector(p >= 4, st.virt) +
        bloco("O QUE EXECUTA", p >= 4, [
          [st.virt ? e.n + "::desenhar()" : "entidade::desenhar()", p >= 4 ? (st.virt ? "var(--ok)" : "var(--falha)") : "var(--fantasma)"],
          ["escreve '" + (st.virt ? e.g : "·") + "'", p >= 4 ? "var(--leitura)" : "var(--fantasma)"]
        ]);

      var linha = st.desenhados.map(function (d) {
        return '<span style="color:' + d.cor + '">' + d.g + "</span>";
      }).join("");
      var falta = 3 - st.desenhados.length;
      elSaida.innerHTML = '<span style="color:var(--fantasma)">#░░</span>' + linha +
        new Array(falta + 1).join('<span style="color:var(--grade-alta)">·</span>') +
        '<span style="color:var(--fantasma)">░░#</span>' +
        '<span class="cursor">█</span>';

      elEst.innerHTML =
        "<span>tipo estático <b>entidade*</b></span>" +
        "<span>tipo dinâmico <b>" + e.n + "</b></span>" +
        "<span>etapa <b>" + (p === 0 ? " - " : ETAPAS[p - 1]) + "</b></span>" +
        "<span>" + (st.virt
          ? 'resolvido pela <b style="color:var(--ok)">vtable</b>, em execução'
          : 'resolvido na <b style="color:var(--falha)">compilação ▲</b>') + "</span>";

      if (btVirt) {
        btVirt.setAttribute("aria-pressed", st.virt ? "true" : "false");
        btVirt.textContent = st.virt ? "✓ virtual LIGADO" : "▲ virtual DESLIGADO";
      }
      if (btModo) btModo.textContent = st.auto ? "││ PASSO A PASSO" : "▶ CONTINUAR";
      if (btPasso) btPasso.hidden = st.auto;
    }

    function bloco(cab, aceso, linhas) {
      return '<div class="hv__bloco"' + (aceso ? ' data-aceso="1"' : "") + ">" +
        '<div class="hv__cab">' + cab + "</div>" +
        linhas.map(function (l) {
          return '<div style="color:' + l[1] + '">' + l[0] + "</div>";
        }).join("") + "</div>";
    }
    function conector(aceso, virt) {
      return '<span class="hv__seta" data-aceso="' + (aceso ? 1 : 0) + '" data-t="' +
        (virt ? "ok" : "falha") + '">' + (virt ? "──▶" : "┄┄▶") + "</span>";
    }

    function andar() {
      st.etapa++;
      if (st.etapa > 4) {
        st.desenhados.push({ g: st.virt ? ENT[st.ent].g : "·", cor: st.virt ? ENT[st.ent].cor : "var(--falha)" });
        st.etapa = 0;
        st.ent++;
        if (st.ent >= ENT.length) { st.ent = 0; st.desenhados = []; }
      }
      pintar();
    }

    function tocar() {
      parar();
      if (!st.auto || !visivel || document.hidden) return;
      timer = setInterval(andar, 820);
    }
    function parar() { if (timer) { clearInterval(timer); timer = 0; } }

    if (btVirt) btVirt.addEventListener("click", function () {
      st.virt = !st.virt; st.etapa = 0; st.ent = 0; st.desenhados = []; pintar();
    });
    if (btModo) btModo.addEventListener("click", function () {
      st.auto = !st.auto; pintar(); tocar();
    });
    if (btPasso) btPasso.addEventListener("click", andar);

    document.addEventListener("visibilitychange", function () { if (document.hidden) parar(); else tocar(); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        visivel = es[0].isIntersecting;
        if (visivel) tocar(); else parar();
      }, { threshold: 0.1 }).observe(raiz);
    }

    if (reduzido) {
      /* nasce parada no quadro em que o erro é visível: virtual
         desligado, três entidades já desenhadas como `·`        */
      st.auto = false; st.virt = false; st.etapa = 4; st.ent = 2;
      st.desenhados = [{ g: "·", cor: "var(--falha)" }, { g: "·", cor: "var(--falha)" }];
      pintar();
    } else {
      pintar(); tocar();
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll("[data-heroi-vtable]"), montar);
  });
})();
