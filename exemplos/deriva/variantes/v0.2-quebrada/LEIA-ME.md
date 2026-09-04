# v0.2-quebrada - `terminal_bruto` sem destrutor

**Aula 08 · RAII com consequência física**

## O que está quebrado

O construtor põe o terminal em modo bruto. Não há destrutor. O estado do
terminal é um recurso do sistema operacional, e ele **sobrevive ao processo**.

## Por que esta é a melhor demonstração de RAII que existe

Porque não é metáfora. Vazar memória é abstrato: o sistema operacional
devolve tudo quando o processo morre, e o estudante nunca sente. Vazar o modo
do terminal significa que a próxima coisa que ele digitar não vai aparecer na
tela - e o conserto é `reset` seguido de Enter, digitado às cegas.

Nenhuma ferramenta acusa este vazamento. ASan não conhece `termios`. O
contador de instâncias vivas acusa **um objeto** sem destrutor, e é a única
pista automática disponível.

## Como rodar sem estragar sua sessão

```bash
g++ -std=c++17 -Wall -Wextra -Wpedantic terminal_quebrado.cpp -o quebrado
./quebrado < /dev/null    # sem tty: seguro, e o contador ainda acusa
./quebrado                # com tty: quebra o terminal. é o ponto.
```

Numa sala de aula, o roteiro é: rodar com `< /dev/null` primeiro, ler o
contador, e só então rodar de verdade num terminal que se possa perder.

## O conserto

Três linhas, e é exatamente a v0.2 boa:

```cpp
~terminal_bruto() {
  if (ativo_) ::tcsetattr(STDIN_FILENO, TCSAFLUSH, &salvo_);
  --contador_terminal::vivos;
}
```

E a pergunta que fecha: onde mais no seu código existe recurso que sobrevive
ao processo? Arquivo aberto com bloqueio, socket, entrada em `/tmp`, linha em
banco de dados. Todos têm a mesma forma.
