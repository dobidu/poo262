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

    /* No fim, a abertura RECOLHE na ultima linha em vez de morar no alto
       da porta de entrada, e o botao que servia para saltar passa a servir
       para reabrir - nada fica inalcancavel.                            */
    function terminar() {
      if (pronto) return;
      pronto = true;
      linhas.forEach(function (l) { l.removeAttribute("data-oculta"); });
      alvo.setAttribute("data-pronta", "1");
      alvo.removeAttribute("data-rodando");
      document.removeEventListener("keydown", terminar);
      document.removeEventListener("pointerdown", terminar);
      if (salto) {
        salto.textContent = "▸ VER A INICIALIZAÇÃO";
        salto.setAttribute("aria-expanded", "false");
        salto.setAttribute("aria-controls", "abertura-log");
      }
    }
    function alternar() {
      var abre = alvo.getAttribute("data-aberta") !== "1";
      if (abre) alvo.setAttribute("data-aberta", "1");
      else alvo.removeAttribute("data-aberta");
      salto.setAttribute("aria-expanded", abre ? "true" : "false");
      salto.textContent = abre ? "▴ RECOLHER" : "▸ VER A INICIALIZAÇÃO";
    }

    /* O clique e registrado ANTES do desvio de reduced-motion. Estava
       depois, e o `return` daquele caminho o pulava: quem pede menos
       movimento (ou abre com ?sem-abertura) recebia o botao ja rotulado
       "VER A INICIALIZACAO" e inerte. E justamente o caminho que tem de
       funcionar. */
    if (salto) salto.addEventListener("click", function () {
      if (pronto) alternar(); else terminar();
    });

    if (reduzido || location.search.indexOf("sem-abertura") > -1) { terminar(); return; }

    // A partir daqui o log cresce: sem este atributo ele fica recolhido,
    // que e o estado de repouso da folha.
    alvo.setAttribute("data-rodando", "1");
    linhas.forEach(function (l) { l.setAttribute("data-oculta", "1"); });
    document.addEventListener("keydown", terminar);
    document.addEventListener("pointerdown", terminar);

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
    /* 1100, e nao 860: a gaveta passou a ser o modo da arvore em toda a
       faixa <=1100px, e travar a rolagem do corpo tem de acompanhar - do
       contrario, em 1000px a gaveta abria por cima de um corpo que
       continuava rolando atras dela. */
    var gavetaEModo = window.innerWidth <= 1100 || raiz.classList.contains("proj");
    document.body.style.overflow = abre && gavetaEModo ? "hidden" : "";
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

  /* ---- o mapa das secoes ----------------------------------
     O `.progresso` era enfeite: o gerador emitia um fio por secao e
     nada aqui os acendia. Agora um fio acende conforme a secao entra
     na tela, os anteriores ficam marcados como vistos, e o nome da
     secao corrente vai para a migalha grudada - que e o que continua
     visivel na projecao depois que a cabeca de aula rola para fora.

     Sem IntersectionObserver (navegador antigo) o mapa continua
     servindo como sete elos para as sete secoes: degrada, nao quebra. */
  function mapaDeSecoes() {
    var mapa = document.querySelector(".progresso");
    if (!mapa || !("IntersectionObserver" in window)) return;
    var fios = Array.prototype.slice.call(mapa.querySelectorAll("a[data-secao]"));
    if (!fios.length) return;
    var campo = document.querySelector("[data-secao-atual]");
    var visiveis = {};

    function pintar() {
      var i, atual = -1;
      for (i = 0; i < fios.length; i++) {
        if (visiveis[fios[i].getAttribute("data-secao")]) { atual = i; break; }
      }
      if (atual === -1) return;
      for (i = 0; i < fios.length; i++) {
        if (i === atual) fios[i].setAttribute("data-atual", "1");
        else fios[i].removeAttribute("data-atual");
        fios[i].setAttribute("data-vista", i < atual ? "1" : "0");
      }
      if (campo) {
        var nome = fios[atual].querySelector(".progresso__nome");
        campo.textContent = nome ? nome.textContent : "";
        campo.hidden = !campo.textContent;
      }
    }

    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        visiveis[e.target.id] = e.isIntersecting;
      });
      pintar();
    }, { rootMargin: "-25% 0px -60% 0px" });

    fios.forEach(function (f) {
      var sec = document.getElementById(f.getAttribute("data-secao"));
      if (sec) obs.observe(sec);
    });
  }

  /* ---- ?projecao ------------------------------------------
     A tecla F liga a projeção, e o URL também. Duas razões: o docente
     deixa a aula da semana no favorito já em escala de sala, e a
     projeção passa a ser capturável sem navegador interativo - antes
     não havia uma única evidência renderizada do modo que a
     disciplina usa em aula.                                    */
  function projecaoPorUrl() {
    if (location.search.indexOf("projecao") > -1) projecao();
  }

  document.addEventListener("DOMContentLoaded", function () {
    esticarMolduras(); abertura(); marcar(); pintarVisitadas(); mapaDeSecoes();
    projecaoPorUrl();
  });
})();
