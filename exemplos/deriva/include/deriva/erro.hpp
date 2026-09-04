// v2.2 · Aula 20 - exceções, garantias, optional e variant
#ifndef DERIVA_ERRO_HPP
#define DERIVA_ERRO_HPP

#include <filesystem>
#include <stdexcept>
#include <string>
#include <variant>

#include "deriva/mapa.hpp"

namespace deriva {

/// A raiz da hierarquia de erros do Deriva.
///
/// Deriva de `std::runtime_error` e não de `std::exception` direto, porque
/// `runtime_error` já guarda a mensagem e resolve o `what()`. Herdar de
/// `std::exception` e reimplementar `what()` é trabalho sem retorno, e a
/// tentação de guardar um `std::string` membro esconde uma armadilha: se o
/// construtor de cópia da exceção lançar durante o desenrolar da pilha, o
/// programa termina.
class erro_de_deriva : public std::runtime_error {
 public:
  explicit erro_de_deriva(const std::string& msg) : std::runtime_error(msg) {}
};

/// O arquivo existe e não é um mapa. Erro de conteúdo, não de ausência.
class mapa_invalido : public erro_de_deriva {
 public:
  mapa_invalido(std::filesystem::path caminho, std::string motivo);

  [[nodiscard]] const std::filesystem::path& caminho() const noexcept {
    return caminho_;
  }
  [[nodiscard]] const std::string& motivo() const noexcept { return motivo_; }

 private:
  std::filesystem::path caminho_;
  std::string motivo_;
};

/// Não deu para ler o arquivo. Permissão, disco, dispositivo.
class falha_de_leitura : public erro_de_deriva {
 public:
  falha_de_leitura(std::filesystem::path caminho, std::error_code ec);

  [[nodiscard]] const std::filesystem::path& caminho() const noexcept {
    return caminho_;
  }
  [[nodiscard]] std::error_code codigo() const noexcept { return ec_; }

 private:
  std::filesystem::path caminho_;
  std::error_code ec_;
};

/// O motivo pelo qual um texto não é mapa. Enumerado, e não string: quem trata
/// o erro decide o que fazer com base nisto, e comparar string é frágil.
enum class razao {
  vazio,
  fileira_torta,
  sem_entrada,
  entrada_duplicada,
  glifo_desconhecido,
};

[[nodiscard]] std::string_view descrever(razao r) noexcept;

/// O resultado de tentar interpretar um texto como mapa.
///
/// **A escolha de projeto da Aula 20**, e ela é declarada no tipo: três formas
/// de dizer que algo não deu certo, cada uma para um caso diferente.
///
/// - `std::optional` para **ausência**: o arquivo não existe. Não é erro, é
///   resposta. É o que `mapa::carregar` devolve desde a v0.3.
/// - `std::variant` para **erro esperado com informação**: o texto existe e
///   não é mapa, e quem chamou precisa saber por quê para decidir. Não é
///   exceção porque acontece no fluxo normal - o estudante vai errar o mapa
///   dele muitas vezes.
/// - **exceção** para o que rompe a operação: não deu para LER o arquivo.
///   Quem chamou não tem o que decidir, e o desenrolar da pilha é a resposta
///   certa.
using resultado_de_mapa = std::variant<mapa, razao>;

/// Interpreta o texto, e diz por que falhou quando falha.
[[nodiscard]] resultado_de_mapa interpretar(std::string_view texto, std::string nome);

/// Lê e interpreta. Lança `falha_de_leitura` quando o sistema de arquivos
/// recusa, e `mapa_invalido` quando o conteúdo não serve.
///
/// **Garantia forte**: ou devolve um mapa válido, ou lança sem ter deixado
/// nada pela metade. Isso é grátis aqui porque a função não tem estado a
/// desfazer - e é justamente essa a razão para a leitura ser separada da
/// aplicação (Aula 20).
[[nodiscard]] mapa carregar_ou_lancar(const std::filesystem::path& caminho);

}  // namespace deriva

#endif
