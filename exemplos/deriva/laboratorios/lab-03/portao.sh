#!/usr/bin/env bash
# LAB-03 · portão · prepara a Aula 4
#
# Git como registro de decisão. O portão não é "usou git": é que o histórico
# possa ser LIDO por outra pessoa e explique as decisões.
#
#   ./portao.sh /caminho/do/seu/repositorio
set -uo pipefail
repo="${1:-.}"
cd "$repo" || { echo "LAB-03: '$repo' nao existe"; exit 1; }
falhas=0
checar() { # descrição, condição já avaliada
  if [ "$2" -eq 0 ]; then printf '  OK    %s\n' "$1"
  else printf '  FALHA %s\n' "$1"; falhas=$((falhas+1)); fi
}

git rev-parse --git-dir >/dev/null 2>&1; checar "e um repositorio git" $?

# (1) Ao menos um merge de branch: o fluxo, e não só commits em fila.
n_merges=$(git log --merges --oneline 2>/dev/null | wc -l)
[ "$n_merges" -ge 1 ]; checar "ha ao menos um merge de branch ($n_merges)" $?

# (2) Nenhuma mensagem de uma palavra. "wip", "fix", "ok" nao registram nada.
curtas=$(git log --format='%s' 2>/dev/null | awk 'NF<=1' | wc -l)
[ "$curtas" -eq 0 ]; checar "nenhuma mensagem de uma palavra ($curtas encontradas)" $?

# (3) Ao menos um commit cujo CORPO explica o porquê, e não o quê.
#     O `git diff` já diz o quê; o corpo existe para o que ele não diz.
com_corpo=$(git log --format='%b' 2>/dev/null | grep -c '[[:alpha:]]')
[ "$com_corpo" -ge 1 ]; checar "ha commit com corpo explicando o porque ($com_corpo)" $?

# (4) .gitignore que cubra o que C++ produz.
if [ -f .gitignore ]; then
  grep -qE '(^|/)build' .gitignore; checar ".gitignore cobre o diretorio de build" $?
else
  checar ".gitignore existe" 1
fi

# (5) Nenhum artefato de build versionado. É o erro mais comum, e o mais caro:
#     binário no histórico não sai mais dele.
sujos=$(git ls-files 2>/dev/null | grep -cE '\.(o|a|so)$|(^|/)build/')
[ "$sujos" -eq 0 ]; checar "nenhum artefato de build versionado ($sujos)" $?

# (6) DECISAO.md, que é o que a disciplina corrige por rubrica.
[ -f DECISAO.md ]; checar "DECISAO.md existe na raiz" $?

echo
if [ "$falhas" -eq 0 ]; then echo "portao LAB-03: OK"; else
  echo "portao LAB-03: FALHA em $falhas item(ns)"; fi
exit "$falhas"
