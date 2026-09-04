# Os doze laboratorios. A solucao de referencia de cada um e COMPILADA e
# EXECUTADA pelo ctest, e e isso que faz "publicado com solucao" ser
# verificavel: solucao publicada que nao compila e pior que solucao ausente.
#
# O esqueleto NAO e compilado aqui de proposito - ele falha o portao por
# construcao, e um alvo que falha nao serve de portao.

set(LABS 01 02 04 05 06 07 08 09 10 11 12)   # 03 e de Git, e tem portao.sh

foreach(lab IN LISTS LABS)
  add_executable(lab_${lab}_solucao lab-${lab}/solucao.cpp)
  target_include_directories(lab_${lab}_solucao PRIVATE ${CMAKE_SOURCE_DIR}/include)
  target_compile_options(lab_${lab}_solucao PRIVATE
    -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion)
  add_test(NAME lab-${lab} COMMAND lab_${lab}_solucao)
endforeach()

# O portao do LAB-03 e um script, e o teste dele confere que ele RECUSA um
# diretorio que nao e repositorio git - senao passaria por vacuidade.
add_test(NAME lab-03-recusa-nao-repo
         COMMAND ${CMAKE_COMMAND} -E env bash
                 ${CMAKE_CURRENT_SOURCE_DIR}/lab-03/portao.sh /tmp)
set_tests_properties(lab-03-recusa-nao-repo PROPERTIES WILL_FAIL TRUE)
