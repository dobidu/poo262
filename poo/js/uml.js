/* =============================================================
   POO v2 · uml.js  (T9)
   UML como ferramenta, não figura: o aluno acrescenta classe e
   relação, e o diagrama se reorganiza - os níveis são calculados
   pela profundidade de herança, não posicionados à mão.
   Aguenta de 3 a 8 classes, que é o intervalo do material.
   ============================================================= */
(function () {
  "use strict";
  var esc = window.POO.esc;

  /* catálogo real da hierarquia da Deriva ------------------- */
  var CAT = {
    entidade: { rot: "entidade", tipo: "abstrata", pai: null,
      membros: ["- vetor2 pos", "- char glifo"],
      metodos: ["+ virtual ~entidade()", "+ virtual void desenhar() const = 0", "+ virtual void agir(mundo&)"],
      base: true },
    sonda:    { rot: "sonda", tipo: "concreta", pai: "entidade",
      membros: ["- int energia"], metodos: ["+ void desenhar() const override", "+ void agir(mundo&) override"] },
    drone:    { rot: "drone", tipo: "concreta", pai: "entidade",
      membros: ["- int carga"], metodos: ["+ void desenhar() const override"] },
    item:     { rot: "item", tipo: "concreta", pai: "entidade",
      membros: ["- std::string nome"], metodos: ["+ void desenhar() const override"] },
    i_reparo: { rot: "i_reparavel", tipo: "interface", pai: null,
      membros: [], metodos: ["+ virtual bool reparar(celula&) = 0"] },
    reparadora: { rot: "sonda_reparadora", tipo: "concreta", pai: "sonda", tambem: "i_reparo",
      membros: [], metodos: ["+ bool reparar(celula&) override"] },
    componente: { rot: "componente", tipo: "abstrata", pai: null,
      membros: [], metodos: ["+ virtual int massa() const = 0"] },
    mochila:  { rot: "mochila", tipo: "concreta", pai: "componente", compoe: "componente",
      membros: ["- vector&lt;unique_ptr&lt;componente&gt;&gt; itens"], metodos: ["+ int massa() const override"] }
  };
  var INICIAL = ["entidade", "sonda", "drone"];

  function montar(raiz) {
    var ativos = INICIAL.slice();
    var sel = null;

    function nivel(k) {
      var n = 0, cur = CAT[k];
      while (cur && cur.pai) { n++; cur = CAT[cur.pai]; }
      return n;
    }

    function pintar() {
      var porNivel = {};
      ativos.forEach(function (k) {
        var n = nivel(k);
        (porNivel[n] = porNivel[n] || []).push(k);
      });
      var niveis = Object.keys(porNivel).sort();
      var html = "";
      niveis.forEach(function (n, idx) {
        html += '<div class="uml__nivel">' + porNivel[n].map(function (k) {
          var d = CAT[k];
          return '<div class="classe" data-tipo="' + d.tipo + '"' + (sel === k ? ' data-sel="1"' : "") +
            ' tabindex="0" data-classe="' + k + '">' +
            '<div class="classe__nome">' +
              (d.tipo === "interface" ? '<span class="classe__estereo">«interface»</span>' : "") +
              (d.tipo === "abstrata" ? '<span class="classe__estereo">«abstrata»</span>' : "") +
              esc(d.rot) + "</div>" +
            (d.membros.length ? '<div class="classe__membros">' + d.membros.join("<br>") + "</div>" : "") +
            '<div class="classe__metodos">' + d.metodos.map(function (m) {
              var pura = m.indexOf("= 0") > -1;
              var virt = m.indexOf("virtual") > -1 || m.indexOf("override") > -1;
              return '<div class="' + (pura ? "pura" : virt ? "virt" : "") + '">' + m + "</div>";
            }).join("") + "</div>" +
            "</div>";
        }).join("") + "</div>";
        if (idx < niveis.length - 1) {
          html += '<div class="uml__liga" aria-hidden="true">△<br>│<br><b>herança pública</b></div>';
        }
      });
      /* composição é seta de losango cheio: relação diferente,
         desenho diferente - não basta trocar a cor            */
      if (ativos.indexOf("mochila") > -1) {
        html += '<div class="uml__liga" aria-hidden="true">◆── <b>composição · mochila contém componentes (Composite)</b></div>';
      }
      if (ativos.indexOf("reparadora") > -1) {
        html += '<div class="uml__liga" aria-hidden="true">△┄┄ <b>implementação · sonda_reparadora também é i_reparavel (diamante do Cap. 17)</b></div>';
      }
      raiz.querySelector("[data-uml-palco]").innerHTML = html;

      Array.prototype.forEach.call(raiz.querySelectorAll("[data-add]"), function (b) {
        var k = b.getAttribute("data-add");
        var dentro = ativos.indexOf(k) > -1;
        b.setAttribute("aria-pressed", dentro ? "true" : "false");
        var pai = CAT[k].pai;
        var podeEntrar = !pai || ativos.indexOf(pai) > -1;
        b.setAttribute("aria-disabled", (!dentro && !podeEntrar) ? "true" : "false");
        b.title = (!dentro && !podeEntrar) ? "precisa de " + CAT[pai].rot + " primeiro" : "";
      });

      var d = sel ? CAT[sel] : null;
      raiz.querySelector("[data-uml-estado]").innerHTML =
        "<table><tbody>" +
        "<tr><th>classes</th><td>" + ativos.length + " de 8</td></tr>" +
        "<tr><th>profundidade</th><td>" + (Math.max.apply(null, ativos.map(nivel)) + 1) + " nível(is)</td></tr>" +
        "<tr><th>abstratas</th><td>" + ativos.filter(function (k) { return CAT[k].tipo !== "concreta"; }).length +
          ' <span style="color:var(--fantasma)"> - não instanciáveis</span></td></tr>' +
        "<tr><th>selecionada</th><td>" + (d ? esc(d.rot) + " - " + d.tipo +
          (d.pai ? ", deriva de " + esc(CAT[d.pai].rot) : ", raiz") : " - clique numa classe") + "</td></tr>" +
        "<tr><th>destrutor virtual</th><td>" +
          (ativos.indexOf("entidade") > -1
            ? '<span class="bom">✓ na base - deletar por entidade* é seguro</span>'
            : '<span class="aviso">▲ sem base polimórfica</span>') + "</td></tr>" +
        "</tbody></table>";
    }

    raiz.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-add]");
      if (b) {
        if (b.getAttribute("aria-disabled") === "true") return;
        var k = b.getAttribute("data-add");
        var idx = ativos.indexOf(k);
        if (idx > -1) {
          /* remover leva os descendentes com ela - herança é
             dependência, e o diagrama não mente sobre isso     */
          ativos = ativos.filter(function (a) {
            var cur = CAT[a];
            while (cur) { if (cur === CAT[k]) return false; cur = cur.pai ? CAT[cur.pai] : null; }
            return true;
          });
          if (sel && ativos.indexOf(sel) === -1) sel = null;
        } else if (ativos.length < 8) { ativos.push(k); }
        pintar(); return;
      }
      var cl = ev.target.closest("[data-classe]");
      if (cl) { sel = cl.getAttribute("data-classe"); pintar(); }
      if (ev.target.closest("[data-uml-reset]")) { ativos = INICIAL.slice(); sel = null; pintar(); }
    });

    pintar();
  }

  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll("[data-uml]"), montar);
  });
})();
