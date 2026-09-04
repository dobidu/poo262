# v2.6-antes - o `mundo` como god class

**Caça ao bug 3 · semana 13 · Aula 24 (SOLID e invariância de comportamento)**

## O que está "quebrado"

Nada, e é esse o ponto. Esta versão compila sem aviso, roda, e faz tudo o que
a refatorada faz. O defeito não é funcional: a classe tem **sete motivos
independentes para mudar**.

| # | responsabilidade | o que ela impede |
|---|---|---|
| 1 | estado do domínio | - |
| 2 | render, direto em `std::cout` | trocar por Qt sem editar esta classe; testar sem capturar a saída do processo |
| 3 | entrada, num `switch` | desfazer, porque não há onde guardar o que foi feito |
| 4 | IA, com `dynamic_cast` por tipo | acrescentar comportamento sem tocar aqui |
| 5 | log, abrindo arquivo aqui dentro | testar o log sem mexer no sistema de arquivos |
| 6 | persistência, formato incluído | versionar o save sem risco para o resto |
| 7 | criação de entidade, terceira tabela de glifos | acrescentar entidade sem editar três lugares |

## A caça não é "ache o erro"

É: **refatore sob SOLID e prove que a saída não mudou.** O erro que a semana 13
caça é a refatoração que muda o comportamento sem que ninguém note - e a prova
é o replay, despejo idêntico byte a byte.

```bash
g++ -std=c++17 -Wall -Wextra -Wpedantic mundo_god_class.cpp -o antes
./antes > /tmp/antes.txt
# refatore para as interfaces da v2.6, e então:
diff /tmp/antes.txt <(./depois)
```

Um `diff` vazio é a única evidência aceita. Teste verde não basta: os testes
que acompanham esta variante passam nas duas versões, e é por isso que eles
não são o oráculo.

## A ordem é cobrada

1. **Estenda o roteiro primeiro.** O replay só prova o que o roteiro exercita;
   refatorar e depois escrever o teste é escrever o teste que passa.
2. Extraia **uma** responsabilidade por vez, rodando o `diff` a cada passo.
   Quem extrai três e depois compara não sabe qual das três mudou a saída.
3. A ordem que menos dói: log (5) → render (2) → criação (7) → entrada (3) →
   IA (4) → persistência (6). O estado do domínio (1) é o que sobra, e é o que
   o `mundo` deveria ter sido desde o começo.

## O que a refatoração NÃO deve fazer

Melhorar a saída. Corrigir o alinhamento do render, acrescentar uma linha ao
save, mudar a ordem das entidades no despejo: tudo isso é melhoria, e nenhuma
delas cabe aqui. Refatoração e melhoria na mesma passada é como se perde a
capacidade de saber qual das duas quebrou o programa.

## Onde está a versão refatorada

`include/deriva/apresentacao.hpp` e `src/apresentacao.cpp`, com as interfaces
`i_apresentacao`, `i_comando`, `i_observador`, a fábrica por glifo e a
estratégia por lambda. `testes/test_padroes.cpp` prova que o desfazer em
cadeia devolve o despejo byte a byte ao estado inicial - o mesmo critério que
esta caça cobra.
