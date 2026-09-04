#include "janela.hpp"

#include <QAction>
#include <QFont>
#include <QMenuBar>
#include <QString>

#include <utility>

namespace deriva::qt {

void tela_qt::desenhar(const mundo& m) {
  alvo_->setPlainText(QString::fromStdString(m.despejar()));
}

void tela_qt::mensagem(std::string_view texto) {
  alvo_->appendPlainText(QString::fromStdString(std::string("> ") + std::string(texto)));
}

janela::janela(mundo w, QWidget* pai)
    : QMainWindow(pai), mundo_(std::move(w)) {
  visor_ = new QPlainTextEdit(this);   // `this` é o pai: o Qt destrói
  visor_->setReadOnly(true);
  visor_->setFont(QFont("IBM Plex Mono", 12));
  setCentralWidget(visor_);

  tela_ = std::make_unique<tela_qt>(visor_);

  QMenu* menu = menuBar()->addMenu("Sonda");
  QAction* norte = menu->addAction("Norte");
  QAction* sul = menu->addAction("Sul");
  QAction* desfazer = menu->addAction("Desfazer");

  // A conexão por ponteiro de função é a forma verificada em compilação. A
  // forma antiga, com as macros SIGNAL e SLOT, casava strings em execução - e
  // um erro de digitação virava conexão que nunca acontece, sem aviso.
  connect(norte, &QAction::triggered, this, &janela::ao_mover_norte);
  connect(sul, &QAction::triggered, this, &janela::ao_mover_sul);
  connect(desfazer, &QAction::triggered, this, &janela::ao_desfazer);

  redesenhar();
}

janela::~janela() = default;

void janela::ao_mover_norte() {
  (void)historico_.aplicar(std::make_unique<mover_sonda>(vetor2{0, -1}), mundo_);
  redesenhar();
}

void janela::ao_mover_sul() {
  (void)historico_.aplicar(std::make_unique<mover_sonda>(vetor2{0, 1}), mundo_);
  redesenhar();
}

void janela::ao_desfazer() {
  (void)historico_.desfazer_ultimo(mundo_);
  redesenhar();
}

void janela::redesenhar() { tela_->desenhar(mundo_); }

}  // namespace deriva::qt
