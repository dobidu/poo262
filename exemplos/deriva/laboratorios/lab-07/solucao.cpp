// LAB-07 · solução de referência · prepara a Aula 13
// Portão: escolher a posse por REQUISITO, provocar o ciclo e desfazê-lo.
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

namespace {

int vivos = 0;

struct no {
  explicit no(std::string nome) : nome_(std::move(nome)) { ++vivos; }
  ~no() { --vivos; }
  no(const no&) = delete;
  no& operator=(const no&) = delete;

  std::string nome_;
  std::vector<std::shared_ptr<no>> adiante_;   // possui
  std::weak_ptr<no> volta_;                    // observa
};

/// Requisito 1: um dono, e o tempo de vida é o do dono. `unique_ptr`.
struct inventario {
  std::vector<std::unique_ptr<no>> pecas;
};

/// Requisito 2: dois donos legítimos, e nenhum pode destruir sozinho.
/// `shared_ptr`, e a volta por `weak_ptr` para não fechar ciclo.
void ligar(const std::shared_ptr<no>& a, const std::shared_ptr<no>& b) {
  a->adiante_.push_back(b);
  b->volta_ = a;
}

/// O ciclo, de propósito, para ser medido.
void ligar_com_ciclo(const std::shared_ptr<no>& a, const std::shared_ptr<no>& b) {
  a->adiante_.push_back(b);
  b->adiante_.push_back(a);   // possui de volta: ninguem chega a zero
}

}  // namespace

int main() {
  int falhas = 0;
  auto checar = [&falhas](const char* o_que, bool ok) {
    std::printf("  %-52s %s\n", o_que, ok ? "OK" : "FALHA");
    if (!ok) ++falhas;
  };

  // (1) posse exclusiva: o requisito é "um dono".
  {
    inventario inv;
    inv.pecas.push_back(std::make_unique<no>("chave"));
    inv.pecas.push_back(std::make_unique<no>("cabo"));
    checar("unique_ptr: dois vivos, um dono cada", vivos == 2);
  }
  checar("unique_ptr: o dono morreu e levou os dois", vivos == 0);

  // (2) posse compartilhada com volta fraca.
  {
    auto a = std::make_shared<no>("eclusa");
    auto b = std::make_shared<no>("corredor");
    ligar(a, b);
    checar("shared: a contagem de b subiu para 2", b.use_count() == 2);
    checar("shared: a de a NAO subiu, porque a volta e fraca", a.use_count() == 1);
    checar("weak: e a volta responde enquanto o alvo vive", b->volta_.lock() != nullptr);
  }
  checar("shared+weak: os dois morreram", vivos == 0);

  // (3) o ciclo, provocado e medido.
  {
    auto a = std::make_shared<no>("a");
    auto b = std::make_shared<no>("b");
    ligar_com_ciclo(a, b);
    checar("ciclo: as duas contagens em 2", a.use_count() == 2 && b.use_count() == 2);
  }
  checar("ciclo: DOIS objetos vazaram, e ninguem os alcanca", vivos == 2);

  // (4) e desfeito, para provar que a diferença é a ponta fraca.
  vivos = 0;
  {
    auto a = std::make_shared<no>("a");
    auto b = std::make_shared<no>("b");
    ligar(a, b);
  }
  checar("com weak na volta, nada vaza", vivos == 0);

  std::printf("\nportao LAB-07: %s\n", falhas == 0 ? "OK" : "FALHA");
  return falhas == 0 ? 0 : 1;
}
