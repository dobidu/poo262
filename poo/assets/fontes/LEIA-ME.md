# Fontes auto-hospedadas

O site v1 importava do Google Fonts por `@import` dentro do CSS, que bloqueia o
render e depende de rede. Aqui nada vem de CDN.

## IBM Plex - as três vozes

| arquivo | família | papel no material |
|---|---|---|
| `IBMPlexMono-{Regular,Medium,SemiBold}.woff2` | `--maquina` | código, moldura, rótulo, estado interno, navegação |
| `IBMPlexSerif-{Regular,Italic,SemiBold}.woff2` | `--humana` | prosa |
| `IBMPlexSans-{Regular,Medium}.woff2` | `--rotulo` | legenda de interativo e de figura |

Origem: <https://github.com/IBM/plex>, tag `v6.4.0`, diretório
`fonts/complete/woff2/`. Licença **SIL OFL 1.1**.

**Use os arquivos `complete`, não os subconjuntos `latin`.** O subconjunto
`latin` do Google Fonts vai até U+00FF mais alguns pontos avulsos, e **não tem
o bloco de box-drawing** (U+2500-257F). Como as molduras deste material são
caracteres reais, e não `border`, um subconjunto `latin` derrubaria o idioma
visual inteiro. A primeira tentativa aqui usou os arquivos do `@fontsource`, de
14 KB, e foi trocada por isso.

## DerivaGeometricos.ttf - a face suplementar

Nenhuma das três famílias Plex cobre a faixa de formas geométricas, e o
material depende de nove glifos dela como portadores semânticos ao lado da cor:

```
▲ falha      △ herança     ◆ composição   ◇ LLM        ▸ Deriva
▼ direção    ◀ ▶ navegação  ▷ alternativa
```

Sem uma face declarada para eles, cada um cairia numa fonte do sistema, com
outro peso e outro avanço, dentro de painéis alinhados por caractere.

Origem: **Noto Sans Mono Regular** (SIL OFL 1.1), subconjunto de nove glifos.
Foi escolhido por casar a métrica: avanço de **600/1000** unidades, o mesmo do
IBM Plex Mono. O DejaVu Sans Mono cobriria os mesmos glifos, mas com
602/1000 - a diferença apareceria em linha longa de moldura.

Gerado por `build/medir_fontes.py`. Para refazer:

```bash
make fontes
```

## Três glifos que ninguém cobre

`⟲` (reiniciar), `☰` (gaveta) e `⏸` (pausa) não existem no Plex nem no Noto
Sans Mono. Em vez de uma segunda face suplementar, foram trocados por
equivalentes que o Plex já traz: **`↺`**, **`▸`** e **`││`**. A troca está no
código-fonte, não em folha de estilo.

## Portão

`build/verifica_fontes.py` recusa o build se o site usar um glifo que nenhuma
face declarada cobre. A tabela de cobertura fica em `conteudo/glifos.py`,
gerada a partir dos arquivos de fonte de verdade.
