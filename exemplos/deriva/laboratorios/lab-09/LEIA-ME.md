# LAB-09 · Catch2 e o replay determinístico como especificação

**Prepara a Aula 16 · semana 9, E1**

## Portão

Escrever o teste que **trava a refatoração antes de refatorar**. A ordem é
cobrada, e é o conteúdo do laboratório: quem refatora e depois escreve o teste
escreve o teste que passa.

## Os dois TODO

1. **Uma semente só é um teste que passa por acaso.** O esqueleto traz uma.
   Escolha quantas e quais, e escreva por que essas - a resposta não é "muitas".
2. **O roteiro exercita o meio.** Acrescente as bordas: largura mínima, limite
   esquerdo, lista de zero passo. Sem elas, a refatoração pode quebrar o limite
   sem que ninguém note, e o portão passaria.

## O que o teste tem de provar, e o que não basta

Três condições, e as duas últimas são as que se esquece:

- o despejo é **idêntico** entre a versão antes e a depois;
- a mesma semente sempre dá o mesmo despejo (senão não é replay, é sorte);
- sementes **diferentes** dão despejos diferentes - sem isso, o teste passaria
  comparando duas funções que ignoram a entrada.

## O experimento de fechamento

Troque a ordem das duas chamadas a `s.ate` em `percurso_depois`. A lógica não
mudou; o despejo mudou, porque a **ordem de consumo do sorteio** é parte do
comportamento observável. O portão acusa, e é exatamente o erro que a caça ao
bug 3 procura na semana 13.
