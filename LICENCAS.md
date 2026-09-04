# Licenças

Este repositório carrega três coisas com licenças diferentes: o **texto** do
material didático, o **código** que o gera e o sistema que ele ensina, e as
**fontes** de terceiro que o site e o livro incorporam.

## O texto: CC BY-SA 4.0

Vale para o material que o estudante lê, e está em [`LICENSE-TEXTO`](LICENSE-TEXTO):

| onde | o que é |
|---|---|
| `livro/capitulos/`, `livro/anexos/` | os 26 capítulos, os 3 anexos, o glossário e as referências |
| `livro/poo-v2.pdf`, `livro/livro.html` | o livro composto, nas duas versões |
| `conteudo/aulas/`, `poo/*.html` | as 38 páginas do site |
| `exemplos/deriva/diagramas/` | os diagramas em Mermaid |
| `PLANO_DE_ENSINO_POO_v2.md` e os documentos de plano | o plano da disciplina |

Adaptar exige crédito e manter a adaptação aberta sob a mesma licença.

## O código: MIT

Vale para o que executa, e está em [`LICENSE`](LICENSE):

| onde | o que é |
|---|---|
| `exemplos/deriva/` | o Deriva: as 20 versões da trilha, os testes, os 12 laboratórios e as variantes quebradas |
| `build/` | os geradores e os portões |
| `poo/js/`, `poo/css/` | os interativos e o desenho do site |
| `conteudo/*.py` | o mapa, os trechos e as medidas |

Reusar o Deriva noutra disciplina não obriga a abrir o resultado. A intenção é
essa: o sistema-base é útil fora deste curso.

## As fontes: SIL Open Font License 1.1

O repositório redistribui subconjuntos do **IBM Plex**, em
`poo/assets/fontes/`, e a licença deles não é nossa de escolher.

> Copyright © 2017 IBM Corp. with Reserved Font Name "Plex".
>
> This Font Software is licensed under the SIL Open Font License, Version 1.1.
> This license is available with a FAQ at <https://scripts.sil.org/OFL>

Origem: <https://github.com/IBM/plex>, tag `v6.4.0`. Os arquivos em
`poo/assets/fontes/*.woff2` são subconjuntos, gerados por
`build/medir_fontes.py`, e nenhum glifo foi alterado.

O `DerivaGeometricos.ttf` do mesmo diretório é um suplemento de dez glifos
geométricos que nenhuma família do Plex tem, recortado do **Noto Sans Mono**,
que também está sob SIL OFL 1.1:

> Copyright © 2022 The Noto Project Authors.
> Licensed under the SIL Open Font License, Version 1.1.

O nome interno da face é `Deriva Geometricos` de propósito: o subsetter
preservava o nome da origem, e o PDF passava a declarar uma quarta família
onde há três mais dez glifos.

## O que NÃO está aqui

O **FTXUI** e o **Catch2** não são redistribuídos: o CMake os busca por
`FetchContent`, em tag fixa, e cada um mantém a sua própria licença. O **Qt**,
quando ligado por `-DDERIVA_COM_QT=ON`, é dependência do sistema e não vem no
repositório.

## Em dúvida

O critério é simples: se o arquivo é lido por uma pessoa, é CC BY-SA; se é
executado por uma máquina, é MIT. Onde os dois se encontram - um capítulo que
contém um trecho de código extraído - o trecho segue o código, porque ele vem
de `exemplos/deriva/` e o capítulo só o exibe.
