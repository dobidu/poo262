# LAB-04 · `vetor2` e `celula`, e o contador `vivos`

**Prepara a Aula 7 · semana 4, E1**

## Portão

Nove verificações, todas OK, e `vivos` fechando em zero. Quatro TODO no
esqueleto.

## O que se aprende

**A invariante é o que justifica a classe.** A `leitura` do esqueleto promete
que a intensidade fica entre 0 e 100, e é essa promessa que a torna `class` em
vez de `struct`. Um agregado sem invariante não tem o que proteger, e
encapsulá-lo só acrescenta cerimônia - é por isso que `vetor2` é `struct` no
Deriva.

Os quatro TODO, em ordem de dor:

1. **onde a invariante é estabelecida** - no construtor, e o caminho é lançar.
2. **a cópia também é um nascimento.** O destrutor decrementa, então a cópia
   tem de incrementar. Rode sem consertar e veja `vivos` fechar **negativo**:
   o contador passa a mentir na direção que ninguém desconfia.
3. **`ajustar` também tem de validar.** A invariante vale para todo caminho que
   escreve no objeto, não só para o construtor. E depois de recusar, o objeto
   tem de ficar intacto - é garantia forte, e sai de graça aqui.
4. **`intensidade()` precisa de `const`.** Sem ele, um objeto `const` não
   consegue ser lido, e o programa deixa de compilar no primeiro uso correto.

## O número que surpreende

`criados` fecha em **2**, não em 3, apesar de haver três construções no
código. A do meio lançou de dentro da lista de inicialização: o corpo nunca
rodou, o objeto nunca existiu, e o destrutor dele também não roda. Um objeto
cujo construtor lança não é um objeto pela metade - ele não é.

## A pergunta de fechamento

Se `vivos` pode fechar negativo por causa de uma cópia esquecida, o que mais
ele não vê? A Aula 11 responde com o destrutor não virtual, e a resposta é
desconfortável.
