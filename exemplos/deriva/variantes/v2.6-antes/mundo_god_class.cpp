// Deriva v2.6-antes · CAÇA AO BUG 3 - semana 13 · Aula 24
//
// O `mundo` como god class. Esta variante COMPILA, passa nos testes que
// acompanham, e faz tudo o que a versão refatorada faz. O defeito não é
// funcional: é que ela tem sete motivos para mudar, e por isso qualquer
// alteração arrisca as outras seis responsabilidades.
//
// A caça ao bug 3 não é "ache o erro". É: **refatore sob SOLID e prove que a
// saída não mudou**. A prova é o replay - despejo idêntico byte a byte. O erro
// que a semana 13 caça é a refatoração que muda a saída sem que ninguém note.
//
//   g++ -std=c++17 -Wall -Wextra -Wpedantic mundo_god_class.cpp -o antes
//   ./antes > /tmp/antes.txt
//   # refatore, e depois:
//   diff /tmp/antes.txt <(./depois)
#include <algorithm>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

namespace deriva_antes {

struct vetor2 {
  int x = 0, y = 0;
  bool operator==(const vetor2& o) const { return x == o.x && y == o.y; }
};

struct entidade {
  virtual ~entidade() = default;
  virtual char glifo() const = 0;
  vetor2 pos;
};
struct sonda : entidade {
  char glifo() const override { return '@'; }
  int energia = 100;
};
struct drone : entidade {
  char glifo() const override { return 'd'; }
  vetor2 rumo{1, 0};
};

/// AS SETE RESPONSABILIDADES. Cada uma é um motivo independente para editar
/// este arquivo, e é essa contagem - não o número de linhas - que a Aula 24
/// pede para medir.
class mundo {
 public:
  mundo(int largura, int altura) : largura_(largura), altura_(altura) {
    terreno_.assign(static_cast<std::size_t>(largura * altura), '.');
    for (int x = 0; x < largura; ++x) {
      terreno_[idx({x, 0})] = '#';
      terreno_[idx({x, altura - 1})] = '#';
    }
    for (int y = 0; y < altura; ++y) {
      terreno_[idx({0, y})] = '#';
      terreno_[idx({largura - 1, y})] = '#';
    }
  }

  // (1) estado do domínio
  void acrescentar(std::unique_ptr<entidade> e) { entidades_.push_back(std::move(e)); }
  bool livre(vetor2 p) const {
    return p.x >= 0 && p.y >= 0 && p.x < largura_ && p.y < altura_ &&
           terreno_[idx(p)] != '#';
  }

  // (2) RENDER. Escreve direto em `std::cout`, e é isso que torna a troca por
  // Qt impossível sem editar esta classe. Também impede testar sem capturar a
  // saída do processo.
  void desenhar() const {
    for (int y = 0; y < altura_; ++y) {
      for (int x = 0; x < largura_; ++x) {
        char c = terreno_[idx({x, y})];
        for (const auto& e : entidades_) {
          if (e->pos == vetor2{x, y}) c = e->glifo();
        }
        std::cout << c;
      }
      std::cout << '\n';
    }
  }

  // (3) ENTRADA. O `switch` de comandos mora aqui, e por isso não há onde
  // guardar o desfazer.
  bool comando(const std::string& c) {
    sonda* s = nullptr;
    for (const auto& e : entidades_) {
      if (auto* p = dynamic_cast<sonda*>(e.get())) s = p;
    }
    if (!s) return false;
    vetor2 alvo = s->pos;
    if (c == "norte") alvo.y -= 1;
    else if (c == "sul") alvo.y += 1;
    else if (c == "leste") alvo.x += 1;
    else if (c == "oeste") alvo.x -= 1;
    else if (c == "esperar") { /* nada */ }
    else return false;
    if (!livre(alvo)) { registrar("bloqueado"); return false; }
    s->pos = alvo;
    registrar("moveu");
    return true;
  }

  // (4) IA. O comportamento de cada tipo está codificado aqui, com
  // `dynamic_cast`, em vez de na entidade ou numa estratégia.
  void turno() {
    for (const auto& e : entidades_) {
      if (auto* d = dynamic_cast<drone*>(e.get())) {
        vetor2 alvo{d->pos.x + d->rumo.x, d->pos.y + d->rumo.y};
        if (livre(alvo)) d->pos = alvo;
        else d->rumo = {-d->rumo.x, -d->rumo.y};
      }
    }
  }

  // (5) LOG. Abre o arquivo aqui dentro, então o teste que quiser verificar o
  // log precisa mexer no sistema de arquivos.
  void registrar(const std::string& evento) {
    std::ofstream log("deriva.log", std::ios::app);
    log << evento << '\n';
  }

  // (6) PERSISTÊNCIA. O formato do save também mora aqui.
  std::string salvar() const {
    std::string s = "antes 1\n";
    for (const auto& e : entidades_) {
      s += e->glifo();
      s += " " + std::to_string(e->pos.x) + " " + std::to_string(e->pos.y) + "\n";
    }
    return s;
  }

  // (7) CRIAÇÃO. A tabela de glifos, uma terceira vez com `dynamic_cast`.
  void povoar(const std::string& glifos) {
    int x = 1, y = 1;
    for (const char g : glifos) {
      if (g == '@') { auto s = std::make_unique<sonda>(); s->pos = {x, y}; acrescentar(std::move(s)); }
      else if (g == 'd') { auto d = std::make_unique<drone>(); d->pos = {x, y}; acrescentar(std::move(d)); }
      if (++x >= largura_ - 1) { x = 1; ++y; }
    }
  }

 private:
  std::size_t idx(vetor2 p) const {
    return static_cast<std::size_t>(p.y) * static_cast<std::size_t>(largura_) +
           static_cast<std::size_t>(p.x);
  }
  int largura_, altura_;
  std::vector<char> terreno_;
  std::vector<std::unique_ptr<entidade>> entidades_;
};

}  // namespace deriva_antes

int main() {
  using namespace deriva_antes;
  mundo w(12, 6);
  w.povoar("@dd");

  std::cout << "== v2.6-antes: sete responsabilidades numa classe\n";
  w.desenhar();
  for (const char* c : {"leste", "leste", "sul", "oeste"}) {
    (void)w.comando(c);
    w.turno();
  }
  std::cout << "\n== depois de quatro comandos\n";
  w.desenhar();
  std::cout << "\n== save\n" << w.salvar();

  std::cout << "\nOs sete motivos para editar esta classe:\n"
               "  1 estado do dominio   2 render      3 entrada\n"
               "  4 IA                  5 log         6 persistencia\n"
               "  7 criacao de entidade\n\n"
               "Refatore sob SOLID e prove pelo replay que esta saida nao mudou.\n";
  return 0;
}
