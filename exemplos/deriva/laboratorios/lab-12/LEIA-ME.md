# LAB-12 · Refatorar o `mundo` sob SOLID sem mudar um byte da saída

**Prepara a Aula 24 · semana 13, E2**

## Portão

Despejo **idêntico** em 24 combinações de roteiro e limite. Invariância de
comportamento verificada por comparação de texto, não por teste verde.

## O TODO

O roteiro do esqueleto tem **um** caso. Quais faltam? A lista vazia, o limite
exato, o valor único, todos iguais, um muito maior que o resto. Escreva o
roteiro **antes** de olhar a refatoração - é a ordem que o laboratório cobra, e
é a única ordem em que o roteiro não é escrito para passar.

## O que a refatoração ganhou

| princípio | o que mudou |
|---|---|
| SRP | somar, classificar e formatar são três motivos para mudar, e agora estão em três lugares |
| OCP | o critério vem de fora, então acrescentar um novo não edita nenhuma das três funções |
| DIP | o formatador é uma função recebida, e não `std::cout` embutido |

## O experimento de fechamento, e ele é o mais importante

Depois de passar, **"melhore" a saída**: alinhe o número, acrescente uma linha
de resumo, ordene as peças. O portão acusa, e com razão.

Refatoração e melhoria na mesma passada é como se perde a capacidade de saber
qual das duas quebrou o programa. Se a melhoria vale a pena - e às vezes vale -
ela é um segundo commit, com o roteiro esperado regravado de propósito e a
decisão registrada. Regravar o esperado é uma **decisão**, nunca um conserto.

## Onde está a versão de verdade

`variantes/v2.6-antes/` traz o `mundo` como god class, com as sete
responsabilidades nomeadas, e é a caça ao bug 3 da semana 13. Este laboratório
é o ensaio: mesma disciplina, escala menor.
