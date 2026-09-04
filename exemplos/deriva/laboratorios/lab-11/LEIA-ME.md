# LAB-11 · Erros no carregamento de mapa: exceções, `optional` e `variant`

**Prepara a Aula 20 · semana 11, E2**

## Portão

Garantia de exceção **declarada e cumprida**, e o desenrolar da pilha chamando
os destrutores de dentro para fora.

## O TODO

`alvo = std::get<std::string>(r);` dá garantia **básica**: se algo lançar no
meio, o objeto fica válido mas pela metade. Troque por copiar-e-trocar e
explique a diferença por escrito.

```cpp
std::string novo = std::get<std::string>(r);   // pode lançar: o alvo nem foi tocado
alvo.swap(novo);                                // não lança: a troca é o ponto sem volta
```

O que se compra é a garantia **forte**: ou o alvo fica com o conteúdo novo, ou
fica exatamente como estava. E o preço é uma cópia a mais - declare no
`DECISAO.md` se ela vale, e para qual tamanho de dado deixaria de valer.

## As três formas, e o critério

| forma | para quê | por que não as outras |
|---|---|---|
| `std::optional` | **ausência** | não é erro, é resposta - o arquivo não existir é caso normal |
| `std::variant` | **erro esperado com informação** | quem chama precisa da razão para decidir, e acontece no fluxo normal |
| exceção | o que **rompe** a operação | quem chama não tem o que decidir, e o desenrolar é a resposta certa |

## O que o último caso prova

A exceção **não pula** os destrutores. Ela os chama, de dentro para fora, e é
essa garantia que faz RAII funcionar sob exceção - o mesmo argumento da Aula 8,
agora do outro lado.

## A pergunta de fechamento

Onde no Deriva a garantia forte é gratuita, e onde ela custaria uma cópia do
mapa inteiro? A resposta muda a decisão, e é ela que vai no `DECISAO.md`.
