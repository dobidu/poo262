// v2.6 · Aulas 24 e 25 - SOLID e os padrões, sobre o Deriva
#ifndef DERIVA_APRESENTACAO_HPP
#define DERIVA_APRESENTACAO_HPP

#include <functional>
#include <memory>
#include <string>
#include <string_view>
#include <vector>

#include "deriva/entidade.hpp"
#include "deriva/vetor2.hpp"

namespace deriva {

class mundo;

// ===========================================================================
// DIP · a interface de apresentação
//
// O núcleo depende DESTA abstração, e não de terminal nem de Qt. É o que
// torna a separação demonstrável em vez de afirmada: a v2.7 acrescenta uma
// segunda implementação e o núcleo não muda uma linha.
//
// Antes da refatoração, o `mundo` escrevia direto em `std::cout` - e trocar a
// saída significava editar o `mundo`. A variante `v2.6-antes` preserva essa
// forma para comparação.
// ===========================================================================
class i_apresentacao {
 public:
  virtual ~i_apresentacao() = default;
  virtual void desenhar(const mundo& m) = 0;
  virtual void mensagem(std::string_view texto) = 0;
};

/// Apresentação que acumula em texto. É o que os testes usam, e é também a
/// prova de que o núcleo não sabe onde está desenhando.
class apresentacao_em_texto final : public i_apresentacao {
 public:
  void desenhar(const mundo& m) override;
  void mensagem(std::string_view texto) override;

  [[nodiscard]] const std::string& acumulado() const noexcept { return saida_; }
  void limpar() { saida_.clear(); }

 private:
  std::string saida_;
};

// ===========================================================================
// Command · a entrada
//
// Um comando é objeto, não `switch`. O que se ganha não é elegância: é o
// desfazer, que um `switch` não tem onde guardar.
// ===========================================================================
class i_comando {
 public:
  virtual ~i_comando() = default;
  [[nodiscard]] virtual bool executar(mundo& m) = 0;
  virtual void desfazer(mundo& m) = 0;
  [[nodiscard]] virtual std::string_view nome() const = 0;
};

/// Mover a sonda. Guarda de onde saiu, e é por isso que sabe voltar.
class mover_sonda final : public i_comando {
 public:
  explicit mover_sonda(vetor2 delta) noexcept : delta_(delta) {}

  [[nodiscard]] bool executar(mundo& m) override;
  void desfazer(mundo& m) override;
  [[nodiscard]] std::string_view nome() const override { return "mover"; }

 private:
  vetor2 delta_;
  vetor2 de_onde_{};
  bool executou_ = false;
};

/// A pilha de desfazer. Guarda os comandos executados, na ordem.
class historico {
 public:
  bool aplicar(std::unique_ptr<i_comando> c, mundo& m);
  [[nodiscard]] bool desfazer_ultimo(mundo& m);
  [[nodiscard]] std::size_t profundidade() const noexcept { return feitos_.size(); }
  [[nodiscard]] std::string despejar() const;

 private:
  std::vector<std::unique_ptr<i_comando>> feitos_;
};

// ===========================================================================
// Observer · o log de eventos
//
// O `mundo` avisa que algo aconteceu e não sabe quem escuta. Antes da
// refatoração ele chamava o log direto, e por isso não dava para testar sem
// arquivo.
// ===========================================================================
class i_observador {
 public:
  virtual ~i_observador() = default;
  virtual void aconteceu(std::string_view evento) = 0;
};

class registro_em_memoria final : public i_observador {
 public:
  void aconteceu(std::string_view evento) override;
  [[nodiscard]] const std::vector<std::string>& eventos() const noexcept {
    return eventos_;
  }

 private:
  std::vector<std::string> eventos_;
};

// ===========================================================================
// Factory · a criação por glifo
//
// Quem lê o mapa não precisa conhecer as classes concretas. É o que permite
// acrescentar uma entidade nova sem tocar no carregador.
// ===========================================================================
[[nodiscard]] std::unique_ptr<entidade> criar_por_glifo(char glifo, vetor2 pos);

// ===========================================================================
// Strategy · a IA, por lambda e não por herança
//
// A forma clássica seria uma hierarquia `i_estrategia` com uma classe por
// comportamento. Em C++ moderno, quando a estratégia é UMA operação e não
// guarda estado, ela é uma função - e `std::function` a guarda. Duas
// operações ou estado próprio, e volta a ser classe (Aula 25).
// ===========================================================================
using estrategia = std::function<vetor2(const entidade&, const mundo&)>;

[[nodiscard]] estrategia estrategia_de_patrulha(vetor2 rumo);
[[nodiscard]] estrategia estrategia_de_perseguicao(char glifo_alvo);
[[nodiscard]] estrategia estrategia_parada();

}  // namespace deriva

#endif
