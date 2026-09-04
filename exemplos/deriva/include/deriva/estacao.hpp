// v1.3 · Aula 13 - posse compartilhada: shared_ptr, weak_ptr e o ciclo
#ifndef DERIVA_ESTACAO_HPP
#define DERIVA_ESTACAO_HPP

#include <memory>
#include <string>
#include <string_view>
#include <vector>

namespace deriva {

/// Um setor da estação, como nó de um grafo de conexões.
///
/// Aqui a posse é **compartilhada de verdade**, e não por preguiça: uma eclusa
/// pertence aos dois corredores que ela liga, e nenhum dos dois pode
/// destruí-la sozinho. É o requisito que `shared_ptr` atende e `unique_ptr`
/// não.
///
/// As conexões para frente são `shared_ptr`: possuem. A conexão de volta é
/// `weak_ptr`: **observa sem possuir**, e é essa assimetria que impede o
/// ciclo. Trocar `volta` por `shared_ptr` fecha o ciclo e prende 160 bytes por
/// par de nós, medidos em `testes/test_posse.cpp`.
class no_estacao {
 public:
  inline static int vivos = 0;
  inline static int criados = 0;

  explicit no_estacao(std::string nome);
  ~no_estacao();

  no_estacao(const no_estacao&) = delete;
  no_estacao& operator=(const no_estacao&) = delete;

  [[nodiscard]] std::string_view nome() const noexcept { return nome_; }

  /// Liga `a` a `b` para frente, e `b` a `a` de volta - a de volta por
  /// `weak_ptr`. Função livre, e não método, porque a operação é sobre o par
  /// e não sobre um dos nós.
  static void ligar(const std::shared_ptr<no_estacao>& a,
                    const std::shared_ptr<no_estacao>& b);

  [[nodiscard]] std::size_t grau() const noexcept { return adiante_.size(); }
  [[nodiscard]] const std::vector<std::shared_ptr<no_estacao>>& adiante() const noexcept {
    return adiante_;
  }

  /// O nó anterior, se ainda existir. `weak_ptr` obriga a perguntar, e é essa
  /// pergunta que torna o ponteiro pendurado impossível.
  [[nodiscard]] std::shared_ptr<no_estacao> anterior() const { return volta_.lock(); }

  /// Verdadeiro quando o nó anterior já morreu. Com `shared_ptr` esta
  /// pergunta não teria como ser respondida: ele nunca morreria.
  [[nodiscard]] bool anterior_perdido() const noexcept {
    return !volta_.expired() ? false : volta_.use_count() == 0 && !volta_.lock();
  }

 private:
  std::string nome_;
  std::vector<std::shared_ptr<no_estacao>> adiante_;
  std::weak_ptr<no_estacao> volta_;
};

/// Percorre a partir da raiz em profundidade, na ordem de ligação, e devolve
/// os nomes. Determinístico: é o que o teste compara.
[[nodiscard]] std::string percorrer(const std::shared_ptr<no_estacao>& raiz);

void zerar_estacao() noexcept;

}  // namespace deriva

#endif
