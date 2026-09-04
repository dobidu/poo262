# v1.1-quebrada - destrutor não virtual na base

**Caça ao bug 2 · semana 9 · Aula 11 (funções virtuais e classes abstratas)**

## O que está quebrado

`entidade` tem função virtual e destrutor **não** virtual. Deletar por
`entidade*` roda `~entidade()` e nunca `~sonda()`, então os 4 KB de leituras
que a derivada adquiriu vazam a cada objeto.

## O que faz esta variante valer uma semana inteira

O defeito é conhecido. O que não é óbvio é **quando o compilador avisa**, e a
resposta muda com a forma do código. Medido em g++ 13.3:

| caso | como o objeto morre | avisos |
|---|---|---|
| A | `delete e;` textual, `-Wall -Wextra -Wpedantic` | **1** (`-Wdelete-non-virtual-dtor`, no `delete`) |
| B | o mesmo delete dentro de `unique_ptr` | **0** |
| C | qualquer um dos dois, com `-Wnon-virtual-dtor` | **3**, nas declarações das classes |

Neste arquivo, que traz os dois casos, o total é **1** sem o flag e **4** com
ele. Para ver o caso B isolado, comente o bloco do caso A.

**O caso B é o achado.** Trocar o ponteiro cru por `unique_ptr` é a boa
prática que a Aula 12 ensina, e ela move o `delete` para dentro de
`std::default_delete`, num cabeçalho do sistema. O `-Wdelete-non-virtual-dtor`
não aponta para código que não é seu, e o único aviso que existia desaparece.
Código moderno, correto em tudo o mais, silenciou o diagnóstico.

O portão do Deriva liga `-Wnon-virtual-dtor` de propósito, e por isso esta é a
única variante que falha na **condição 1 de 4** e não na 2. Também é lição: o
aviso existia, e bastava pedir por ele no `CMakeLists.txt`.

## A pegadinha do contador

`vivos` **fecha em zero** aqui, e mente. O contador da variante mora na base, e
o destrutor da base roda por todos os objetos - ele conta objetos, não
recursos. Para acusar este defeito, o contador tem de morar na **derivada**, e
é assim que a v1.1 boa faz.

Descobrir esse limite é parte da lição: o instrumento da Aula 07 não é
universal, e saber o que ele não vê vale tanto quanto saber usá-lo.

## Roteiro de observação, na ordem

1. `./quebrado` - `~sonda()` roda uma vez de duas, e `vivos` fecha em zero.
2. Compile o caso B isolado com `-Wall -Wextra -Wpedantic`: nada.
3. Acrescente `-Wnon-virtual-dtor`: três avisos, e nenhum deles no `delete` -
   todos na declaração das classes, que é onde o defeito de fato está.
4. Com ASan, se houver: `LeakSanitizer` acusa 4 KB por objeto.
5. `gdb`: `break deriva_quebrada::sonda::~sonda` **não dispara** no caso B.

## O conserto

Uma palavra:

```cpp
virtual ~entidade() = default;
```

E a pergunta de fechamento: por que o padrão não faz isso por conta própria em
toda classe com função virtual? Porque destrutor virtual custa vtable, e há
classes polimórficas que ninguém deleta por ponteiro de base.
