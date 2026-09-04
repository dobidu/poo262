// v1.0 · Aula 10 - herança simples · v1.1 · Aula 11 - virtuais e abstração
#ifndef DERIVA_ENTIDADE_HPP
#define DERIVA_ENTIDADE_HPP

#include <string>
#include <string_view>

#include "deriva/celula.hpp"
#include "deriva/vetor2.hpp"

namespace deriva {

class mundo;   // declaração adiantada: `agir` só precisa da referência

/// Qualquer coisa que ocupa uma célula e faz algo por turno.
///
/// A hierarquia é a que o domínio pede, não taxonomia inventada para o
/// exercício: uma sonda, um drone e um item são coisas diferentes que ocupam
/// posição e desenham um glifo. O que varia é o que cada uma faz no turno.
///
/// **Abstrata** (v1.1): `desenhar` é puramente virtual, então `entidade` não
/// se instancia. Isso não é cerimônia - uma entidade sem glifo não tem
/// significado no domínio, e o compilador passa a dizer isso.
///
/// **Destrutor virtual** (v1.1): sem ele, `delete` por `entidade*` não roda o
/// destrutor da derivada, e nenhum aviso aparece quando o `delete` mora dentro
/// de um `unique_ptr`. A variante `variantes/v1.1-quebrada/` mede os três
/// casos. É a caça ao bug 2.
///
/// O contador de instâncias vivas mora em CADA classe concreta, escrito à mão,
/// e não na base. Duas razões: o contador da base contaria objetos e não tipos,
/// e a repetição é o que motiva o `contador_de_instancias<T>` da Aula 19.
class entidade {
 public:
  explicit entidade(vetor2 pos) noexcept : pos_(pos) {}

  virtual ~entidade() = default;

  // Base polimórfica não se copia por valor: copiar por `entidade&` fatiaria
  // o objeto. A cópia correta é `clonar`, que a Aula 25 transforma em padrão.
  entidade(const entidade&) = delete;
  entidade& operator=(const entidade&) = delete;

  [[nodiscard]] virtual char glifo() const = 0;
  [[nodiscard]] virtual std::string_view nome() const = 0;

  /// Um turno. A base não faz nada, e a derivada que não age não precisa
  /// dizer nada - é o caso do `item`.
  virtual void agir(mundo&) {}

  [[nodiscard]] vetor2 pos() const noexcept { return pos_; }
  void mover_para(vetor2 p) noexcept { pos_ = p; }

  /// Não-virtual de propósito, e chamando o virtual: é o Template Method na
  /// sua forma mais curta. A moldura do texto é da base; o glifo é da
  /// derivada (Aula 11).
  [[nodiscard]] std::string descrever() const;

 private:
  vetor2 pos_;
};

/// A sonda que o estudante opera. Tem energia, e gasta energia agindo.
///
/// **Não é `final`, e já foi.** Na v1.0 esta classe era `final`, porque nada
/// derivava dela e a palavra documentava a intenção. A v1.7 introduziu
/// `sonda_reparadora`, e o compilador recusou: "cannot derive from final base".
/// A palavra saiu, e a lição fica: `final` é promessa, não decoração, e
/// retirá-la é admitir que a hierarquia mudou de forma. Quem depende de a
/// classe ser folha - devirtualização, por exemplo - perde a garantia nesse
/// instante (Aula 11 e Aula 17).
class sonda : public entidade {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  explicit sonda(vetor2 pos, int energia = 100) noexcept
      : entidade(pos), energia_(energia) {
    ++vivos;
    ++criados;
  }
  ~sonda() override { --vivos; }

  [[nodiscard]] char glifo() const override { return '@'; }
  [[nodiscard]] std::string_view nome() const override { return "sonda"; }
  void agir(mundo& m) override;

  [[nodiscard]] int energia() const noexcept { return energia_; }
  void gastar(int quanto) noexcept;

 private:
  int energia_;
};

/// Drone de patrulha. Anda sozinho, em linha, e inverte ao bater.
class drone final : public entidade {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  explicit drone(vetor2 pos, vetor2 rumo = {1, 0}) noexcept
      : entidade(pos), rumo_(rumo) {
    ++vivos;
    ++criados;
  }
  ~drone() override { --vivos; }

  [[nodiscard]] char glifo() const override { return 'd'; }
  [[nodiscard]] std::string_view nome() const override { return "drone"; }
  void agir(mundo& m) override;

  [[nodiscard]] vetor2 rumo() const noexcept { return rumo_; }

 private:
  vetor2 rumo_;
};

/// Item no chão. Não age - e por isso não sobrescreve `agir`.
class item final : public entidade {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  item(vetor2 pos, std::string nome, int massa) noexcept;
  ~item() override { --vivos; }

  [[nodiscard]] char glifo() const override { return '!'; }
  [[nodiscard]] std::string_view nome() const override { return nome_; }

  [[nodiscard]] int massa() const noexcept { return massa_; }

 private:
  std::string nome_;
  int massa_;
};

/// Soma dos contadores das três classes concretas. É o que a Aula 11 lê para
/// provar que o destrutor virtual fez o seu trabalho.
[[nodiscard]] int entidades_vivas() noexcept;
void zerar_entidades() noexcept;

}  // namespace deriva

#endif
