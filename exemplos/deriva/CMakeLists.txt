# Deriva · POO UFPB - CMake que a Aula 02 ensina, sem nada além do necessário.
cmake_minimum_required(VERSION 3.16)
project(deriva LANGUAGES CXX VERSION 0.3.0)

# C++17 é o teto e o foco da disciplina. `CXX_EXTENSIONS OFF` desliga as
# extensões GNU: código que só compila com -std=gnu++17 não é C++17.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Debug CACHE STRING "" FORCE)
endif()

option(DERIVA_SANITIZERS "Compilar com ASan e UBSan" OFF)
option(DERIVA_TESTES     "Compilar os testes (baixa o Catch2)" ON)
option(DERIVA_COM_FTXUI  "Camada de terminal com FTXUI v5.0.0" OFF)
option(DERIVA_COM_QT     "Segundo front-end em Qt6 (Aula 26)" OFF)
option(DERIVA_COM_CPP20  "Alvo opcional de C++20 do Anexo A" OFF)

# ---------------------------------------------------------------------------
# o núcleo: nada de UI aqui dentro. É esta separação que faz o argumento do
# segundo front-end (Aula 26) fechar - e ela existe desde a v0.2.
# ---------------------------------------------------------------------------
add_library(deriva_nucleo
  src/contador.cpp
  src/instrumento.cpp
  src/grade.cpp
  src/mapa.cpp
  src/entidade.cpp
  src/mundo.cpp
  src/estacao.cpp
  src/fov.cpp
  src/reparadora.cpp
  src/inspetor.cpp
  src/erro.cpp
  src/inventario.cpp
  src/partida.cpp
  src/fila_de_comandos.cpp
  src/apresentacao.cpp
  src/padroes.cpp
  src/solid.cpp
  comparativo/grade_procedural.cpp
  tipos/despacho.cpp
  src/terminal_bruto.cpp
)
target_include_directories(deriva_nucleo PUBLIC include)
find_package(Threads REQUIRED)
target_link_libraries(deriva_nucleo PUBLIC Threads::Threads)

# O portão de zero warning incide sobre ISTO, e só. Dependência de terceiro
# entra como SYSTEM mais abaixo, justamente para que o aviso dela não conte -
# e para que ninguém se esconda atrás dela.
target_compile_options(deriva_nucleo PRIVATE
  -Wall -Wextra -Wpedantic -Wshadow -Wnon-virtual-dtor -Wold-style-cast
  -Wcast-align -Wunused -Woverloaded-virtual -Wconversion -Wsign-conversion
  -Wdouble-promotion -Wformat=2
)

if(DERIVA_SANITIZERS)
  target_compile_options(deriva_nucleo PUBLIC -fsanitize=address,undefined -fno-omit-frame-pointer -g)
  target_link_options(deriva_nucleo PUBLIC -fsanitize=address,undefined)
endif()

# ---------------------------------------------------------------------------
# O codigo gerado por IA da Aula 04, com os tres defeitos plantados.
#
# Ele mora num alvo SEPARADO por uma razao que e ela mesma conteudo: o defeito
# 2 e um destrutor nao virtual, e `-Wnon-virtual-dtor` esta ligado no portao
# do nucleo. Um arquivo que existe para CARREGAR um defeito nao pode ficar sob
# a bandeira que o detecta, ou o portao passa a recusar o material didatico.
#
# A supressao e local, declarada, e vale so aqui. E o mesmo gesto que um
# projeto de verdade usa para esconder problema - com a diferenca de que aqui
# o motivo esta escrito e o escopo e um arquivo.
# ---------------------------------------------------------------------------
add_library(deriva_revisao revisao_ia/gerado.cpp)
target_include_directories(deriva_revisao PUBLIC include revisao_ia)
target_compile_options(deriva_revisao PRIVATE
  -Wall -Wextra -Wpedantic -Wno-non-virtual-dtor)

add_executable(deriva src/main.cpp)
target_link_libraries(deriva PRIVATE deriva_nucleo)
target_compile_options(deriva PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion)

# ---------------------------------------------------------------------------
# FTXUI - opcional e FIXO em v5.0.0.
# v5.0.0 declara target_compile_features(... cxx_std_17): alinhada ao alvo.
# As v6/v7 podem elevar o padrão exigido, então a tag não flutua.
# ---------------------------------------------------------------------------
if(DERIVA_COM_FTXUI)
  include(FetchContent)
  FetchContent_Declare(ftxui
    GIT_REPOSITORY https://github.com/ArthurSonzogni/FTXUI.git
    GIT_TAG v5.0.0
    GIT_SHALLOW TRUE
    SYSTEM
  )
  FetchContent_MakeAvailable(ftxui)
  target_link_libraries(deriva PRIVATE ftxui::screen ftxui::dom)
  target_compile_definitions(deriva PRIVATE DERIVA_COM_FTXUI=1)
endif()

# ---------------------------------------------------------------------------
# Anexo A · o alvo de C++20, em ALVO SEPARADO e com padrao proprio.
#
# `CXX_STANDARD 20` aqui e so aqui: o nucleo continua em C++17, e e essa
# separacao que faz o Anexo A existir sem que nenhum exemplo obrigatorio passe
# a exigir C++20. Ligar isto nao muda uma linha de `deriva_nucleo`.
# ---------------------------------------------------------------------------
if(DERIVA_COM_CPP20)
  add_executable(deriva_c20 c20/main_c20.cpp)
  target_include_directories(deriva_c20 PRIVATE include c20)
  set_target_properties(deriva_c20 PROPERTIES CXX_STANDARD 20 CXX_EXTENSIONS OFF)
  target_compile_options(deriva_c20 PRIVATE -Wall -Wextra -Wpedantic)
  if(DERIVA_TESTES)
    add_test(NAME anexo-a-cpp20 COMMAND deriva_c20)
  endif()
endif()

# ---------------------------------------------------------------------------
# v2.7 · Qt - o SEGUNDO front-end, e a prova de que o nucleo nao muda.
#
# Desligado por padrao: a Aula 26 e demonstracao do docente com esqueleto
# publicado, sem entrega obrigatoria, e o laboratorio nao tem Qt instalado.
# O que importa e que ligar isto nao altera uma linha de `deriva_nucleo`.
# ---------------------------------------------------------------------------
if(DERIVA_COM_QT)
  set(CMAKE_AUTOMOC ON)   # o MOC gera o codigo que Q_OBJECT exige
  find_package(Qt6 REQUIRED COMPONENTS Widgets)
  add_executable(deriva_qt qt/main_qt.cpp qt/janela.cpp)
  target_include_directories(deriva_qt PRIVATE qt)
  target_link_libraries(deriva_qt PRIVATE deriva_nucleo Qt6::Widgets)
  target_compile_options(deriva_qt PRIVATE -Wall -Wextra -Wpedantic)
endif()

# ---------------------------------------------------------------------------
# testes
# ---------------------------------------------------------------------------
if(DERIVA_TESTES)
  include(FetchContent)
  FetchContent_Declare(Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG v3.5.2
    GIT_SHALLOW TRUE
    SYSTEM
  )
  FetchContent_MakeAvailable(Catch2)

  enable_testing()
  add_executable(testes
    testes/test_vetor2.cpp
    testes/test_celula.cpp
    testes/test_grade.cpp
    testes/test_mapa.cpp
    testes/test_ciclo_de_vida.cpp
    testes/test_leiaute.cpp
    testes/test_posse.cpp
    testes/test_string_view.cpp
    testes/test_move_string.cpp
    testes/test_corrida.cpp
    testes/test_entidade.cpp
    testes/test_mundo.cpp
    testes/test_estacao.cpp
    testes/test_operadores.cpp
    testes/test_fov.cpp
    testes/test_diamante.cpp
    testes/test_inspetor.cpp
    testes/test_generico.cpp
    testes/test_erro.cpp
    testes/test_inventario.cpp
    testes/test_partida.cpp
    testes/test_concorrencia.cpp
    testes/test_padroes.cpp
    testes/test_comparativo.cpp
    testes/test_revisao_ia.cpp
    testes/test_tipos.cpp
    testes/test_uml.cpp
    testes/test_encaminhamento.cpp
    testes/test_padroes_extra.cpp
    testes/test_solid.cpp
  )
  find_package(Threads REQUIRED)
  target_link_libraries(testes PRIVATE deriva_nucleo deriva_revisao Catch2::Catch2WithMain Threads::Threads)
  # o teste do codigo gerado inclui o cabecalho com o defeito plantado
  target_compile_options(testes PRIVATE -Wall -Wextra -Wpedantic -Wno-non-virtual-dtor)

  include(CTest)
  include(Catch)
  catch_discover_tests(testes)

  # Os doze laboratorios, com a solucao de referencia verificada a cada build.
  add_subdirectory(laboratorios)
endif()
