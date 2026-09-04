#include "deriva/erro.hpp"

#include <fstream>
#include <sstream>
#include <utility>

namespace deriva {

mapa_invalido::mapa_invalido(std::filesystem::path caminho, std::string motivo)
    : erro_de_deriva("mapa invalido em '" + caminho.string() + "': " + motivo),
      caminho_(std::move(caminho)),
      motivo_(std::move(motivo)) {}

falha_de_leitura::falha_de_leitura(std::filesystem::path caminho, std::error_code ec)
    : erro_de_deriva("nao foi possivel ler '" + caminho.string() + "': " + ec.message()),
      caminho_(std::move(caminho)),
      ec_(ec) {}

std::string_view descrever(razao r) noexcept {
  switch (r) {
    case razao::vazio: return "o texto esta vazio";
    case razao::fileira_torta: return "as fileiras tem larguras diferentes";
    case razao::sem_entrada: return "nao ha entrada marcada com @";
    case razao::entrada_duplicada: return "ha mais de uma entrada marcada com @";
    case razao::glifo_desconhecido: return "ha glifo que o mapa nao define";
  }
  return "razao desconhecida";
}

resultado_de_mapa interpretar(std::string_view texto, std::string nome) {
  // Repare que a validação acontece ANTES de qualquer construção: nada é
  // alocado até se saber que o texto serve. É o que torna a garantia forte
  // barata - não há o que desfazer.
  if (texto.empty()) return razao::vazio;

  std::size_t largura = 0, entradas = 0, fileiras = 0, inicio = 0;
  while (inicio <= texto.size()) {
    const std::size_t fim = texto.find('\n', inicio);
    const std::string_view linha = texto.substr(
        inicio, fim == std::string_view::npos ? std::string_view::npos : fim - inicio);
    if (!linha.empty()) {
      if (fileiras == 0) largura = linha.size();
      else if (linha.size() != largura) return razao::fileira_torta;
      ++fileiras;
      for (const char c : linha) {
        if (c == '@') ++entradas;
        else if (c != '#' && c != '.' && c != '!') return razao::glifo_desconhecido;
      }
    }
    if (fim == std::string_view::npos) break;
    inicio = fim + 1;
  }

  if (fileiras == 0) return razao::vazio;
  if (entradas == 0) return razao::sem_entrada;
  if (entradas > 1) return razao::entrada_duplicada;

  std::optional<mapa> m = mapa::de_texto(texto, std::move(nome));
  if (!m) return razao::fileira_torta;   // a validação acima já cobriu; cinto
  return std::move(*m);
}

mapa carregar_ou_lancar(const std::filesystem::path& caminho) {
  std::error_code ec;
  if (!std::filesystem::exists(caminho, ec)) {
    // Ausência tratada como erro AQUI, e como `optional` em `mapa::carregar`.
    // A diferença não é capricho: esta função promete devolver um mapa, e
    // aquela promete responder se há um.
    throw falha_de_leitura(caminho, std::make_error_code(std::errc::no_such_file_or_directory));
  }
  if (ec) throw falha_de_leitura(caminho, ec);

  std::ifstream arq(caminho);
  if (!arq) {
    throw falha_de_leitura(caminho, std::make_error_code(std::errc::permission_denied));
  }
  std::ostringstream buf;
  buf << arq.rdbuf();
  const std::string texto = buf.str();

  resultado_de_mapa r = interpretar(texto, caminho.stem().string());
  if (const razao* pr = std::get_if<razao>(&r)) {
    throw mapa_invalido(caminho, std::string(descrever(*pr)));
  }
  return std::move(std::get<mapa>(r));
}

}  // namespace deriva
