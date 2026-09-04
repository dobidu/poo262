// LAB-05 · solução de referência · prepara a Aula 8
// Portão: o traço de ciclo de vida bate linha por linha com o roteiro, e o
// recurso é restaurado mesmo quando uma exceção passa por cima dele.
#include <cstdio>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

std::vector<std::string> traco;

/// RAII sobre um recurso simulado: um "modo" global que precisa ser
/// restaurado. É o `terminal_bruto` sem o termios, para o laboratório poder
/// rodar em pipe.
int modo_do_sistema = 0;

class modo_bruto {
 public:
  explicit modo_bruto(int novo) : anterior_(modo_do_sistema) {
    modo_do_sistema = novo;
    traco.push_back("+modo " + std::to_string(novo));
  }
  ~modo_bruto() {
    modo_do_sistema = anterior_;   // a linha que separa RAII de promessa
    traco.push_back("-modo " + std::to_string(anterior_));
  }
  modo_bruto(const modo_bruto&) = delete;
  modo_bruto& operator=(const modo_bruto&) = delete;

 private:
  int anterior_;
};

class marca {
 public:
  explicit marca(std::string nome) : nome_(std::move(nome)) {
    traco.push_back("+" + nome_);
  }
  ~marca() { traco.push_back("-" + nome_); }
  marca(const marca&) = delete;
  marca& operator=(const marca&) = delete;

 private:
  std::string nome_;
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
    std::printf("  %-46s %s\n", o_que, ok ? "OK" : "FALHA");
    if (!ok) ++falhas;
  };

  // Roteiro 1: saída normal. A ordem de destruição é a inversa, sempre.
  traco.clear();
  {
    const marca a("mapa");
    const modo_bruto m(1);
    { const marca b("sonda"); }
  }
  checar("ordem inversa na saida normal",
         despejo() == "+mapa\n+modo 1\n+sonda\n-sonda\n-modo 0\n-mapa\n");
  checar("o modo foi restaurado", modo_do_sistema == 0);

  // Roteiro 2: exceção. Ela CHAMA os destrutores ao desenrolar - não os pula.
  traco.clear();
  try {
    const marca externo("externo");
    const modo_bruto m(2);
    const marca interno("interno");
    throw std::runtime_error("falha de leitura do setor");
  } catch (const std::runtime_error&) {
    traco.push_back("!capturada");
  }
  checar("a excecao desenrola de dentro para fora",
         despejo() == "+externo\n+modo 2\n+interno\n-interno\n-modo 0\n-externo\n!capturada\n");
  checar("o modo foi restaurado apesar da excecao", modo_do_sistema == 0);

  // Roteiro 3: aninhamento. Cada escopo restaura o que ele mesmo mudou.
  traco.clear();
  {
    const modo_bruto fora(1);
    { const modo_bruto dentro(2); checar("o modo interno vale enquanto vive", modo_do_sistema == 2); }
    checar("e o externo volta ao sair do interno", modo_do_sistema == 1);
  }
  checar("e o sistema volta ao inicio", modo_do_sistema == 0);

  std::printf("\nportao LAB-05: %s\n", falhas == 0 ? "OK" : "FALHA");
  return falhas == 0 ? 0 : 1;
}
