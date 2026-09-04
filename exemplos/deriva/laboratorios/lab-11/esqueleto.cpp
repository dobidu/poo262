// LAB-11 · esqueleto · prepara a Aula 20
// Portão: garantia de exceção declarada e cumprida, e o desenrolar da pilha
// chamando os destrutores.
#include <cstdio>
#include <optional>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

namespace {

std::vector<std::string> traco;

struct recurso {
  explicit recurso(std::string nome) : nome_(std::move(nome)) {
    traco.push_back("+" + nome_);
  }
  ~recurso() { traco.push_back("-" + nome_); }
  recurso(const recurso&) = delete;
  recurso& operator=(const recurso&) = delete;
  std::string nome_;
};

class erro_de_carga : public std::runtime_error {
 public:
  explicit erro_de_carga(const std::string& m) : std::runtime_error(m) {}
};

enum class razao { vazio, torto, sem_entrada };

/// `variant` para erro ESPERADO com informação: quem chama decide.
[[nodiscard]] std::variant<std::string, razao> interpretar(const std::string& t) {
  if (t.empty()) return razao::vazio;
  if (t.find('@') == std::string::npos) return razao::sem_entrada;
  if (t.find("##\n#") != std::string::npos) return razao::torto;
  return t;
}

/// `optional` para AUSÊNCIA: não é erro, é resposta.
[[nodiscard]] std::optional<std::string> procurar(const std::string& nome) {
  if (nome == "estacao-01") return std::string("#@#");
  return std::nullopt;
}

/// Exceção para o que ROMPE a operação, com garantia FORTE: ou o alvo fica
/// com o conteúdo novo, ou fica exatamente como estava.
///
/// Copiar-e-trocar é o que a compra: a cópia pode lançar, e se lançar o alvo
/// nem foi tocado. Atribuir membro a membro daria garantia básica - o objeto
/// ficaria válido, mas pela metade.
void carregar_em(std::string& alvo, const std::string& nome) {
  const std::optional<std::string> achado = procurar(nome);
  if (!achado) throw erro_de_carga("nao existe: " + nome);

  const auto r = interpretar(*achado);
  if (const razao* p = std::get_if<razao>(&r)) {
    throw erro_de_carga("conteudo invalido, razao " +
                        std::to_string(static_cast<int>(*p)));
  }

  // TODO: esta linha da garantia BASICA - o alvo fica valido, mas pela
  // metade se algo lancar no meio. Troque por copiar-e-trocar e explique a
  // diferenca por escrito.
  alvo = std::get<std::string>(r);
}

}  // namespace

int main() {
  int falhas = 0;
  auto checar = [&falhas](const char* o_que, bool ok) {
    std::printf("  %-54s %s\n", o_que, ok ? "OK" : "FALHA");
    if (!ok) ++falhas;
  };

  checar("optional: ausencia nao e erro", !procurar("nao-existe").has_value());
  checar("variant: erro esperado carrega a razao",
         std::get<razao>(interpretar("")) == razao::vazio);
  checar("e o caso valido devolve o conteudo",
         std::holds_alternative<std::string>(interpretar("#@#")));

  // Garantia forte: o alvo fica intacto quando a operação falha.
  std::string setor = "conteudo-anterior";
  bool lancou = false;
  try { carregar_em(setor, "nao-existe"); } catch (const erro_de_carga&) { lancou = true; }
  checar("a excecao foi lancada", lancou);
  checar("garantia FORTE: o alvo ficou EXATAMENTE como estava",
         setor == "conteudo-anterior");

  carregar_em(setor, "estacao-01");
  checar("e o caminho de sucesso troca o conteudo", setor == "#@#");

  // O desenrolar chama os destrutores, de dentro para fora.
  traco.clear();
  try {
    const recurso externo("arquivo");
    const recurso interno("buffer");
    throw erro_de_carga("falha no meio");
  } catch (const erro_de_carga&) {
    traco.push_back("!capturada");
  }
  std::string t;
  for (const std::string& l : traco) t.append(l).push_back('|');
  checar("o desenrolar destroi de dentro para fora",
         t == "+arquivo|+buffer|-buffer|-arquivo|!capturada|");

  std::printf("\nportao LAB-11: %s\n", falhas == 0 ? "OK" : "FALHA");
  return falhas == 0 ? 0 : 1;
}
