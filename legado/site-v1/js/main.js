/* ================================================================
   Sintonia POO — main.js
   Funcionalidades: navegação por teclado, copy code, progress bar,
   Mermaid init, active nav link, Godbolt URLs
   ================================================================ */

'use strict';

// --- Progress bar de leitura ---
(function() {
  const bar = document.getElementById('reading-progress');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const mc = document.querySelector('.main-content') || document.documentElement;
    const scrolled = mc.scrollTop || window.scrollY;
    const total = (mc.scrollHeight || document.body.scrollHeight) - window.innerHeight;
    bar.style.width = total > 0 ? Math.min(100, (scrolled / total) * 100) + '%' : '0';
  }, { passive: true });
})();

// --- Marcar link ativo no sidebar ---
(function() {
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(a => {
    if (a.getAttribute('href') === current ||
        a.getAttribute('href') === './' + current) {
      a.classList.add('active');
    }
  });
})();

// --- Botões de copiar código ---
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const block = btn.closest('.code-block');
      const code = block ? block.querySelector('code') : null;
      if (!code) return;
      try {
        await navigator.clipboard.writeText(code.textContent);
        btn.textContent = '✓ copiado';
        btn.classList.add('copied');
        setTimeout(() => {
          btn.textContent = 'copiar';
          btn.classList.remove('copied');
        }, 2000);
      } catch {
        btn.textContent = 'erro';
        setTimeout(() => { btn.textContent = 'copiar'; }, 1500);
      }
    });
  });
});

// --- Inicializar Mermaid ---
document.addEventListener('DOMContentLoaded', () => {
  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'dark',
      darkMode: true,
      themeVariables: {
        background: '#1c2128',
        primaryColor: '#1a3a5c',
        primaryTextColor: '#e6edf3',
        primaryBorderColor: '#7aa2f7',
        lineColor: '#8b949e',
        secondaryColor: '#21262d',
        tertiaryColor: '#161b22',
        fontFamily: 'JetBrains Mono, monospace',
        fontSize: '13px',
      },
      flowchart: { curve: 'basis', htmlLabels: true },
      classDiagram: { useMaxWidth: true },
      sequence: { useMaxWidth: true, showSequenceNumbers: false },
    });
  }
});

// --- Inicializar Prism --- 
document.addEventListener('DOMContentLoaded', () => {
  if (typeof Prism !== 'undefined') Prism.highlightAll();
});

// --- Navegação por teclado (← → para próxima/anterior aula) ---
(function() {
  const prevLink = document.querySelector('.lecture-nav-btn.prev');
  const nextLink = document.querySelector('.lecture-nav-btn.next');

  document.addEventListener('keydown', e => {
    // Não captura se estiver num input/textarea
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if ((e.key === 'ArrowLeft' || e.key === 'h') && prevLink) {
      prevLink.click();
    }
    if ((e.key === 'ArrowRight' || e.key === 'l') && nextLink) {
      nextLink.click();
    }
    // Esc vai para o índice da unidade
    if (e.key === 'Escape') {
      const unitIndex = document.querySelector('a[href="index.html"]');
      if (unitIndex) unitIndex.click();
    }
    // ? abre atalhos de teclado
    if (e.key === '?') toggleKeysHelp();
  });
})();

// --- Toggle ajuda de atalhos ---
function toggleKeysHelp() {
  const hint = document.querySelector('.kbd-hint');
  if (hint) {
    hint.style.opacity = hint.style.opacity === '0' ? '0.7' : '0';
  }
}

// --- Smooth scroll para slides com hash ---
document.addEventListener('DOMContentLoaded', () => {
  if (window.location.hash) {
    const el = document.querySelector(window.location.hash);
    if (el) {
      setTimeout(() => el.scrollIntoView({ behavior: 'smooth', block: 'start' }), 300);
    }
  }
});

// --- Godbolt URL builder ---
function buildGodboltUrl(code, lang = 'c++17', flags = '-std=c++17 -Wall -Wextra -O2') {
  const encoded = btoa(unescape(encodeURIComponent(code)));
  const compiler = lang.includes('20') ? 'g122' : 'g121';
  return `https://godbolt.org/#z:OYLghAFBqd5QCxAYwPYBMCmBRdBLAF1QCcAaPECAKxAEZSBnVAV2OUxAHIBSAJgGY8ANgAd4nLhwDMuAbTAB1AEZyJ84aAHJO3ADJ4A5mLUgAhupXrNzKAE8A1gHUATrT1cA9lwFguUyAGllKABbR3QJAD0AKgBqADNUAAUJCQDjQOMgA%3D%3D`;
}

// --- Expandir/colapsar seções longas --- 
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-collapsible]').forEach(section => {
    const content = section.querySelector('.collapsible-content');
    const btn = section.querySelector('.collapse-btn');
    if (!content || !btn) return;
    btn.addEventListener('click', () => {
      const isOpen = content.style.display !== 'none';
      content.style.display = isOpen ? 'none' : '';
      btn.textContent = isOpen ? '▶ mostrar' : '▼ ocultar';
    });
  });
});

// --- Search simples (para páginas com muitos slides) ---
(function() {
  const searchInput = document.getElementById('slide-search');
  if (!searchInput) return;
  searchInput.addEventListener('input', () => {
    const q = searchInput.value.toLowerCase().trim();
    document.querySelectorAll('.slide').forEach(slide => {
      const text = slide.textContent.toLowerCase();
      slide.style.display = (!q || text.includes(q)) ? '' : 'none';
    });
  });
})();
