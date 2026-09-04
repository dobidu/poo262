// v2.0 · Aula 19 - CRTP: o detector de vazamento vira exercício de template
#ifndef DERIVA_CONTADOR_CRTP_HPP
#define DERIVA_CONTADOR_CRTP_HPP

namespace deriva {

/// O contador de instâncias vivas, generalizado.
///
/// Desde a Aula 7 este contador foi escrito **à mão** em cada classe: um
/// `inline static int vivos`, um `++` no construtor, um `--` no destrutor.
/// Três classes concretas de entidade, mais `mapa`, mais `terminal_bruto`,
/// mais `no_estacao`. A repetição foi deliberada, e é ela o argumento deste
/// template: quem sentiu o tédio de escrever a sexta cópia entende por que
/// generalizar, e quem não sentiu acha que é enfeite.
///
/// O truque é o parâmetro `T`: cada instanciação de
/// `contador_de_instancias<X>` é um TIPO diferente, logo tem os seus próprios
/// `vivos` e `criados`. Herança comum não faria isso - uma base não-template
/// compartilharia um contador só entre todas as derivadas, que é exatamente o
/// erro que o contador da base cometeria (Aula 11).
///
/// Nada aqui é virtual, e é isso que o torna polimorfismo **estático**: o
/// custo é zero em tempo de execução, e o objeto não cresce um byte, porque
/// não há vtable.
///
/// As classes das Aulas 7 a 18 continuam com o contador manual, de propósito:
/// o material precisa das duas formas lado a lado para que a comparação seja
/// possível. `testes/test_contador_crtp.hpp` prova que se comportam igual.
template <class T>
class contador_de_instancias {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  static void zerar() noexcept { vivos = criados = 0; }

  /// Verdadeiro quando todo objeto deste tipo já foi destruído. É o que o
  /// portão `make verifica` consulta.
  [[nodiscard]] static bool fechou() noexcept { return vivos == 0; }

 protected:
  // Protegido e não-virtual: esta base não é para ser usada por ponteiro, e
  // por isso não paga destrutor virtual. Quem herdar dela e for base
  // polimórfica declara o SEU destrutor virtual, como `entidade` faz.
  contador_de_instancias() noexcept {
    ++vivos;
    ++criados;
  }
  contador_de_instancias(const contador_de_instancias&) noexcept {
    ++vivos;
    ++criados;   // cópia também é nascimento, e o manual esquecia disso
  }
  contador_de_instancias(contador_de_instancias&&) noexcept {
    ++vivos;
    ++criados;
  }
  contador_de_instancias& operator=(const contador_de_instancias&) noexcept {
    return *this;   // atribuição não cria nem destrói
  }
  contador_de_instancias& operator=(contador_de_instancias&&) noexcept {
    return *this;
  }
  ~contador_de_instancias() noexcept { --vivos; }
};

static_assert(sizeof(contador_de_instancias<int>) == 1,
              "base vazia: nao ha estado por objeto, so por TIPO");

}  // namespace deriva

#endif
