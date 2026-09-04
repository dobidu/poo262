# LAB-06 · O destrutor não virtual, acusado pelo contador `vivos`

**Prepara a Aula 11 · semana 6, E2**

## Portão

Provar o vazamento **sem ferramenta externa** e provar a correção. Seis
verificações, e `vivos` fechando em zero.

## Os dois TODO

1. **Uma palavra: `virtual`.** Rode antes de acrescentá-la e o portão falha
   dizendo quantos objetos ficaram vivos. Acrescente e compare. Note que o
   `unique_ptr` continuou correto o tempo todo - ele chamou `delete` no
   ponteiro que tinha, e o problema nunca foi dele.
2. **O contador está no lugar certo?** Mova-o para a base, mantendo o defeito
   do TODO 1, e rode de novo. O contador **fecha em zero** e o vazamento
   continua lá: o destrutor da base roda por todos os objetos, então ele conta
   objetos e não recursos. Um instrumento que dá resultado verde na presença do
   defeito é pior que instrumento nenhum, porque produz confiança falsa.

## Por que sem ferramenta externa

O laboratório da disciplina não tem sanitizer nem Valgrind, e isso é conteúdo.
Sem detector automático, a posse precisa ser verificável à mão - e é o que este
laboratório treina. Depois de passar, se você tiver ASan em casa, rode e veja a
ferramenta apontar a alocação que você já havia identificado.

## As duas perguntas que o portão faz ao passar

Vão para o `DECISAO.md`, e são elas que valem a discussão em aula:

- por que `vivos` fecha em zero na variante `v1.1-quebrada`, com o defeito
  presente?
- quantos avisos o compilador dá com `-Wall -Wextra -Wpedantic` quando o
  `delete` está dentro de um `unique_ptr`?

A segunda resposta é **zero**, e ela é medida: `variantes/v1.1-quebrada/LEIA-ME.md`.
