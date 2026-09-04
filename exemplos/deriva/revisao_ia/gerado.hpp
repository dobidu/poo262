// Aula 04 - código OO gerado por IA, plausível e defeituoso
#ifndef DERIVA_REVISAO_IA_HPP
#define DERIVA_REVISAO_IA_HPP

#include <memory>
#include <string>
#include <vector>

namespace deriva::revisao {

// ===========================================================================
// O QUE UM MODELO PRODUZ para "uma classe que guarda as leituras de um sensor
// da estação, com hierarquia e inventário".
//
// Compila sem um aviso. Passa no teste que o próprio modelo escreveu. Tem
// **três defeitos plantados**, e cada um deles é um item da rubrica da Aula 4.
// Nenhum é erro de digitação: os três são decisões plausíveis, e é isso que
// os torna caros.
//
// Os três estão marcados com `DEFEITO n` para o material. O arquivo que o
// estudante recebe é `gerado_sem_marcas.hpp`, escrito por
// `build/gerar_sem_marcas.py`: dele saem as marcas, esta tarja, e também o
// `namespace revisado` do fim deste arquivo - que é a versão corrigida dos
// três defeitos, e que entregava a resposta de cada um quarenta linhas
// abaixo dele. A tarefa é encontrá-los, e por isso a cópia do estudante não
// pode trazer nem a contagem nem a correção.
// ===========================================================================

/// A base da hierarquia gerada.
struct sensor_base {
  explicit sensor_base(std::string nome) : nome_(std::move(nome)) {}

  // DEFEITO 2 · item R5 da rubrica (Hierarquia): destrutor NÃO virtual numa base com
  // método virtual. Deletar por `sensor_base*` não roda o destrutor da
  // derivada. Com o `delete` dentro de um `unique_ptr`, o compilador não
  // emite aviso algum.
  ~sensor_base() = default;   // R5

  virtual double media() const = 0;

  // DEFEITO 3 · item R3 da rubrica (const-correctness): devolve cópia da string a cada chamada,
  // e não é `const` nem `[[nodiscard]]`. Chamar num objeto `const` não
  // compila, e o custo passa despercebido em laço.
  std::string nome() { return nome_; }   // R3

 protected:
  std::string nome_;
};

/// Sensor térmico. Guarda as leituras num vetor.
struct sensor_termico : sensor_base {
  explicit sensor_termico(std::string nome) : sensor_base(std::move(nome)) {}

  void registrar(double v) { leituras_.push_back(v); }
  double media() const override;

  // DEFEITO 1 · item R1 da rubrica (Posse): o vetor é público, e com ele a invariante
  // "as leituras nunca são negativas" - que `registrar` protege - passa a ser
  // contornável de fora. A classe promete algo que não consegue garantir.
  std::vector<double> leituras_;   // R1
};

/// O painel, que possui os sensores.
class painel {
 public:
  void acrescentar(std::unique_ptr<sensor_base> s);
  [[nodiscard]] std::size_t quantos() const noexcept { return sensores_.size(); }
  [[nodiscard]] double media_geral() const;

 private:
  std::vector<std::unique_ptr<sensor_base>> sensores_;
};

/// Os três defeitos, e o item da rubrica que pega cada um. Serve ao portão do
/// laboratório e à correção.
struct achado {
  int numero;
  const char* item_da_rubrica;
  const char* o_que_e;
};
[[nodiscard]] std::vector<achado> defeitos_plantados();

// ===========================================================================
// A versão revisada. Os mesmos requisitos, os três defeitos corrigidos.
// ===========================================================================
namespace revisado {

class sensor_base {
 public:
  explicit sensor_base(std::string nome) : nome_(std::move(nome)) {}
  virtual ~sensor_base() = default;                        // R5 ✓

  sensor_base(const sensor_base&) = delete;
  sensor_base& operator=(const sensor_base&) = delete;

  [[nodiscard]] virtual double media() const = 0;
  [[nodiscard]] std::string_view nome() const noexcept {   // R3 ✓
    return nome_;
  }

 protected:
  std::string nome_;
};

class sensor_termico final : public sensor_base {
 public:
  inline static int vivos = 0;

  explicit sensor_termico(std::string nome);
  ~sensor_termico() override;

  /// Devolve se aceitou: a invariante é da classe, e o vetor é privado.  R1 ✓
  [[nodiscard]] bool registrar(double v);
  [[nodiscard]] double media() const override;
  [[nodiscard]] std::size_t quantas() const noexcept { return leituras_.size(); }

 private:
  std::vector<double> leituras_;   // R1
};

}  // namespace revisado
}  // namespace deriva::revisao

#endif
