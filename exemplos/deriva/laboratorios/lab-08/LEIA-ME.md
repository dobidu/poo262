# LAB-08 · Cópia versus movimento em `grade`, e o objeto de origem depois

**Prepara a Aula 14 · semana 8, E1**

## Portão

Instrumentar o ciclo de vida e **ler a ordem na saída**, distinguindo cópia de
movimento sem adivinhar. Sete verificações, com o traço comparado texto a
texto.

## Os dois TODO

1. **Falta `noexcept` no construtor de movimento.** Rode o caso 3 sem ele: o
   `std::vector` **copia** ao realocar em vez de mover. O motivo é a garantia
   que ele precisa dar - se mover puder lançar no meio da realocação, ele fica
   com metade dos elementos no buffer novo e nenhum jeito de voltar. Sem
   `noexcept`, ele escolhe copiar, que é reversível.
2. **O traço tem de distinguir as cinco operações.** Sem sufixo próprio para
   cada uma, ele diz que algo nasceu e não diz de onde - e é justamente essa a
   pergunta da Aula 14.

## O detalhe que o portão expõe

A última linha do traço de movimento é `-`, sem nome. O rótulo da origem foi
**movido** para o destino, então o destrutor dela não tem mais o que imprimir.
A instrumentação foi afetada pelo movimento que ela mede.

O conserto é escolha: deixar o rótulo fora do que se move, ou aceitar o traço
anônimo sabendo ler o que ele significa. Escreva no `DECISAO.md` qual você
escolheu e por quê.

## A pergunta de fechamento

Cópia duplica os bytes e o endereço muda; movimento passa o mesmo endereço
adiante. Onde, no Deriva, isso vira diferença de desempenho mensurável - e onde
não vira nada?
