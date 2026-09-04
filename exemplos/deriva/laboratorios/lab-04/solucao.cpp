// LAB-04 · solução de referência · prepara a Aula 7
// Portão: a invariante da classe protegida, `const` cumprindo o que promete,
// e o contador `vivos` fechando em zero.
#include <cstdio>
#include <stdexcept>
#include <string>

namespace {

/// Uma leitura de sensor, com invariante: a intensidade fica entre 0 e 100.
///
/// A invariante é o que justifica a classe. Um agregado público não tem o que
/// proteger, e encapsular o que não tem invariante só acrescenta cerimônia -
/// é por isso que `vetor2` é `struct` no Deriva e esta é `class`.
class leitura {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  leitura(std::string sensor, int intensidade)
      : sensor_(std::move(sensor)), intensidade_(validar(intensidade)) {
    ++vivos;
    ++criados;
  }

  // Regra do três: o destrutor decrementa, então a cópia tem de incrementar.
  // Sem isto, `vivos` fecha NEGATIVO - e o contador passa a mentir na direção
  // que ninguém desconfia.
  leitura(const leitura& o)
      : sensor_(o.sensor_), intensidade_(o.intensidade_) {
    ++vivos;
    ++criados;
  }
  leitura& operator=(const leitura& o) {
    if (this != &o) {
      sensor_ = o.sensor_;
      intensidade_ = o.intensidade_;
    }
    return *this;   // atribuição não cria nem destrói
  }
  ~leitura() { --vivos; }

  /// `const` e `[[nodiscard]]`: não muda estado, e ignorar o retorno é erro.
  [[nodiscard]] int intensidade() const noexcept { return intensidade_; }
  [[nodiscard]] const std::string& sensor() const noexcept { return sensor_; }

  /// Muda estado, então NÃO é const - e revalida, porque a invariante vale
  /// para todo caminho que escreve no objeto, não só para o construtor.
  void ajustar(int nova) { intensidade_ = validar(nova); }

  [[nodiscard]] bool forte() const noexcept { return intensidade_ >= 70; }

 private:
  [[nodiscard]] static int validar(int v) {
    if (v < 0 || v > 100) {
      throw std::invalid_argument("intensidade fora de 0..100: " + std::to_string(v));
    }
    return v;
  }
  std::string sensor_;
  int intensidade_;
};

}  // namespace

int main() {
  int falhas = 0;
  auto checar = [&falhas](const char* o_que, bool ok) {
    std::printf("  %-44s %s\n", o_que, ok ? "OK" : "FALHA");
    if (!ok) ++falhas;
  };

  {
    const leitura a("termico", 42);
    checar("a invariante aceita valor valido", a.intensidade() == 42);
    checar("const promete e cumpre: le sem mudar", a.sensor() == "termico");

    bool recusou = false;
    try { const leitura ruim("x", 101); (void)ruim; }
    catch (const std::invalid_argument&) { recusou = true; }
    checar("o construtor recusa valor fora da faixa", recusou);

    leitura b = a;                      // cópia: nascimento
    checar("a copia incrementa o contador", leitura::vivos == 2);
    b.ajustar(80);
    checar("ajustar revalida e aceita 80", b.forte());
    checar("a copia nao alterou o original", a.intensidade() == 42);

    bool recusou_ajuste = false;
    try { b.ajustar(-1); } catch (const std::invalid_argument&) { recusou_ajuste = true; }
    checar("ajustar recusa valor invalido", recusou_ajuste);
    checar("e o objeto ficou intacto apos a recusa", b.intensidade() == 80);
  }

  checar("vivos fecha em zero", leitura::vivos == 0);
  // DUAS, e não três. O `leitura ruim("x", 101)` lançou de dentro da lista de
  // inicialização, então o corpo do construtor nunca rodou e o objeto nunca
  // existiu - logo não contou. Um objeto cujo construtor lança não é um objeto
  // pela metade: ele não é. O destrutor dele também não roda, e é por isso que
  // o contador continua correto.
  checar("criados contou DUAS construcoes, nao tres", leitura::criados == 2);

  std::printf("\nportao LAB-04: %s\n", falhas == 0 ? "OK" : "FALHA");
  return falhas == 0 ? 0 : 1;
}
