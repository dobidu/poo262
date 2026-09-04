// Aula 17 - o diamante com estado, medido
#ifndef DERIVA_DIAMANTE_HPP
#define DERIVA_DIAMANTE_HPP

#include <cstddef>

namespace deriva::medida {

/// Este cabeçalho não entra no jogo. Como `leiaute.hpp`, ele existe para que
/// os números do Cap. 17 sejam os que o g++ produz.
///
/// O diamante de verdade só aparece quando a base do meio tem ESTADO. Aqui
/// está ele nas três formas, para serem medidas lado a lado.

/// A base com estado. Um `int` e uma função virtual.
struct nucleo {
  virtual ~nucleo() = default;
  int leituras = 0;
};

/// Herança comum nos dois ramos: o `nucleo` é DUPLICADO na folha.
struct movel : nucleo { int passos = 0; };
struct sensor : nucleo { int alcance = 0; };
struct patrulha_duplicada : movel, sensor { int rota = 0; };

/// Herança virtual: existe UM `nucleo` na folha, e o compilador paga por isso
/// com um ponteiro extra por ramo virtual.
struct movel_v : virtual nucleo { int passos = 0; };
struct sensor_v : virtual nucleo { int alcance = 0; };
struct patrulha_unica : movel_v, sensor_v { int rota = 0; };

/// A saída que o material recomenda: composição no lugar do segundo ramo.
/// Nenhum diamante, nenhuma ambiguidade, nenhuma pergunta sobre qual
/// `leituras` é o certo. É também a MAIOR das três em bytes (56), e continua
/// sendo a recomendada: o que se está comprando é a ausência de uma pergunta
/// que não tem resposta boa.
struct patrulha_composta : movel { sensor_v olho; int rota = 0; };

// Os números medidos em g++ 13.3 x86-64, e eles contrariam a intuição:
//
//   nucleo                16    vptr 8 + int 4 + padding 4
//   movel / sensor        16    a base cabe no mesmo alinhamento
//   patrulha_duplicada    40    DUAS bases de 16, mais rota e padding
//   patrulha_unica        48    UMA base, e mais um ponteiro por ramo virtual
//   patrulha_composta     56    nenhum diamante, e o maior de todos
//
// A herança virtual é a MAIOR das três, não a menor. O ponteiro para a base
// virtual que cada ramo carrega custa mais do que duplicar uma base de 16
// bytes. Escrever aqui que ela "economiza memória" seria mentir, e a primeira
// versão deste cabeçalho tinha um `static_assert` invertido afirmando
// exatamente isso - o compilador o recusou.
//
// O que a herança virtual compra não é tamanho: é **correção**. Na forma
// duplicada existem dois campos `leituras` com endereços diferentes, e nenhum
// dos dois é "o" valor; escrever por um ramo e ler pelo outro devolve lixo
// coerente. Na forma virtual existe um campo só. É por isso que se paga.
static_assert(sizeof(nucleo) == 16, "vptr 8 + int 4 + padding 4");
static_assert(sizeof(patrulha_duplicada) == 40, "duas bases de 16, mais rota");
static_assert(sizeof(patrulha_unica) == 48, "uma base, mais um ponteiro por ramo");
static_assert(sizeof(patrulha_unica) > sizeof(patrulha_duplicada),
              "a indireção virtual custa MAIS bytes que a duplicação que evita");

/// Quantos subobjetos `nucleo` existem em cada forma. Não dá para afirmar em
/// `static_assert`, porque a resposta é sobre identidade de endereço e não
/// sobre tamanho; `testes/test_diamante.cpp` a mede.
[[nodiscard]] inline std::size_t nucleos_em_duplicada() {
  patrulha_duplicada p;
  const nucleo* por_movel = static_cast<movel*>(&p);
  const nucleo* por_sensor = static_cast<sensor*>(&p);
  return por_movel == por_sensor ? 1u : 2u;
}

[[nodiscard]] inline std::size_t nucleos_em_unica() {
  patrulha_unica p;
  const nucleo* por_movel = static_cast<movel_v*>(&p);
  const nucleo* por_sensor = static_cast<sensor_v*>(&p);
  return por_movel == por_sensor ? 1u : 2u;
}

}  // namespace deriva::medida

#endif
