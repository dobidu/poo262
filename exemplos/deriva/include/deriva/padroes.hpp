// v2.6 · Aula 25 - os padrões que faltavam: State, Decorator, Singleton
#ifndef DERIVA_PADROES_HPP
#define DERIVA_PADROES_HPP

#include <functional>
#include <memory>
#include <string>
#include <string_view>
#include <vector>

#include "deriva/apresentacao.hpp"
#include "deriva/inventario.hpp"

namespace deriva {

// ===========================================================================
// State · as telas do console
//
// A alternativa é um `enum` mais um `switch` em cada função que reage a
// comando. Com quatro telas e cinco comandos são vinte casos espalhados, e
// acrescentar uma tela obriga a visitar todos.
//
// Como objeto, cada tela responde por si, e a transição é o valor de retorno -
// o que a torna testável sem console.
// ===========================================================================
class i_tela {
 public:
  virtual ~i_tela() = default;
  [[nodiscard]] virtual std::string_view nome() const = 0;

  /// Trata o comando e devolve a tela seguinte, ou `nullptr` para ficar.
  /// Devolver a próxima em vez de mutar um campo é o que impede duas telas de
  /// discordarem sobre qual está ativa.
  [[nodiscard]] virtual std::unique_ptr<i_tela> comando(std::string_view c) = 0;
};

class tela_mapa final : public i_tela {
 public:
  [[nodiscard]] std::string_view nome() const override { return "mapa"; }
  [[nodiscard]] std::unique_ptr<i_tela> comando(std::string_view c) override;
};

class tela_inventario final : public i_tela {
 public:
  [[nodiscard]] std::string_view nome() const override { return "inventario"; }
  [[nodiscard]] std::unique_ptr<i_tela> comando(std::string_view c) override;
};

class tela_inspecao final : public i_tela {
 public:
  [[nodiscard]] std::string_view nome() const override { return "inspecao"; }
  [[nodiscard]] std::unique_ptr<i_tela> comando(std::string_view c) override;
};

/// A máquina, que só guarda a tela corrente e delega.
class console {
 public:
  console();
  void comando(std::string_view c);
  [[nodiscard]] std::string_view tela() const { return atual_->nome(); }
  [[nodiscard]] const std::vector<std::string>& historico() const noexcept {
    return historico_;
  }

 private:
  std::unique_ptr<i_tela> atual_;
  std::vector<std::string> historico_;
};

// ===========================================================================
// Decorator · a apresentação, empacotada
//
// Um decorador implementa a MESMA interface que decora, e guarda um ponteiro
// para ela. Empilhar dois é empilhar comportamento sem herdar de nenhum dos
// dois - que é o que herança não daria: com herança, "numerado e com moldura"
// exigiria uma classe para cada combinação.
// ===========================================================================
class com_numero_de_linha final : public i_apresentacao {
 public:
  explicit com_numero_de_linha(std::unique_ptr<i_apresentacao> dentro)
      : dentro_(std::move(dentro)) {}

  void desenhar(const mundo& m) override;
  void mensagem(std::string_view texto) override;

 private:
  std::unique_ptr<i_apresentacao> dentro_;
  int linha_ = 0;
};

class com_moldura final : public i_apresentacao {
 public:
  com_moldura(std::unique_ptr<i_apresentacao> dentro, std::string titulo)
      : dentro_(std::move(dentro)), titulo_(std::move(titulo)) {}

  void desenhar(const mundo& m) override;
  void mensagem(std::string_view texto) override;

 private:
  std::unique_ptr<i_apresentacao> dentro_;
  std::string titulo_;
};

// ===========================================================================
// Singleton · escrito para ser criticado
//
// O material recomenda NÃO usá-lo, e escrevê-lo é a forma de mostrar por quê.
// Este é o Singleton de Meyers, que é a versão correta da forma errada: a
// inicialização de estático local é garantidamente única e segura entre
// threads desde C++11.
//
// Os quatro custos, e nenhum deles é opinião:
//   1. o teste não consegue substituí-lo, porque quem o usa o pede por nome;
//   2. dois testes na mesma execução compartilham o estado dele;
//   3. a ordem de destruição entre estáticos não é controlável;
//   4. ele esconde uma dependência que a assinatura deveria declarar.
//
// O contador `vivos` da Aula 07 é estado global mutável, e este material o usa
// assim - como INSTRUMENTO, e não como projeto. A diferença vale ser dita: o
// contador não participa da lógica do jogo, e nenhuma decisão do domínio
// depende dele.
// ===========================================================================
class registro_global {
 public:
  static registro_global& instancia();

  void anotar(std::string_view evento);
  [[nodiscard]] std::size_t quantos() const noexcept { return eventos_.size(); }
  void limpar() { eventos_.clear(); }

  registro_global(const registro_global&) = delete;
  registro_global& operator=(const registro_global&) = delete;

 private:
  registro_global() = default;
  std::vector<std::string> eventos_;
};

/// A alternativa, e é ela que o material recomenda: a dependência declarada no
/// parâmetro. Duas linhas mais longa na chamada, e testável.
void anotar_em(i_observador& onde, std::string_view evento);

}  // namespace deriva

#endif
