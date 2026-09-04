# Deriva - o portão de correção da disciplina, numa linha de comando.
#
#   make verifica    as quatro condições: warning, ctest, replay, contadores
#
# Nenhuma delas depende de sanitizer: o laboratório não os tem. O lugar do
# ASan é a Aula 02, como ferramenta - não como critério de aceitação.

BUILD  ?= build
SEMENTE ?= 7

.PHONY: verifica configura compila testes replay contadores sanitizers gdb-dtor limpa

verifica: compila
	@$(MAKE) --no-print-directory testes
	@$(MAKE) --no-print-directory replay
	@$(MAKE) --no-print-directory contadores
	@echo "verifica: OK - 4 de 4"

configura:
	@cmake -S . -B $(BUILD) -DCMAKE_BUILD_TYPE=Debug > /dev/null

# (1) warning: zero aviso no código do estudante.
#     Não é `-Werror`: o alvo compila e depois procura "error" ou "warning" no
#     log. O efeito é o mesmo - build vermelho - e a diferença que importa é
#     que o log inteiro fica em build/compilacao.log para ser lido, em vez de
#     a compilação parar no primeiro aviso.
compila: configura
	@cmake --build $(BUILD) --parallel 2>&1 | tee $(BUILD)/compilacao.log \
	  | grep -E "^[^ ]+:[0-9]+:[0-9]+: (warning|error):|^[^ ]+:[0-9]+: (warning|error):" && \
	  { echo "verifica: FALHA (1/4 warning) - ha aviso ou erro acima"; exit 1; } || true
	@echo "  (1/4) warning     OK  zero aviso com -Wall -Wextra -Wpedantic"

# (2) testes: todos verdes.
testes:
	@ctest --test-dir $(BUILD) --output-on-failure > $(BUILD)/ctest.log 2>&1 || \
	  { cat $(BUILD)/ctest.log; echo "verifica: FALHA (2/4 testes)"; exit 1; }
	@echo "  (2/4) ctest       OK  $$(grep -c 'Passed' $(BUILD)/ctest.log) testes verdes"

# (3) replay: despejo idêntico byte a byte. É o oráculo das Aulas 16, 24 e 25.
replay:
	@./$(BUILD)/deriva --replay roteiro.txt --semente $(SEMENTE) > $(BUILD)/replay.out
	@diff -u esperado.txt $(BUILD)/replay.out > $(BUILD)/replay.diff || \
	  { cat $(BUILD)/replay.diff; echo "verifica: FALHA (3/4 replay) - a saida mudou"; exit 1; }
	@echo "  (3/4) replay      OK  identico byte a byte (semente $(SEMENTE))"

# (4) contadores: o contador de instâncias vivas fecha em zero.
contadores:
	@./$(BUILD)/deriva --replay roteiro.txt --semente $(SEMENTE) --contadores \
	  | tail -1 > $(BUILD)/contadores.out
	@grep -q '^vivos=0 ' $(BUILD)/contadores.out || \
	  { cat $(BUILD)/contadores.out; \
	    echo "verifica: FALHA (4/4 contadores) - algum destrutor nao rodou"; exit 1; }
	@echo "  (4/4) contadores  OK  $$(cat $(BUILD)/contadores.out)"

# Grava o esperado. Rodar isto é uma DECISÃO: você está dizendo que a saída
# nova é a correta. Numa refatoração, é justamente o que não se pode fazer.
esperado:
	@cmake -S . -B $(BUILD) -DCMAKE_BUILD_TYPE=Debug > /dev/null
	@cmake --build $(BUILD) --parallel > /dev/null
	@./$(BUILD)/deriva --replay roteiro.txt --semente $(SEMENTE) > esperado.txt
	@echo "esperado.txt regravado - confira o diff no git antes de aceitar"

# Ferramenta da Aula 02, não portão.
sanitizers:
	@cmake -S . -B $(BUILD)-asan -DCMAKE_BUILD_TYPE=Debug -DDERIVA_SANITIZERS=ON > /dev/null
	@cmake --build $(BUILD)-asan --parallel > /dev/null
	@./$(BUILD)-asan/deriva --replay roteiro.txt --semente $(SEMENTE) > /dev/null
	@ctest --test-dir $(BUILD)-asan --output-on-failure > /dev/null
	@echo "asan+ubsan: limpos"

# Aula 08 e 11: provar que o destrutor roda - e onde ele não roda.
gdb-dtor: compila
	@gdb -batch -ex 'break deriva::mapa::~mapa' -ex run -ex 'info locals' -ex bt \
	     -ex 'continue' --args ./$(BUILD)/deriva --render 2>&1 | head -30

limpa:
	@rm -rf $(BUILD) $(BUILD)-asan
