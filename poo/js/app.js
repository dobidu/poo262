/* =============================================================
   POO v2 · app.js
   Moldura do site: abertura POST (uma vez, saltável), gaveta de
   navegação, projeção (F), navegação entre aulas (J/K), copiar
   código, e marcação de aula visitada.
   Nada essencial depende deste arquivo: sem JS o conteúdo lê.
   ============================================================= */
(function () {
  "use strict";
  var raiz = document.documentElement;
  var reduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- T3 · abertura tipo POST ------------------------------
     Uma vez por visita, e saltável de imediato: quem volta pela
     décima vez aperta qualquer coisa e está dentro. Sob
     reduced-motion nasce no estado final.                       */
  function abertura() {
    var alvo = document.querySelector("[data-abertura]");
    if (!alvo) return;
    var linhas = Array.prototype.slice.call(alvo.querySelectorAll("[data-post]"));
    var salto = alvo.querySelector("[data-saltar]");
    var pronto = false;

    function terminar() {
      if (pronto) return;
      pronto = true;
      linhas.forEach(function (l) { l.removeAttribute("data-oculta"); });
      alvo.setAttribute("data-pronta", "1");
      document.removeEventListener("keydown", terminar);
      document.removeEventListener("pointerdown", terminar);
      if (salto) salto.hidden = true;
    }

    if (reduzido || location.search.indexOf("sem-abertura") > -1) { terminar(); return; }

    linhas.forEach(function (l) { l.setAttribute("data-oculta", "1"); });
    document.addEventListener("keydown", terminar);
    document.addEventListener("pointerdown", terminar);
    if (salto) salto.addEventListener("click", terminar);

    var k = 0;
    (function proxima() {
      if (pronto) return;
      if (k >= linhas.length) { terminar(); return; }
      linhas[k].removeAttribute("data-oculta");
      k++;
      setTimeout(proxima, 165);
    })();
  }

  /* ---- projeção (F): escala, não modo ---------------------- */
  function projecao() {
    raiz.classList.toggle("proj");
    var b = document.querySelector('[data-acao="projecao"]');
    if (b) b.setAttribute("aria-pressed", raiz.classList.contains("proj") ? "true" : "false");
    if (document.fullscreenEnabled) {
      if (raiz.classList.contains("proj") && !document.fullscreenElement) {
        var p = raiz.requestFullscreen();
        if (p && p.catch) p.catch(function () {});
      } else if (document.fullscreenElement) { document.exitFullscreen(); }
    }
  }
  document.addEventListener("fullscreenchange", function () {
    if (!document.fullscreenElement) {
      raiz.classList.remove("proj");
      var b = document.querySelector('[data-acao="projecao"]');
      if (b) b.setAttribute("aria-pressed", "false");
    }
  });

  /* ---- gaveta da árvore de aulas --------------------------- */
  function gaveta(forcar) {
    var a = document.querySelector(".arvore");
    var b = document.querySelector('[data-acao="gaveta"]');
    if (!a) return;
    var abre = forcar !== undefined ? forcar : a.getAttribute("data-aberta") !== "1";
    a.setAttribute("data-aberta", abre ? "1" : "0");
    if (b) b.setAttribute("aria-expanded", abre ? "true" : "false");
    document.body.style.overflow = abre && window.innerWidth <= 860 ? "hidden" : "";
    if (abre) { var f = a.querySelector("a"); if (f) f.focus(); }
  }

  /* ---- aulas visitadas: memória local, degradável ---------- */
  var CH = "poo-visitadas";
  function lidas() {
    try { return JSON.parse(localStorage.getItem(CH) || "[]"); } catch (e) { return []; }
  }
  function marcar() {
    var atual = document.querySelector("[data-aula-slug]");
    if (!atual) return;
    var slug = atual.getAttribute("data-aula-slug");
    var v = lidas();
    if (v.indexOf(slug) === -1) {
      v.push(slug);
      try { localStorage.setItem(CH, JSON.stringify(v)); } catch (e) {}
    }
  }
  function pintarVisitadas() {
    var v = lidas();
    Array.prototype.forEach.call(document.querySelectorAll("a[data-slug]"), function (a) {
      if (v.indexOf(a.getAttribute("data-slug")) > -1) a.setAttribute("data-visitada", "1");
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-unidade-conta]"), function (el) {
      var slugs = (el.getAttribute("data-unidade-conta") || "").split(",").filter(Boolean);
      var n = slugs.filter(function (s) { return v.indexOf(s) > -1; }).length;
      var b = el.querySelector("b");
      if (b) b.textContent = String(n);
    });
  }

  /* ---- copiar código -------------------------------------- */
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-acao]");
    if (!b) return;
    var a = b.getAttribute("data-acao");
    if (a === "projecao") projecao();
    else if (a === "gaveta") gaveta();
    else if (a === "copiar") {
      var pre = b.closest(".codigo").querySelector("pre");
      var txt = pre ? pre.innerText : "";
      var ok = function () { var o = b.textContent; b.textContent = "✓ COPIADO"; setTimeout(function () { b.textContent = o; }, 1400); };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(ok, function () {});
      else ok();
    }
  });

  /* ---- teclado da página ----------------------------------
     As setas NÃO são da página: pertencem aos interativos.
     A página anda com J/K, como em LPII.                      */
  document.addEventListener("keydown", function (ev) {
    if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
    var t = ev.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    if (t && t.closest && t.closest("[data-int]")) return;
    function ir(rel) {
      var l = document.querySelector('link[rel="' + rel + '"]');
      if (l && l.href) location.href = l.href;
    }
    switch (ev.key) {
      case "j": case "J": ir("prev"); break;
      case "k": case "K": ir("next"); break;
      case "f": case "F": ev.preventDefault(); projecao(); break;
      case "m": case "M": ev.preventDefault(); gaveta(); break;
      case "Escape": gaveta(false); break;
      default: return;
    }
  });

  /* ---- réguas de moldura ----------------------------------
     O HTML traz um trecho curto de ─ (para ler sem JS) e aqui a
     régua é esticada até preencher a largura do painel. É por
     isso que a moldura são caracteres reais e não uma border.  */
  function esticarMolduras() {
    var TRACO = new Array(200).join("─");
    Array.prototype.forEach.call(document.querySelectorAll(".moldura__regua[data-fill]"), function (el) {
      el.textContent = TRACO;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    esticarMolduras(); abertura(); marcar(); pintarVisitadas();
  });
})();
