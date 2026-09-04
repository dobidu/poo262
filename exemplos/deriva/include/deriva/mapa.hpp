// v0.3 · Aula 09 - composição, std::optional, std::filesystem, string_view
#ifndef DERIVA_MAPA_HPP
#define DERIVA_MAPA_HPP

#include <filesystem>
#include <ostream>
#include <optional>
#include <string>
#include <string_view>

#include "deriva/contador.hpp"
#include "deriva/grade.hpp"
#include "deriva/instrumento.hpp"
#include "deriva/vetor2.hpp"

namespace deriva {

class mapa;
/// Escrever o despejo num fluxo. Função livre e não membro: `operator<<` tem
/// o fluxo do lado esquerdo, e o lado esquerdo não é nosso.
std::ostream& operator<<(std::ostream& os, const mapa& m);

/// Um setor da estação: a grade, o nome, e onde a sonda entra.
///
/// `mapa` **compõe** uma `grade` - não herda dela. A pergunta que decide é a
/// da Aula 09: um mapa *é* uma grade, ou um mapa *tem* uma grade? Ele tem
/// nome e ponto de entrada, que grade nenhuma tem; e não faz sentido passar
/// um mapa onde se espera uma grade.
///
/// Carregar de arquivo devolve `std::optional`: arquivo ausente ou linha
/// malformada é *ausência de resultado*, não exceção. Erro de verdade -
/// permissão negada, disco cheio - só chega na v2.2 (Aula 20), e aí sim como
/// exceção.
class mapa {
 public:
  mapa(std::string nome, int largura, int altura);

  // A regra dos cinco, completa (v1.4 · Aula 14).
  //
  // MEDIDO, e o resultado contraria o que este comentário dizia antes. Com o
  // construtor de movimento, `de_texto` custa **duas** construções; sem ele,
  // custa **duas** também. O movimento não mudou número nenhum que o contador
  // relate, porque o contador conta OBJETOS - e dois objetos nascem nos dois
  // casos: o local e o que vai para dentro do `std::optional`.
  //
  // O que o movimento mudou é o CUSTO da segunda construção: com ele, o
  // ponteiro de heap da grade troca de dono; sem ele, as células são copiadas
  // uma a uma. `testes/test_mapa.cpp` mede a diferença por identidade de
  // endereço, que é o único jeito de vê-la - e é essa a lição da Aula 14: o
  // instrumento da Aula 07 não distingue cópia de movimento, e saber o que ele
  // não vê vale tanto quanto saber usá-lo.
  //
  // `noexcept` não é decoração: `std::vector<mapa>` só usa o movimento ao
  // realocar se ele for `noexcept`.
  ~mapa();
  mapa(const mapa& o);
  mapa& operator=(const mapa& o);
  mapa(mapa&& o) noexcept;
  mapa& operator=(mapa&& o) noexcept;

  [[nodiscard]] const grade& g() const noexcept { return grade_; }
  [[nodiscard]] grade& g() noexcept { return grade_; }
  [[nodiscard]] std::string_view nome() const noexcept { return nome_; }
  [[nodiscard]] vetor2 entrada() const noexcept { return entrada_; }

  /// Lê um mapa em texto. Uma linha por fileira; `#` parede, `.` piso,
  /// `@` entrada da sonda, `!` item.
  ///
  /// `std::nullopt` quando o arquivo não existe, está vazio, ou tem linha de
  /// largura diferente das outras.
  [[nodiscard]] static std::optional<mapa> carregar(
      const std::filesystem::path& caminho);

  /// A mesma coisa, a partir do conteúdo já em memória. É esta que os testes
  /// usam: teste que depende do sistema de arquivos é teste frágil.
  [[nodiscard]] static std::optional<mapa> de_texto(std::string_view texto,
                                                    std::string nome);

  /// Render determinístico. Mesma entrada, mesma saída, byte a byte - é o que
  /// torna o replay da Aula 16 possível.
  /// v1.5 · Aula 15. O par const / não-const existe porque `mapa` const tem
  /// de deixar LER a célula e não deixar escrever nela. Uma sobrecarga só,
  /// devolvendo referência não-const, permitiria escrever através de um mapa
  /// constante; devolvendo referência const, impediria escrever em qualquer um.
  [[nodiscard]] const celula& operator[](vetor2 p) const { return grade_.em(p); }
  [[nodiscard]] celula& operator[](vetor2 p) { return grade_.em(p); }

  [[nodiscard]] std::string despejar() const;

 private:
  std::string nome_;
  grade grade_;
  vetor2 entrada_{};
  marca_de_vida marca_;
};

}  // namespace deriva

#endif
