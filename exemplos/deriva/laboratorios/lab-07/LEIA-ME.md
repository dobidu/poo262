# LAB-07 · Posse: `unique_ptr`, `shared_ptr` e o ciclo que vaza

**Prepara a Aula 13 · semana 7, E2**

## Portão

Escolher a posse **por requisito** (e escrever o requisito), provocar o ciclo e
desfazê-lo. Nove verificações.

## Os dois TODO

1. **Qual das duas pontas possui.** O esqueleto declara as duas como
   `shared_ptr`, e é a única combinação que vaza. Troque a de volta por
   `weak_ptr` e escreva o requisito de cada uma - a resposta não é "weak é
   melhor", é que ida e volta representam relações diferentes.
2. **Um dono, e o tempo de vida é o do dono.** O inventário do esqueleto usa
   `shared_ptr` sem precisar. Troque, e diga o que se ganha: não é
   desempenho, é que o tipo passa a **declarar** quem destrói.

## O que o caso 3 mede

Com as duas pontas possuindo, as contagens param em 2 e 2. Nenhum destrutor
roda, ninguém alcança mais aqueles objetos, e o programa termina com dois
vazados. O contador de instâncias é o que acusa - o `use_count` já era 2 antes
de sair do escopo, e olhar só para ele não revelaria nada.

## A regra de escolha, na ordem em que se pergunta

1. Precisa de mais de um dono? Se não, `unique_ptr`, e acaba aqui.
2. Precisa? Então há uma relação de volta? Se sim, ela é `weak_ptr`.
3. Ninguém possui, só observa? Ponteiro cru ou referência - e o tipo tem de
   dizer que é observação.

## A pergunta de fechamento

`shared_ptr` resolve posse compartilhada e não resolve ciclo. O que resolveria
ciclo de verdade, e por que C++ não tem isso na biblioteca padrão?
