// v2.4 · Aula 22 - a thread de entrada, e o que se compartilha
#ifndef DERIVA_FILA_DE_COMANDOS_HPP
#define DERIVA_FILA_DE_COMANDOS_HPP

#include <condition_variable>
#include <deque>
#include <mutex>
#include <optional>
#include <string>

namespace deriva {

/// A fila entre a thread que lê o teclado e a que desenha.
///
/// **O que se compartilha é esta fila, e nada mais.** É a decisão de projeto
/// da Aula 22, e ela é o oposto da tentação: seria mais fácil deixar as duas
/// threads mexerem no `mundo`, e é exatamente isso que produz a corrida que o
/// interativo mostra. Aqui o `mundo` continua sendo de uma thread só; o que
/// atravessa a fronteira são comandos, um por vez, protegidos.
///
/// `std::scoped_lock` (C++17) no lugar de `std::lock_guard`: aceita mais de um
/// mutex e resolve a ordem de travamento sozinho, o que elimina uma classe
/// inteira de impasse. Para um mutex só, os dois são equivalentes, e usar o
/// novo é hábito.
///
/// A condição de parada não é uma variável booleana lida sem proteção - esse é
/// o erro que a Aula 22 mostra medido. Ela é parte do estado guardado pelo
/// mesmo mutex, e a espera usa `condition_variable`, que acorda quem espera em
/// vez de queimar processador.
class fila_de_comandos {
 public:
  /// Põe um comando na fila e acorda quem estiver esperando.
  void empurrar(std::string comando);

  /// Bloqueia até haver comando ou a fila ser fechada. `std::nullopt` quando
  /// fechada e vazia - é o sinal de fim, e não uma exceção.
  [[nodiscard]] std::optional<std::string> puxar();

  /// Tira sem bloquear. Serve ao laço de render, que não pode parar.
  [[nodiscard]] std::optional<std::string> tentar_puxar();

  /// Fecha para sempre e acorda todos. Idempotente.
  void fechar();

  [[nodiscard]] bool fechada() const;
  [[nodiscard]] std::size_t tamanho() const;

 private:
  mutable std::mutex mutex_;
  std::condition_variable tem_coisa_;
  std::deque<std::string> fila_;
  bool fechada_ = false;
};

/// Roda `quantos` comandos por uma fila, de uma thread produtora e uma
/// consumidora, e devolve a ordem em que foram consumidos.
///
/// Determinístico apesar de haver duas threads, e é isso que a Aula 22 quer
/// mostrar: concorrência não implica indeterminismo. A ordem é preservada
/// porque a fila é FIFO e há um consumidor só. Com dois consumidores, a ordem
/// deixaria de ser garantida - e aí o replay não serviria mais.
[[nodiscard]] std::string exercitar_fila(int quantos);

}  // namespace deriva

#endif
