# LAB-10 · CRTP e `contador_de_instancias<T>`: generalizar o próprio detector

**Prepara a Aula 19 · semana 11, E1**

## Portão

As três classes usando o contador generalizado, com comportamento **idêntico**
ao escrito à mão, e custo zero declarado.

## Os três TODO

1. **Falta o parâmetro de template.** Rode antes de acrescentá-lo: os três
   tipos compartilham **um** contador só, e nenhum deles acusa mais nada. É o
   mesmo erro que um contador na classe base cometeria.
2. **A cópia também é um nascimento.** O mesmo item do LAB-04, agora no
   template - e agora corrigido em um lugar em vez de seis.
3. **Passe cada tipo a si mesmo.** `struct sonda : contador_de_instancias<sonda>`.
   É a linha que parece circular e não é: na hora em que a base é instanciada,
   `sonda` já é um tipo declarado, e é só disso que o template precisa.

## Por que este laboratório vem depois de doze capítulos

Porque o contador foi escrito à mão **seis vezes** no Deriva antes disto:
`sonda`, `drone`, `item`, `mapa`, `terminal_bruto`, `no_estacao`. Quem sentiu o
tédio da sexta cópia entende por que generalizar. Quem não sentiu acha que
template é enfeite, e é por isso que a Aula 19 não vem antes da 7.

## O que o template ganha, e é medido

`sizeof` da base é 1 (base vazia), e a derivada **não cresce** por causa dela.
Nenhuma vtable, nenhum custo em execução. É a diferença entre polimorfismo
estático e dinâmico, e ela aparece no `sizeof`.

## A pergunta de fechamento

Tente trocar o CRTP por uma base não-template comum. Além de compartilhar o
contador, o que mais se perde? Pense no que aconteceria com um `delete` por
ponteiro dessa base.
