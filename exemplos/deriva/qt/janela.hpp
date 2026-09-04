// v2.7 · Aula 26 - Qt como SEGUNDO front-end sobre o mesmo núcleo
#ifndef DERIVA_QT_JANELA_HPP
#define DERIVA_QT_JANELA_HPP

// Este arquivo NÃO entra no build padrão. Compila com
//     cmake -S . -B build -DDERIVA_COM_QT=ON
// e requer Qt6 instalado. O plano v2 rebaixa a Aula 26 a demonstração do
// docente com esqueleto publicado, sem entrega obrigatória - e é este o
// esqueleto.
//
// O argumento da aula não é Qt. É que o núcleo do Deriva NÃO MUDA uma linha
// para ganhar uma segunda interface, e isso só é verdade porque a v2.6 extraiu
// `i_apresentacao`. Antes dela, o `mundo` escrevia em `std::cout` e esta
// janela seria impossível sem editá-lo - é o que a variante `v2.6-antes`
// preserva para comparação.

#include <QMainWindow>
#include <QPlainTextEdit>

#include <memory>

#include "deriva/apresentacao.hpp"
#include "deriva/mundo.hpp"

namespace deriva::qt {

/// A implementação Qt de `i_apresentacao`.
///
/// Repare no que ela NÃO faz: não conhece regra de jogo, não decide o que
/// acontece num turno, não sabe o que é uma parede. Ela recebe um `mundo` e
/// desenha. É a mesma interface que `apresentacao_em_texto` implementa, e o
/// núcleo não sabe qual das duas está do outro lado.
class tela_qt final : public i_apresentacao {
 public:
  explicit tela_qt(QPlainTextEdit* alvo) : alvo_(alvo) {}

  void desenhar(const mundo& m) override;
  void mensagem(std::string_view texto) override;

 private:
  QPlainTextEdit* alvo_;   // observação, não posse: a árvore do Qt é a dona
};

/// A janela.
///
/// **Posse no Qt é diferente.** `QObject` tem árvore de pais, e o pai destrói
/// os filhos. Passar um `QWidget*` cru para o construtor do filho ENTREGA a
/// posse ao pai - e por isso `unique_ptr` sobre `QWidget` com pai é erro de
/// dupla liberação. É a exceção à regra da Aula 12, e ela é declarada e não
/// escondida.
///
/// O `Q_OBJECT` exige o MOC, um pré-processador que gera código a partir do
/// cabeçalho. É por isso que `CMAKE_AUTOMOC` existe, e é o que faz esta classe
/// precisar de um sistema de build que o Qt entenda.
class janela : public QMainWindow {
  Q_OBJECT

 public:
  explicit janela(mundo w, QWidget* pai = nullptr);
  ~janela() override;

 private slots:
  /// Um slot é um método comum que o MOC registra para poder ser chamado por
  /// nome, sem que quem chama conheça o tipo. É a versão do Qt para Observer,
  /// e o compilador não verifica a assinatura - o erro aparece em execução, na
  /// forma de uma conexão que não acontece.
  void ao_mover_norte();
  void ao_mover_sul();
  void ao_desfazer();

 private:
  void redesenhar();

  mundo mundo_;                          // o núcleo, intacto
  historico historico_;                  // Command, da v2.6
  std::unique_ptr<tela_qt> tela_;
  QPlainTextEdit* visor_ = nullptr;      // filho: o Qt é o dono
};

}  // namespace deriva::qt

#endif
