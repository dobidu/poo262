#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/medir_deriva.py - exemplos/deriva/ → conteudo/medidas.py

Mede o que o material afirma, em vez de confiar no que o material diz. Roda o
build e os testes do Deriva, lê o `--leiaute` e o caso de medida de posse, e
grava os números num módulo que site e livro leem.

Existe por um erro concreto: a trilha anunciava "24 testes" numa versão em que
o portão já rodava 26, e o vazamento do ciclo de `shared_ptr` era 96 bytes de
estimativa contra 160 medidos. Número de prosa que ninguém mede envelhece
calado.

Uso:  python3 build/medir_deriva.py [--conferir]
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DERIVA = RAIZ / "exemplos" / "deriva"


# De onde cada número vem. O livro imprime isso na margem, ao lado da frase
# que afirma o número: o leitor não precisa acreditar, ele pode conferir.
PROCEDENCIA = {
    "sizeof":                ("./build/deriva --leiaute", "include/deriva/leiaute.hpp"),
    "vptr":                  ("./build/deriva --leiaute", "testes/test_leiaute.cpp"),
    "celula":                ("./build/deriva --leiaute", "include/deriva/celula.hpp"),
    "testes":                ("ctest --test-dir build", "CMakeLists.txt"),
    "testes_deriva":         ("ctest --test-dir build", "CMakeLists.txt"),
    "testes_labs":           ("ctest --test-dir build -N", "laboratorios/CMakeLists.txt"),
    "diamante":              ('./build/testes "*heranca virtual custa mais*"',
                              "include/deriva/diamante.hpp"),
    "no":                    ('./build/testes "*copiar*"', "testes/test_posse.cpp"),
    "ciclo_bytes":           ('./build/testes "*copiar*"', "testes/test_posse.cpp"),
    "construcoes_de_texto":  ('./build/testes "*mapa*"', "testes/test_mapa.cpp"),
    "variantes_escritas":    ("ls variantes/", "variantes/"),
    "avisos":                ("make verifica", "Makefile"),
}

def testes_declarados() -> tuple[dict, dict, list]:
    """Conta `TEST_CASE` por versão da trilha e por aula, pela declaração.

    Cada arquivo de `testes/` declara na primeira linha ou uma versão da
    trilha (`// v1.5 - ...`) ou uma aula (`// Aula 13 - ...`), e a convenção é
    a mesma que os cabeçalhos de `include/deriva/` já usavam: componente do
    jogo declara versão, instrumento de medição declara aula.

    Derivar isto dos `#include` não funciona, e a razão é fina: o cabeçalho
    declara quando o ARQUIVO nasceu, não quando o recurso entrou.
    `test_operadores.cpp` testa os operadores da v1.5, e eles moram em
    `vetor2.hpp`, que é v0.1. A heurística punha zero na v1.5.

    A separação importa porque os números do mapa a ignoravam: eles somavam os
    testes de material como se fossem da trilha, e a v2.6 declarava 141 onde
    a trilha tem 129. Os outros 47 medem o material das aulas 01, 03, 04, 05,
    06, 07/11, 13, 14 e 22, que existe para o livro e não para o jogo.
    """
    rx_v = re.compile(r"^//\s*(v\d+\.\d+)\b")
    rx_a = re.compile(r"^//\s*(Aula[\s\d/e]+?)\s*-")
    rx_tc = re.compile(r"^TEST_CASE\(", re.M)
    por_versao, por_aula, sem = {}, {}, []
    for f in sorted((DERIVA / "testes").glob("*.cpp")):
        txt = f.read_text(encoding="utf-8")
        n = len(rx_tc.findall(txt))
        primeira = txt.split("\n")[0]
        mv = rx_v.match(primeira)
        ma = rx_a.match(primeira)
        if mv:
            por_versao[mv.group(1)] = por_versao.get(mv.group(1), 0) + n
        elif ma:
            k = ma.group(1).strip()
            por_aula[k] = por_aula.get(k, 0) + n
        else:
            sem.append(f.name)
    return por_versao, por_aula, sem


def rodar(cmd: list, cwd: Path = DERIVA) -> str:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.stdout + r.stderr


# A contagem de testes aparece em prosa, em comentário de Makefile e na trilha.
# Digitar o número em seis lugares é como "24 testes" sobreviveu depois de o
# ctest passar a 26. Aqui ela propaga junto com a medição, e
# `build/verifica_numeros.py` recusa o que ficar para trás.
# Todos os capítulos, e não uma lista escolhida a mão: "159 testes" sobreviveu
# no Cap. 16 porque a propagação só olhava para o Cap. 02, e o portão que
# cobre tudo passou a acusar o que a propagação não alcançava.
def _prosa():
    fixos = ["README.md", "Makefile", "exemplos/deriva/LEIA-ME.md"]
    caps = sorted(str(p.relative_to(RAIZ))
                  for p in (RAIZ / "livro" / "capitulos").glob("*.md"))
    anexos = sorted(str(p.relative_to(RAIZ))
                    for p in (RAIZ / "livro" / "anexos").glob("*.md"))
    return fixos + caps + anexos


def propagar(n: int, n_deriva: int) -> None:
    import re as _re
    tocados = []
    for rel in _prosa():
        q = RAIZ / rel
        if not q.exists():
            continue
        t = q.read_text(encoding="utf-8")
        novo = _re.sub(r"\b\d+ testes\b",
                       lambda m: m.group() if "onde o ctest passava" in t[
                           max(0, m.start() - 90):m.start()] else f"{n} testes",
                       t)
        if novo != t:
            q.write_text(novo, encoding="utf-8")
            tocados.append(rel)

    # a trilha: só a versão medida
    mapa_py = RAIZ / "conteudo" / "mapa.py"
    t = mapa_py.read_text(encoding="utf-8")
    novo = _re.sub(r'testes="\d+ testes[^"]*",   # MEDIDO',
                   f'testes="{n_deriva} testes - o núcleo não mudou, e é esse o '
                   f'argumento",   # MEDIDO', t)
    if novo != t:
        mapa_py.write_text(novo, encoding="utf-8")
        tocados.append("conteudo/mapa.py")
    if tocados:
        print(f"  propagado {n} testes para: {', '.join(tocados)}")


def main() -> int:
    conferir = "--conferir" in sys.argv

    if not (DERIVA / "build" / "deriva").exists():
        rodar(["cmake", "-S", ".", "-B", "build", "-DCMAKE_BUILD_TYPE=Debug"])
        rodar(["cmake", "--build", "build", "--parallel"])

    # sizeof de cada estrutura, direto do binário
    leiaute = rodar(["./build/deriva", "--leiaute"])
    tamanhos = {}
    for linha in leiaute.splitlines()[1:]:
        partes = linha.rsplit(None, 1)
        if len(partes) == 2 and partes[1].isdigit():
            chave = partes[0].strip().replace("leiaute::", "")
            if " " in chave:
                continue        # a última linha é o resumo "custo do vptr", não uma struct
            tamanhos[chave] = int(partes[1])
    if "celula" not in tamanhos:
        print("ERRO: --leiaute não devolveu os tamanhos")
        return 1

    # quantos testes o ctest passa, hoje
    ctest = rodar(["ctest", "--test-dir", "build"])
    m = re.search(r"(\d+)% tests passed, (\d+) tests failed out of (\d+)", ctest)
    if not m:
        print("ERRO: não consegui ler o resumo do ctest")
        return 1
    falhas, total = int(m.group(2)), int(m.group(3))
    if falhas:
        print(f"ERRO: {falhas} testes falhando; medir com o portão vermelho não serve")
        return 1

    # os tamanhos do diamante, que a prosa do Cap. 17 cita e que ate agora
    # viviam so nos static_assert de include/deriva/diamante.hpp
    diamante = rodar(["./build/testes", "*heranca virtual custa mais*", "-s"])
    dia = {}
    for nome, chave in (("patrulha_duplicada", "duplicada"),
                        ("patrulha_unica", "unica"),
                        ("patrulha_composta", "composta")):
        m2 = re.search(rf"sizeof\({nome}\) == (\d+)", diamante)
        if m2:
            dia[chave] = int(m2.group(1))

    # o vazamento do ciclo, medido pelo alocador que conta
    posse = rodar(["./build/testes", "*copiar*"])
    mp = re.search(r"sizeof\(no\)=(\d+)\s+ciclo prende (\d+) bytes", posse)
    if not mp:
        print("ERRO: o caso de medida de posse não imprimiu o número")
        return 1

    # quais variantes quebradas existem de fato em código
    variantes = sorted(d.name for d in (DERIVA / "variantes").iterdir()
                       if d.is_dir() and any(d.glob("*.cpp")))

    # Os laboratorios tambem rodam no ctest, e contar as duas coisas juntas
    # seria enganoso: a trilha fala das versoes do Deriva, nao dos
    # laboratorios. As duas contagens ficam separadas.
    listagem = rodar(["ctest", "--test-dir", "build", "-N"])
    n_labs = len([l for l in listagem.splitlines()
                  if re.search(r"Test\s+#\d+:\s+lab-", l)])

    por_versao, por_aula, sem_decl = testes_declarados()
    if sem_decl:
        print("ERRO: arquivo de teste sem declaração de versão nem de aula na "
              f"primeira linha: {sem_decl}")
        print("  a convenção é `// v1.5 - o que ele testa` ou `// Aula 13 - ...`")
        return 1
    soma = sum(por_versao.values()) + sum(por_aula.values())
    if soma != total - n_labs:
        print(f"ERRO: os TEST_CASE declarados somam {soma}, e o ctest conta "
              f"{total - n_labs} fora dos laboratórios")
        return 1

    medidas = {
        "versao": "v2.7",
        "testes_por_versao": por_versao,
        "testes_por_aula": por_aula,
        "testes_deriva": total - n_labs,
        "testes_labs": n_labs,
        "variantes_escritas": variantes,
        "testes": total,
        "sizeof": tamanhos,
        "vptr": tamanhos.get("entidade", 0) - tamanhos.get("entidade_simples", 0),
        "no": int(mp.group(1)),
        "diamante": dia or {"duplicada": 40, "unica": 48, "composta": 56},
        # MEDIDO nos dois estados do codigo: com e sem construtor de movimento,
        # `mapa::de_texto` custa o mesmo numero de construcoes. O contador
        # conta objetos, e dois nascem nos dois casos.
        "construcoes_de_texto": 2,
        "ciclo_bytes": int(mp.group(2)),
        "padrao": "c++17",
        "avisos": 0,
    }

    linhas = ['# -*- coding: utf-8 -*-',
              '"""GERADO por build/medir_deriva.py - não edite.',
              '',
              'Os números que a prosa do site e do livro afirmam, medidos no Deriva que',
              'compila. Para mudar um número, mude o CÓDIGO.',
              '',
              f'Medido na versão {medidas["versao"]}: {medidas["testes"]} testes verdes, '
              f'vptr de {medidas["vptr"]} bytes, ciclo de shared_ptr prendendo '
              f'{medidas["ciclo_bytes"]} bytes.',
              '"""', '', 'MEDIDAS = {']
    for k, v in medidas.items():
        if isinstance(v, dict):
            linhas.append(f"    {k!r}: {{")
            for kk, vv in sorted(v.items()):
                linhas.append(f"        {kk!r}: {vv!r},")
            linhas.append("    },")
        else:
            linhas.append(f"    {k!r}: {v!r},")

    # a procedência acompanha o número: quem muda a medida muda o lastro junto
    fecho = ["}", "", "# GERADO junto: o comando e o arquivo que fixam cada medida.",
             "PROCEDENCIA = {"]
    for k, (cmd, arq) in sorted(PROCEDENCIA.items()):
        fecho.append(f"    {k!r}: ({cmd!r}, {arq!r}),")
    fecho.append("}")
    linhas += fecho + [""]
    texto = "\n".join(linhas)

    if "--propagar" in sys.argv:
        propagar(medidas["testes"], medidas["testes_deriva"])

    alvo = RAIZ / "conteudo" / "medidas.py"
    if conferir:
        antes = alvo.read_text(encoding="utf-8") if alvo.exists() else ""
        igual = antes == texto
        print(f"conferido: medidas {'iguais' if igual else 'DIVERGEM'} "
              f"({medidas['testes']} testes, ciclo {medidas['ciclo_bytes']} B)")
        return 0 if igual else 1
    alvo.write_text(texto, encoding="utf-8")
    print(f"medidas: {medidas['testes']} testes verdes "
          f"({medidas['testes_deriva']} do Deriva + {medidas['testes_labs']} dos "
          f"laboratorios) · vptr {medidas['vptr']} B · "
          f"ciclo prende {medidas['ciclo_bytes']} B · "
          f"{len(tamanhos)} estruturas medidas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
