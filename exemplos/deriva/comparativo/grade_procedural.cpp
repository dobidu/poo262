#include "grade_procedural.hpp"

namespace deriva::comparativo {

grade_c criar(int largura, int altura) {
  grade_c g;
  g.largura = largura;
  g.altura = altura;
  // `malloc` devolve `void*` e pode devolver nulo. Quem chama tem de conferir,
  // e quase nunca confere - o compilador não obriga.
  g.celulas = static_cast<char*>(std::calloc(
      static_cast<std::size_t>(largura) * static_cast<std::size_t>(altura),
      sizeof(char)));
  return g;
}

void destruir(grade_c* g) {
  std::free(g->celulas);
  g->celulas = nullptr;   // higiene que ninguém obriga, e que evita a segunda
                          // liberação virar corrupção em vez de erro
}

char em(const grade_c* g, int x, int y) {
  // Sem verificação de limite: acrescentá-la aqui custaria em todo acesso, e
  // a versão C++ resolve isso com duas funções, uma que confere e outra que
  // não. Aqui há uma só, e ela escolhe errado para alguém.
  return g->celulas[static_cast<std::size_t>(y) * static_cast<std::size_t>(g->largura) +
                    static_cast<std::size_t>(x)];
}

void escrever(grade_c* g, int x, int y, char c) {
  g->celulas[static_cast<std::size_t>(y) * static_cast<std::size_t>(g->largura) +
             static_cast<std::size_t>(x)] = c;
}

int maneiras_de_errar_em_c() {
  // 1 esquecer criar · 2 esquecer destruir · 3 destruir duas vezes
  // 4 copiar a struct e destruir as duas · 5 mexer em largura depois
  // 6 indexar fora · 7 ignorar o nulo do calloc
  return 7;
}

int maneiras_de_errar_em_cpp() {
  // O construtor obriga (1 e 7 somem), o destrutor é chamado pelo escopo (2 e
  // 3 somem), a regra do zero faz a cópia ser profunda (4 some), `largura_` é
  // privado e const-correcto (5 some), e `dentro()` mais o par const/não-const
  // de `em()` deixam a escolha do custo com quem chama (6 fica, e é o único
  // que fica).
  return 1;
}

}  // namespace deriva::comparativo
