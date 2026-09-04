# LAB-05 · Ciclo de vida e `terminal_bruto`: RAII com consequência

**Prepara a Aula 8 · semana 4, E2**

## Portão

Três roteiros de traço batendo **linha por linha**, e o modo do sistema
restaurado nos três - inclusive naquele em que uma exceção passa por cima.

## Por que o recurso aqui é simulado

O `terminal_bruto` de verdade mexe em `termios`, e um laboratório que quebra o
terminal de quem o roda em pipe não serve para portão automático. O recurso
aqui é um "modo do sistema" global, com a mesma forma: adquirido no construtor,
restaurado no destrutor, e **visível de fora do objeto**.

Depois de passar, rode a variante de verdade: `variantes/v0.2-quebrada/`, com
`< /dev/null` primeiro.

## Os dois TODO

1. **Uma linha no destrutor.** Ela é a diferença entre RAII e promessa. Rode
   sem ela e o roteiro 3 falha: o modo nunca volta, e o próximo escopo herda o
   estado que o anterior deixou.
2. **`marca` guarda recurso?** Declare o que falta e escreva por quê - e a
   resposta **não é a mesma** para `marca` e `modo_bruto`. Uma pode ser
   copiada sem estragar nada; a outra representa um recurso único, e copiá-la
   restauraria o mesmo estado duas vezes.

## O que o roteiro 2 prova

A exceção **não pula** os destrutores: ela os chama, de dentro para fora, ao
desenrolar a pilha. É essa garantia, e nada mais, que faz RAII funcionar - e é
por isso que um `restaurar()` manual no fim da função não é equivalente.

## A pergunta de fechamento

Onde mais no seu código existe recurso que sobrevive ao processo? Arquivo com
bloqueio, socket, entrada em `/tmp`, linha em banco. Todos têm esta forma, e
nenhum deles é liberado pelo sistema operacional quando o programa morre.
