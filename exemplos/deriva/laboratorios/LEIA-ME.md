# Os 12 laboratórios preparatórios

Um laboratório é o que se faz **antes** da aula que depende dele. Cada um tem
esqueleto, solução de referência e um portão - e o portão é executável, não uma
opinião.

**Eles não valem nota**, e é essa separação que permite publicá-los com
solução. O que vale nota são os exercícios cronometrados de 30 minutos,
aplicados sem data prévia, e eles cobrem exatamente este terreno.

## Como usar

```bash
cd laboratorios/lab-04
g++ -std=c++17 -Wall -Wextra -Wpedantic -I../../include esqueleto.cpp -o meu
./meu                     # falha, e a mensagem diz o que falta
# ... resolva ...
./meu                     # o portão passa
diff <(./meu) <(../../build/laboratorios/lab_04_solucao)   # compare com a referência
```

## O portão de cada um roda no `ctest`

A solução de referência de todos os doze é compilada e executada por
`make verifica`. Solução publicada que não compila é pior que solução ausente,
e o único jeito de garantir que ela compila é compilá-la a cada build.

| id | prepara | tema | portão |
|---|---|---|---|
| LAB-01 | Aula 2 | ambiente, CMake e portões | compilar sem warning; o primeiro alvo |
| LAB-02 | Aula 3 | `string_view`, ligações estruturadas, `[[nodiscard]]` | a armadilha de tempo de vida, reproduzida e explicada |
| LAB-03 | Aula 4 | Git como registro de decisão | branch, merge e mensagem que justifica |
| LAB-04 | Aula 7 | `vetor2` e `celula`; o contador `vivos` | invariante que a classe protege; o que `const` promete |
| LAB-05 | Aula 8 | ciclo de vida e `terminal_bruto` | esquecer o destrutor e ver o terminal quebrar |
| LAB-06 | Aula 11 | o destrutor não virtual | provar o vazamento sem ferramenta externa |
| LAB-07 | Aula 13 | posse: `unique_ptr`, `shared_ptr`, o ciclo | escolher a posse por requisito |
| LAB-08 | Aula 14 | cópia versus movimento, e a origem depois | instrumentar e ler a ordem na saída |
| LAB-09 | Aula 16 | Catch2 e o replay como especificação | escrever o teste que trava a refatoração |
| LAB-10 | Aula 19 | CRTP e `contador_de_instancias<T>` | polimorfismo estático no que já foi escrito à mão |
| LAB-11 | Aula 20 | erros: exceções, `optional`, `variant` | garantia de exceção; desenrolar com destrutores |
| LAB-12 | Aula 24 | refatorar o `mundo` sem mudar um byte | invariância verificada por replay |

## A forma de cada laboratório

`esqueleto.cpp` compila e **falha o portão**, com mensagem dizendo o que falta.
Começar de algo que constrói é deliberado: quem começa de arquivo que não
compila gasta a primeira hora com erro de sintaxe em vez de com o conceito.

`solucao.cpp` é a referência. Ela não é a única resposta certa, e o portão é
que decide - se o seu programa passa no portão e você consegue explicar por
quê, ele está certo mesmo que não se pareça com esta.
