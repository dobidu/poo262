// v1.6 · Aula 16 - campo de visão determinístico, e portanto testável
#ifndef DERIVA_FOV_HPP
#define DERIVA_FOV_HPP

#include <set>
#include <string>
#include <vector>

#include "deriva/mapa.hpp"
#include "deriva/vetor2.hpp"

namespace deriva {

/// O que a sonda vê a partir de uma posição, num raio.
///
/// A escolha de projeto que faz esta função existir separada: ela é **pura**.
/// Recebe mapa, origem e raio, devolve o conjunto de células visíveis, e não
/// toca em nada. Função pura é testável sem montar o mundo, sem terminal e
/// sem entrada - e é por isso que o campo de visão é o primeiro alvo dos
/// testes da Aula 16, e não o último.
///
/// O algoritmo é linha de visão por interpolação inteira de Bresenham: para
/// cada célula do quadrado do raio, caminha da origem até ela e para na
/// primeira parede. Não é o FOV mais bonito que existe; é determinístico, e é
/// isso que o replay exige.
[[nodiscard]] std::set<vetor2> visiveis(const mapa& m, vetor2 origem, int raio);

/// A linha de visão de `a` até `b`, inclusive, parando na primeira parede.
/// Exposta porque é o que o teste examina quando `visiveis` discorda do
/// esperado.
[[nodiscard]] std::vector<vetor2> linha(vetor2 a, vetor2 b);

/// O setor desenhado com o que não se vê apagado. Determinístico.
[[nodiscard]] std::string despejar_fov(const mapa& m, vetor2 origem, int raio);

}  // namespace deriva

#endif
