// LAB-08 · esqueleto · prepara a Aula 14
// Portão: instrumentar o ciclo de vida e LER a ordem na saída, distinguindo
// cópia de movimento sem adivinhar.
#include <cstdio>
#include <string>
#include <utility>
#include <vector>

namespace {

std::vector<std::string> traco;

/// A instrumentação distingue as CINCO operações. Sem sufixo próprio para cada
/// uma, o traço diz que algo nasceu e não diz de onde - e é justamente essa a
/// pergunta da Aula 14.
class carga {
 public:
  explicit carga(std::string rotulo, std::size_t bytes)
      : rotulo_(std::move(rotulo)), dados_(bytes, 0) {
    traco.push_back("+" + rotulo_);
  }
  ~carga() { traco.push_back("-" + rotulo_); }

  carga(const carga& o) : rotulo_(o.rotulo_ + "'"), dados_(o.dados_) {
    traco.push_back("+" + rotulo_ + " (copia de " + o.rotulo_ + ")");
  }
  // TODO 1: falta uma palavra nesta assinatura, e ela decide se o
  // `std::vector` move ou copia ao realocar. Rode o caso 3 sem ela.
  carga(carga&& o)
      : rotulo_(std::move(o.rotulo_) + "^"), dados_(std::move(o.dados_)) {
    // TODO 2: o traco tem de DISTINGUIR movimento de copia. Sem sufixo
    // proprio, ele diz que algo nasceu e nao diz de onde.
    traco.push_back("+" + rotulo_);
  }
  carga& operator=(const carga& o) {
    if (this != &o) { rotulo_ = o.rotulo_ + "'"; dados_ = o.dados_; }
    traco.push_back("=copia " + rotulo_);
    return *this;
  }
  carga& operator=(carga&& o) noexcept {
    if (this != &o) { rotulo_ = std::move(o.rotulo_) + "^"; dados_ = std::move(o.dados_); }
    traco.push_back("=move " + rotulo_);
    return *this;
  }

  [[nodiscard]] std::size_t bytes() const noexcept { return dados_.size(); }
  [[nodiscard]] const void* onde() const noexcept { return dados_.data(); }

 private:
  std::string rotulo_;
  std::vector<char> dados_;
};

[[nodiscard]] std::string despejo() {
  std::string s;
  for (const std::string& l : traco) s.append(l).push_back('\n');
  return s;
}

}  // namespace

int main() {
  int falhas = 0;
  auto checar = [&falhas](const char* o_que, bool ok) {
    std::printf("  %-52s %s\n", o_que, ok ? "OK" : "FALHA");
    if (!ok) ++falhas;
  };

  // (1) cópia: os bytes são duplicados, e o endereço muda.
  traco.clear();
  {
    const carga a("a", 1024);
    const void* antes = a.onde();
    const carga b = a;
    checar("copia: o destino tem buffer proprio", b.onde() != antes);
    checar("copia: e a origem continua com os bytes", a.bytes() == 1024);
  }
  checar("copia: o traco mostra DUAS construcoes e DUAS destruicoes",
         despejo() == "+a\n+a' (copia de a)\n-a'\n-a\n");

  // (2) movimento: o mesmo endereço troca de dono.
  traco.clear();
  {
    carga a("a", 1024);
    const void* antes = a.onde();
    const carga b = std::move(a);
    checar("move: o destino recebeu o MESMO buffer", b.onde() == antes);
    checar("move: e a origem ficou sem bytes", a.bytes() == 0);
  }
  // A última linha é "-" e não "-a": o rótulo da origem foi MOVIDO para o
  // destino, então o destrutor dela não tem mais nome para imprimir. A
  // instrumentação foi afetada pelo movimento que ela mede - e o conserto é
  // deixar o rótulo fora do que se move, ou aceitar o traço anônimo e saber
  // ler o que ele significa.
  checar("move: o traco distingue movida de copia, e a origem perdeu o nome",
         despejo() == "+a\n+a^ (movida)\n-a^\n-\n");

  // (3) `std::vector` só usa o movimento ao realocar se ele for `noexcept`.
  traco.clear();
  {
    std::vector<carga> v;
    v.reserve(1);
    v.emplace_back("x", 8);
    v.emplace_back("y", 8);   // realoca: move `x`, não copia
  }
  const bool moveu_ao_realocar = despejo().find("(movida)") != std::string::npos;
  checar("vector realocou movendo, e nao copiando", moveu_ao_realocar);

  std::printf("\nportao LAB-08: %s\n", falhas == 0 ? "OK" : "FALHA");
  if (falhas == 0) {
    std::printf("\nAgora retire o `noexcept` do construtor de movimento e rode\n"
                "de novo. O ultimo caso passa a mostrar copia, e o motivo esta\n"
                "na garantia que o `vector` precisa dar ao realocar.\n");
  }
  return falhas == 0 ? 0 : 1;
}
