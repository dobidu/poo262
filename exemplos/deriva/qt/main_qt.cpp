// v2.7 · o segundo front-end, sobre o mesmo núcleo
#include <QApplication>

#include <utility>

#include "deriva/mapa.hpp"
#include "deriva/mundo.hpp"
#include "janela.hpp"

int main(int argc, char** argv) {
  QApplication app(argc, argv);

  auto m = deriva::mapa::carregar("mapas/estacao-01.txt");
  if (!m) return 2;
  deriva::mundo w(std::move(*m));
  w.acrescentar(std::make_unique<deriva::sonda>(w.setor().entrada()));

  // Nenhuma linha do núcleo mudou para isto existir. É o argumento inteiro da
  // Aula 26, e ele só é verdade porque a v2.6 extraiu `i_apresentacao`.
  deriva::qt::janela janela(std::move(w));
  janela.resize(900, 600);
  janela.setWindowTitle("Deriva - segundo front-end");
  janela.show();
  return app.exec();
}
