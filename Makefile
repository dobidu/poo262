# POO v2 · UFPB/CI - site e livro a partir de uma fonte única.
#
#   make            portão completo: mapa, extração conferida, contrato, site, livro
#   make site       gera poo/ a partir de conteudo/
#   make livro      gera livro/ a partir de legado/poo.docx
#   make extrai     reextrai conteudo/aulas/ do site v1  (SOBRESCREVE edições)
#   make verifica   só os portões, sem escrever nada

PY := python3

# O venv do projeto. Ele existe por três dependências que o livro impresso
# tem e o site não: `brotli` para abrir o WOFF2, `fonttools` para o subset
# geométrico, e `pymupdf` para o portão do PDF. Nenhuma entra no python do
# sistema (PEP 668), e um clone limpo as instala com `make venv`.
VENV := build/venv
PYV  := $(VENV)/bin/python

.PHONY: all verifica site livro semear-livro extrai mapa contrato codigo deriva voz medidas numeros fontes limpa

# o livro vem ANTES do site: a capa linka o PDF, e `conferir_links`
# do build_site precisa que o arquivo exista para nao reprovar
all: verifica livro livro-pdf site
	@echo "── pronto: poo/ e livro/"

mapa:
	@$(PY) conteudo/mapa.py

contrato:
	@node build/verifica_pecas.js

# O detector de voz, como portao. Regras duras
# quebram o build; sinais brandos sao relatados com --sinais.
voz:
	@$(PY) build/verifica_voz.py

sinais:
	@$(PY) build/verifica_voz.py --sinais

# O Deriva é o portão mais duro: compila com zero aviso, 188 testes verdes,
# replay idêntico byte a byte e contador de instâncias fechando em zero. É de
# lá que sai todo trecho de código do material.
deriva:
	@$(MAKE) --no-print-directory -C exemplos/deriva verifica

codigo: deriva
	@$(PY) build/extrair_codigo.py

# Mede o Deriva compilado e grava conteudo/medidas.py. Todo numero que a prosa
# afirma sai daqui.
medidas:
	@$(PY) build/medir_deriva.py --propagar

# Confere as afirmacoes numericas do material contra o que foi medido.
numeros:
	@$(PY) build/gerar_sem_marcas.py --conferir
	@$(PY) build/gerar_plano_docx.py --conferir
	@$(PY) build/verifica_numeros.py

# Mede a cobertura real das fontes e regera o subconjunto geometrico.
# Precisa de rede; roda raramente. O portao usa conteudo/glifos.py, offline.
fontes:
	@$(PY) build/medir_fontes.py

glifos:
	@$(PY) build/verifica_fontes.py

# Os portões nunca escrevem. Se algum falhar, nada é gerado.
# O arquivo que o estudante recebe na Aula 04: `gerado.hpp` sem as marcas
# `DEFEITO n`, sem a tarja que conta quantos sao, e sem o `namespace revisado`
# que traz a correcao dos tres. O cabecalho prometia isso e o arquivo nao
# existia: o exercicio era impossivel como descrito.
sem-marcas:
	@$(PY) build/gerar_sem_marcas.py

# O plano em .docx que a pagina do plano oferece para baixar. Era feito a mao,
# ficou 17 h atras do markdown, e `make limpa` o apagava sem que nada soubesse
# refaze-lo.
plano-docx:
	@$(PY) build/gerar_plano_docx.py

verifica: mapa contrato voz sem-marcas plano-docx
	@$(MAKE) --no-print-directory -C exemplos/deriva verifica
	@$(PY) build/medir_deriva.py --conferir
	@$(PY) build/gerar_sem_marcas.py --conferir
	@$(PY) build/gerar_plano_docx.py --conferir
	@$(PY) build/verifica_numeros.py
	@$(PY) build/extrair_codigo.py --conferir
	@$(PY) build/extrair_v1.py --conferir
	@$(PY) build/build_site.py --conferir
	@echo "── portões OK"

# O portao de glifos vem DEPOIS de gerar, porque e a saida que ele examina.
site: mapa
	@$(PY) build/build_site.py
	@$(PY) build/verifica_fontes.py

# Versão para estudante: sem as notas de migração destinadas ao docente.
site-limpo: mapa
	@$(PY) build/build_site.py --sem-notas
	@$(PY) build/verifica_fontes.py

# A extracao recorta o DOCX para livro/extraido/ e NAO sobrescreve
# livro/capitulos/, que e o livro de verdade. A montagem junta o que existe.
livro:
	@$(PY) build/extrair_livro.py
	@$(PY) build/montar_livro.py --docx

venv: $(PYV)

$(PYV):
	@python3 -m venv $(VENV)
	@$(VENV)/bin/pip install --quiet --upgrade pip
	@$(VENV)/bin/pip install --quiet brotli fonttools pymupdf
	@echo "venv: brotli (woff2), fonttools (subset), pymupdf (portao do PDF)"

fontes-tex: $(PYV)
	@$(PYV) build/converter_fontes.py

# O PDF de impressao e o artefato primario do livro; a versao de tela herda
# a estrutura dele. `verifica_pdf.py` confere o PDF, e nao o fonte: ele pega
# a classe de defeito que so nasce na composicao (risca, tofu, tinta fora do
# papel, carimbo sobre carimbo, linha transbordando).
livro-pdf: fontes-tex
	@$(PY) build/render_livro.py --tela
	@$(PYV) build/verifica_pdf.py

# Destrutivo: descarta a reescrita e volta ao recorte cru do DOCX.
semear-livro:
	@$(PY) build/extrair_livro.py --semear
	@$(PY) build/montar_livro.py --docx

# Reextrair NAO descarta a reescrita: o recorte fiel vai para
# conteudo/extraido/ e conteudo/aulas/ so e semeado quando o arquivo nao
# existe ou quando ninguem o tocou desde a ultima extracao.
extrai:
	@$(PY) build/extrair_v1.py

# Destrutivo: descarta a reescrita do site e volta ao recorte cru do v1.
semear-site:
	@$(PY) build/extrair_v1.py --semear

limpa:
	@rm -f poo/*.html poo/plano-de-ensino.docx
	@rm -rf build/tex build/fontes-tex livro/livro.html livro/poo-v2.pdf
	@rm -rf livro/extraido livro/livro.md livro/poo-v2.docx livro/MIGRACAO.md
	@echo "livro/capitulos e livro/anexos NAO foram apagados: sao trabalho a mao."
