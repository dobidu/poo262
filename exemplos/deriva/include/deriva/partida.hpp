// v2.5 · Aula 23 - serialização, versionamento e compatibilidade regressiva
#ifndef DERIVA_PARTIDA_HPP
#define DERIVA_PARTIDA_HPP

#include <optional>
#include <string>
#include <string_view>
#include <vector>

#include "deriva/vetor2.hpp"

namespace deriva {

class mundo;

/// O estado salvo de uma partida.
///
/// O formato é texto de linhas `chave valor`, e a escolha tem motivo: o
/// despejo do replay já é texto, o `diff` do portão já compara texto, e um
/// formato binário obrigaria a escrever uma ferramenta de inspeção só para
/// depurar o salvamento. JSON entraria se houvesse estrutura aninhada de
/// verdade; aqui não há.
///
/// **Versionamento é a primeira linha do arquivo**, e não a última nem um
/// campo no meio: quem lê precisa saber com que regras ler antes de ler
/// qualquer outra coisa.
struct partida {
  /// Sobe quando o formato muda de forma que um leitor antigo erraria.
  /// Acrescentar campo OPCIONAL no fim não muda a versão; mudar o significado
  /// de um campo existente muda.
  static constexpr int kVersaoAtual = 2;

  int versao = kVersaoAtual;
  std::string setor;
  vetor2 sonda{};
  int carga = 0;
  int turno = 0;
  /// Campo que a versão 2 acrescentou. Um arquivo v1 não o tem, e o leitor
  /// tem de aceitar isso - é o que compatibilidade regressiva significa.
  int energia = 100;

  [[nodiscard]] std::string serializar() const;

  /// Lê o que houver. `std::nullopt` quando o texto não é uma partida;
  /// exceção nenhuma, porque arquivo de save corrompido é caso esperado.
  [[nodiscard]] static std::optional<partida> desserializar(std::string_view texto);

  /// Extrai o estado de um mundo em execução.
  [[nodiscard]] static partida de(const mundo& m, int turno);
};

/// Quantas versões de formato este leitor entende. Serve ao teste que prova a
/// compatibilidade regressiva.
[[nodiscard]] std::vector<int> versoes_aceitas();

}  // namespace deriva

#endif
