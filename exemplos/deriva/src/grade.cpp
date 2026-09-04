#include "deriva/grade.hpp"

#include <stdexcept>
#include <string>

namespace deriva {
namespace {

/// Valida NA lista de inicialização, não no corpo.
///
/// A primeira versão deste construtor validava no corpo, e um teste pegou o
/// erro: com `grade(5, -1)`, o `-1` virava `size_t` enorme e o `std::vector`
/// lançava `length_error` **antes** de o corpo rodar. A mensagem que o
/// estudante veria era "cannot create std::vector larger than max_size()", que
/// não diz nada sobre a grade.
///
/// A lista de inicialização roda inteira antes da primeira linha do corpo:
/// validação de argumento que protege a construção de um membro tem de estar
/// na lista, e a ordem é a de DECLARAÇÃO dos membros - `largura_` e `altura_`
/// vêm antes de `celulas_`, então a checagem acontece a tempo (Aula 08).
[[nodiscard]] int exigir_positivo(int valor, const char* qual) {
  if (valor <= 0) {
    throw std::invalid_argument(std::string("grade: ") + qual +
                                " precisa ser positiva, recebeu " +
                                std::to_string(valor));
  }
  return valor;
}

}  // namespace

// `celulas_` é construído UMA vez, com o tamanho certo. Atribuir no corpo o
// construiria vazio antes e o redimensionaria depois.
grade::grade(int largura, int altura)
    : largura_(exigir_positivo(largura, "largura")),
      altura_(exigir_positivo(altura, "altura")),
      celulas_(static_cast<std::size_t>(largura_) * static_cast<std::size_t>(altura_)) {}

bool grade::dentro(vetor2 p) const noexcept {
  return p.x >= 0 && p.y >= 0 && p.x < largura_ && p.y < altura_;
}

const celula& grade::em(vetor2 p) const {
  return celulas_[static_cast<std::size_t>(p.y) * static_cast<std::size_t>(largura_) +
                  static_cast<std::size_t>(p.x)];
}

celula& grade::em(vetor2 p) {
  return celulas_[static_cast<std::size_t>(p.y) * static_cast<std::size_t>(largura_) +
                  static_cast<std::size_t>(p.x)];
}

std::size_t grade::bytes_das_celulas() const noexcept {
  return celulas_.size() * sizeof(celula);
}

}  // namespace deriva
