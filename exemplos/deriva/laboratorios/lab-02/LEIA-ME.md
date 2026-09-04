# LAB-02 · C++17 na prática: `string_view`, ligações estruturadas, `[[nodiscard]]`

**Prepara a Aula 3 · semana 2, E1**

## Portão

Os quatro casos de tempo de vida reproduzidos e explicados por escrito, e
`portao LAB-02: OK`. **Nenhum deles lê memória liberada** - demonstrar
comportamento indefinido é trocar a lição por um programa que às vezes passa.

## Os quatro casos

1. **A vista aponta, não possui.** `data()` e `size()` iguais aos do dono, e
   nenhuma cópia. `sizeof(string_view)` são 16 bytes: um ponteiro e um tamanho.
2. **`substr` de vista não copia.** De `std::string`, aloca; de
   `string_view`, aponta para dentro do original. É a diferença que faz
   `mapa::de_texto` receber vista em vez de string.
3. **A vista não termina em nul.** `strlen(prefixo.data())` devolve o tamanho
   do **dono**, não o da vista. Para API de C o caminho é
   `std::string(vista)`, que copia de propósito - e aí o custo está declarado.
4. **O que a função guarda tem de possuir.** O TODO 4 do esqueleto declara
   `nome` como `string_view`, e ele está errado: o membro sobrevive à chamada
   que o inicializou. Troque para `std::string` e explique por escrito por que
   o programa **passaria** na maioria das execuções com o tipo errado - é essa
   a parte que o exercício cobra.

## O que mais entra

Ligação estruturada sobre `std::map`, com `const auto&` e não `auto`, e o
`[[nodiscard]]` em função que devolve status.

## A pergunta de fechamento

Se o caso 4 passa quase sempre com o tipo errado, o que o teria pegado? A
resposta não é "mais testes".
