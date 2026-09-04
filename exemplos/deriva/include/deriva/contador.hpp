// v0.1 · Aula 07 - o contador de instâncias vivas
#ifndef DERIVA_CONTADOR_HPP
#define DERIVA_CONTADOR_HPP

namespace deriva {

/// O detector de vazamento da disciplina, e ele não depende de sanitizer.
///
/// `vivos` é `inline static` - variável inline é C++17, e é o que dispensa a
/// definição num .cpp. Incrementa no construtor, decrementa no destrutor: se
/// não fecha em zero no fim de `main`, um destrutor não rodou.
///
/// Nesta versão o contador é escrito À MÃO em cada classe que o quer. Essa
/// repetição é deliberada: é ela que motiva o `contador_de_instancias<T>` por
/// CRTP na Aula 19. Template que chega antes de o estudante sentir a
/// repetição é solução para um problema que ele não teve.
///
/// Não é seguro entre threads. A Aula 22 mostra exatamente esta variável
/// perdendo um incremento - e é o interativo de corrida de dados.
struct contador_mapa {
  inline static int vivos = 0;
  inline static int criados = 0;
};

struct contador_terminal {
  inline static int vivos = 0;
  inline static int criados = 0;
};

/// Zera tudo. Só para os testes: cada TEST_CASE começa do mesmo estado.
void zerar_contadores() noexcept;

/// Soma dos `vivos`. É o que `--contadores` imprime.
[[nodiscard]] int total_vivos() noexcept;

}  // namespace deriva

#endif
