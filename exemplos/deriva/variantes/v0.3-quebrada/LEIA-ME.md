# v0.3-quebrada - cópia rasa em `grade`

**Caça ao bug 1 · semana 5 · Aula 09 (regra do zero e do três)**

## O que está quebrado

`grade` guarda `celula*` cru, declara `~grade()` que faz `delete[]`, e **não**
declara construtor de cópia nem atribuição. A cópia gerada pelo compilador
copia o ponteiro, não o buffer: duas grades, um buffer, dois `delete[]`.

## O que o estudante deve observar, nesta ordem

1. **Sem ferramenta nenhuma.** `./quebrada` mostra que escrever em `b` mudou
   `a`, e que os dois buffers têm o mesmo endereço. Isto basta para o
   diagnóstico - e é o único caminho disponível no laboratório.
2. **Com o contador de instâncias vivas.** Acrescente `vivos` a `grade` como
   na Aula 07: ele fecha em zero, e é isso que engana. O contador conta
   objetos, não recursos - descobrir esse limite é parte da lição.
3. **Com o alocador.** Nesta máquina a própria glibc aborta com
   `free(): double free detected in tcache 2`. Não é para se confiar: o tcache
   pega *este* arranjo, e um double free separado por outras alocações passa.
   Detecção do alocador é sorte de layout.
4. **Com o ASan**, se houver: `attempting double-free`, com as duas pilhas de
   liberação nomeadas. É a confirmação com garantia - e é a diferença entre
   "abortou" e "abortou e disse onde".
5. **Com o compilador.** `-Wall -Wextra -Wpedantic` não emite uma palavra.
   Nenhum aviso existe para isto, porque a linguagem está fazendo o que foi
   pedida.

## O conserto, e por que o conserto certo é o mais curto

Escrever construtor de cópia e atribuição funciona e é o que a regra do três
manda. Mas o conserto **melhor** é apagar o destrutor: troque `celula*` por
`std::vector<celula>` e a classe volta à regra do zero, com as cinco operações
corretas de graça. É o que a `v0.3` boa faz.

A pergunta que fecha a discussão: *quantas linhas a mais a versão com
`vector` tem?* Nenhuma.

## Rodar

```bash
g++ -std=c++17 -Wall -Wextra -Wpedantic grade_quebrada.cpp -o quebrada && ./quebrada
g++ -std=c++17 -g -fsanitize=address,undefined grade_quebrada.cpp -o q-asan && ./q-asan
```
