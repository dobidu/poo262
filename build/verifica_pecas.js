/* =============================================================
   build/verifica_pecas.js - o contrato dos interativos, testado.

   O motor garante o contrato em tempo de execução; este teste
   garante que cada peça o cumpre ANTES de ir ao ar, e roda sem
   navegador. Confere, para as 9 peças:

     · pelo menos um cenário que demonstra a falha e um que a evita;
     · quadro(cen, i) definido para TODO i de 0 a passos(cen);
     · palco, estado e legenda não-vazios em todo passo;
     · pureza: chamar duas vezes o mesmo (cen, passo) dá o mesmo
       byte - é isso que faz "voltar" ser exato e não animação
       reversa;
     · nada de Math.random e nada de autoplay no código-fonte.

   Uso: node build/verifica_pecas.js
   ============================================================= */
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const RAIZ = path.join(__dirname, "..");
const ARQUIVOS = ["poo/js/pecas.js", "poo/js/pecas-extra.js"];

const pecas = {};
const janela = {
  POO: {
    registrar: (slug, p) => { pecas[slug] = p; },
    esc: (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"),
    caixa: (o) => `[caixa ${o.cab || ""}]${o.corpo}`,
    moldura: () => "",
  },
  matchMedia: () => ({ matches: false }),
};
const contexto = { window: janela, document: { addEventListener() {} },
                   Math, String, Array, Object, JSON, Number };
contexto.globalThis = contexto;

/* comentário não é código: a varredura olha o fonte sem comentários,
   senão a própria frase "sem Math.random" acusaria a peça. */
const semComentarios = (s) => s.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^\s*\/\/.*$/gm, "");

let fontes = "";
for (const rel of ARQUIVOS) {
  const src = fs.readFileSync(path.join(RAIZ, rel), "utf8");
  fontes += semComentarios(src);
  vm.runInNewContext(src, contexto, { filename: rel });
}

const erros = [];
const nomes = Object.keys(pecas);

if (/Math\.random/.test(fontes)) erros.push("há Math.random no fonte das peças - o estado deixaria de ser função de (cenário, passo)");
if (/setInterval|setTimeout|autoplay/i.test(fontes)) erros.push("há temporizador no fonte das peças - nenhuma peça pode andar sozinha");

for (const nome of nomes) {
  const p = pecas[nome];
  const onde = `peça "${nome}"`;
  if (!p.titulo) erros.push(`${onde}: sem título para a moldura`);
  if (!Array.isArray(p.cenarios) || p.cenarios.length < 2)
    erros.push(`${onde}: precisa de ao menos dois cenários`);
  const tipos = (p.cenarios || []).map((c) => c.tipo);
  if (!tipos.includes("falha")) erros.push(`${onde}: nenhum cenário do tipo "falha" - o contrato exige um que demonstre a falha`);
  if (!tipos.includes("ok")) erros.push(`${onde}: nenhum cenário do tipo "ok" - o contrato exige um que a evite`);

  for (const c of p.cenarios || []) {
    const n = p.passos(c.id);
    if (!Number.isInteger(n) || n < 1) { erros.push(`${onde}/${c.id}: passos() devolveu ${n}`); continue; }
    for (let i = 0; i <= n; i++) {
      let q;
      try { q = p.quadro(c.id, i); }
      catch (e) { erros.push(`${onde}/${c.id} passo ${i}: quadro() lançou ${e.message}`); continue; }
      if (!q || typeof q.palco !== "string" || !q.palco.trim())
        erros.push(`${onde}/${c.id} passo ${i}: palco vazio`);
      if (!Array.isArray(q.estado) || q.estado.length < 3)
        erros.push(`${onde}/${c.id} passo ${i}: painel de estado com menos de 3 linhas - é ele que mostra o que a execução não mostra`);
      for (const l of q.estado || []) {
        if (!Array.isArray(l) || l.length !== 2 || !String(l[0]).trim() || !String(l[1]).trim())
          erros.push(`${onde}/${c.id} passo ${i}: linha de estado malformada: ${JSON.stringify(l)}`);
      }
      if (typeof q.legenda !== "string" || q.legenda.trim().length < 40)
        erros.push(`${onde}/${c.id} passo ${i}: legenda curta ou ausente - o contrato pede uma ou duas frases dizendo onde olhar`);

      const outra = p.quadro(c.id, i);
      if (JSON.stringify(outra) !== JSON.stringify(q))
        erros.push(`${onde}/${c.id} passo ${i}: quadro() não é puro - duas chamadas divergem`);
    }
    // ir e voltar tem de reconstruir o mesmo quadro
    const ida = JSON.stringify(p.quadro(c.id, 1));
    p.quadro(c.id, n);
    if (JSON.stringify(p.quadro(c.id, 1)) !== ida)
      erros.push(`${onde}/${c.id}: passar pelo fim e voltar ao passo 1 mudou o quadro - há estado acumulado`);
  }
}

const passos = nomes.reduce((a, n) =>
  a + pecas[n].cenarios.reduce((b, c) => b + pecas[n].passos(c.id) + 1, 0), 0);

if (erros.length) {
  for (const e of erros) console.log("CONTRATO ERRO:", e);
  console.log(`${erros.length} violações em ${nomes.length} peças`);
  process.exit(1);
}
console.log(`contrato OK: ${nomes.length} peças · ` +
  `${nomes.reduce((a, n) => a + pecas[n].cenarios.length, 0)} cenários · ` +
  `${passos} quadros conferidos (puros, com falha e com ok)`);
