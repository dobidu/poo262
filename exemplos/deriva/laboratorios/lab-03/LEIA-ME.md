# LAB-03 · Git como registro de decisão

**Prepara a Aula 4 · semana 2, E2**

## Portão

`./portao.sh /caminho/do/seu/repo` sem falha. Seis condições, e nenhuma delas
é sobre saber os comandos.

## O que se aprende

Que o histórico é para ser **lido**. O `git diff` já diz o que mudou; a
mensagem existe para o que ele não diz - por que aquela decisão, e o que foi
descartado.

As três condições que mais reprovam:

- **nenhuma mensagem de uma palavra.** `wip`, `fix`, `ok` não registram nada, e
  em três meses o autor também não lembra;
- **ao menos um commit com corpo** explicando o porquê. Assunto em uma linha,
  linha em branco, corpo. É convenção, e ela existe porque as ferramentas a
  usam;
- **nenhum artefato de build versionado.** É o erro mais comum e o mais caro:
  binário que entra no histórico não sai mais dele.

## Por que este laboratório não tem C++

Porque o objeto de estudo é o registro, não o programa. O repositório que você
vai conferir é o do seu Deriva, e o `DECISAO.md` que o portão exige é o mesmo
que acompanha toda entrega da disciplina.

## A pergunta de fechamento

Abra o histórico de um projeto seu de outro semestre. Você consegue dizer, sem
ler o código, por que alguma decisão foi tomada? Se não, o histórico é registro
de digitação e não de decisão.
