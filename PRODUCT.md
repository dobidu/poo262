# PRODUCT.md · Material de POO · UFPB

## O que é

O material completo da disciplina de **Programação Orientada a Objetos em C++17**
do Centro de Informática da UFPB: um site de 38 páginas, um livro de apoio de
283 páginas, e o repositório do sistema que atravessa o curso.

Três artefatos, uma fonte. `conteudo/mapa.py` é a tabela canônica - 26 aulas em
3 unidades, 3 anexos, 20 versões do sistema, 12 laboratórios, 8 tipos de exemplo
interativo -, e site e livro derivam dela. Livro e site divergem quando não há
fonte única, e foi o que aconteceu na versão anterior.

- **Autor e docente:** Carlos Eduardo Coelho Freire Batista · `bidu@ci.ufpb.br`
- **Oferta-alvo:** 2026.2 · 60 h · 4 créditos · 30 encontros de 2 h
- **Padrão-alvo:** C++17, e ele é teto. C++20 aparece rotulado, num anexo e num
  alvo de compilação separado.

## Quem lê

**O estudante de início de graduação**, que vem de C ou de Python e nunca
escreveu um sistema de vinte classes. Ele lê o livro em casa, no PDF ou
impresso, e vê o site projetado em sala. Não é leitor de referência: é leitor de
primeira passagem, que precisa entender o mecanismo antes de consultar a
sintaxe.

**O docente**, que projeta o site em sala em regime de predição: antes de o
passo avançar, os estudantes escrevem o que vai acontecer, e comparam.

## O que o material existe para fazer

Formar **uma** habilidade central: determinar o comportamento de um programa
C++ **a partir do texto**, e não de uma execução observada. Qual construtor
roda, qual destrutor, qual função virtual é chamada, o que sobra no objeto de
origem depois de um `std::move`, o que a ordem de declaração dos membros custa
em bytes.

Quem só sabe responder compilando confia na execução observada. A prova da
disciplina é em papel por essa razão.

## O sistema que atravessa o curso: o Deriva

Um *roguelike* de terminal em que uma sonda de inspeção percorre uma estação
orbital abandonada. Vinte versões, uma por aula, todas compilando, e quatro
variantes **deliberadamente quebradas** onde o erro ensina mais que o acerto.

Três razões para o artefato ser este:

1. **RAII tem consequência física.** `terminal_bruto` põe o terminal em modo
   bruto no construtor e o restaura no destrutor. Sem o destrutor, o terminal do
   estudante fica inutilizável **depois** que o programa sai.
2. **A falha é visível.** Destrutor não virtual aparece como entidade que não
   desaparece do mapa; objeto usado depois de movido aparece como glifo em
   branco.
3. **O Qt entra como segundo front-end** sobre o mesmo núcleo, o que torna a
   separação domínio/apresentação demonstrável em vez de afirmada.

## As restrições, e nenhuma é acidental

**As máquinas do laboratório não têm sanitizer nem Valgrind, e isso é
conteúdo.** O ferramental é `g++`, `cmake`, `gdb` e `git`. Sem detector
automático, a posse precisa ser verificável à mão, por três técnicas ensinadas
antes de serem exigidas: o contador de instâncias vivas, a instrumentação de
ciclo de vida, e o `gdb` com ponto de parada em destrutor.

**Todo trecho de código do material é extraído de arquivo que compila**, nunca
digitado no texto. São 152 trechos, declarados por âncora em
`conteudo/trechos.py`, e o build falha se uma âncora deixar de existir.

**Todo número que a prosa afirma é medido.** `conteudo/medidas.py` é gerado
rodando o binário, e um portão recusa afirmação que o código negue. Já pegou
quatro números errados, entre eles uma afirmação central que estava falsa nas
duas direções.

**O material publicado não carrega marcador de pendência.** Nem `REVISAR`, nem
`PENDENTE`, nem `a definir`. A pendência se resolve; sinalizá-la transfere ao
leitor um trabalho que é nosso, e esconder é pior.

## O que já existe

| artefato | estado |
|---|---|
| site | 38 páginas, geradas · 26 aulas, 3 anexos, trilha, 12 laboratórios, rubrica, portão, plano de ensino, glossário |
| livro | 283 páginas · 26 capítulos + 3 anexos + glossário e referências · Aula N = Capítulo N |
| Deriva | v0.0 → v2.7 · 188 testes verdes · `make verifica` 4 de 4 · 4 variantes quebradas |
| laboratórios | 12, com enunciado, esqueleto e solução de referência verificada pelo `ctest` |
| interativos | 9 peças, 8 tipos canônicos, contrato testado sem navegador |

## O idioma visual, que já está estabelecido

Herdado do Claude Design e implementado em `poo/css/tokens.css` e
`poo/css/pagina.css`. Ele **não** é para ser substituído:

- **Fósforo âmbar** (`#F2A93B`) sobre preto de viés esverdeado (`#0A0C0B`).
  Prosa nunca é âmbar: o âmbar é moldura, rótulo, cursor e ênfase de interface.
- **Três famílias, três papéis semânticos.** IBM Plex Mono para código, moldura,
  rótulo, estado interno e navegação; Plex Serif para prosa; Plex Sans para
  legenda de interativo e de figura.
- **Box-drawing como primitiva.** As molduras são caracteres reais
  (`─ │ ┌ ┐ └ ┘ ├ ┤ ╭ ╮ ╰ ╯`), com o título embutido na moldura superior.
- **A estética é diegética**: o visual TUI é literalmente a interface do sistema
  que o estudante constrói. Site e projeto são a mesma coisa visualmente.
- Cor nunca é o único portador de significado: todo estado semântico tem glifo e
  rótulo textual ao lado.
- Azul UFPB só em badge institucional e rodapé.

## O que faria um resultado polido parecer errado

- Prosa em âmbar, ou qualquer uso do âmbar que o transforme em cor de texto.
- Moldura desenhada com `border` no lugar de caractere, ou box-drawing que
  desalinhe.
- Emoji. O idioma é box-drawing e formas geométricas; emoji é do material antigo
  e foi removido.
- Travessão `—` ou en-dash `–`, em qualquer registro. Hífen espaçado no lugar. <!-- voz:permitido -->
- Bloco de código com quebra de linha automática. Código nunca reflui.
- Cor decorativa: `--ok` e `--falha` marcam exclusivamente *compila × quebrado
  de propósito*, sempre com glifo e rótulo.
- Autoplay em exemplo interativo. O passo é sempre do estudante.
