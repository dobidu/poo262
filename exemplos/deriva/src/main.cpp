// Deriva · v0.3 - o console. Sonda de inspeção numa estação orbital.
//
// Ainda não é o jogo: é o que a Unidade I entrega. Render do setor, um
// roteiro determinístico de movimentos, e as três técnicas de verificação que
// não dependem de ferramenta externa - contador de instâncias vivas,
// instrumentação de ciclo de vida, e um destrutor onde pôr ponto de parada.
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <string_view>
#include <vector>

#include "deriva/contador.hpp"
#include "deriva/entidade.hpp"
#include "deriva/fov.hpp"
#include "deriva/grade.hpp"
#include "deriva/inspetor.hpp"
#include "deriva/mundo.hpp"
#include "deriva/reparadora.hpp"
#include "deriva/instrumento.hpp"
#include "deriva/leiaute.hpp"
#include "deriva/mapa.hpp"
#include "deriva/terminal_bruto.hpp"
#include "deriva/vetor2.hpp"

namespace {

/// Gerador congruente linear, com constantes de Numerical Recipes.
///
/// Não é `std::mt19937` nem, muito menos, `std::random_device`: precisa ser
/// reproduzível byte a byte em qualquer máquina, porque é sobre isso que o
/// replay da Aula 16 se apoia. Aleatoriedade de verdade seria pior aqui.
class sorteio {
 public:
  explicit sorteio(unsigned semente) noexcept : estado_(semente) {}

  [[nodiscard]] unsigned proximo() noexcept {
    estado_ = estado_ * 1664525u + 1013904223u;
    return estado_;
  }
  [[nodiscard]] int ate(int limite) noexcept {
    return limite <= 0 ? 0 : static_cast<int>(proximo() % static_cast<unsigned>(limite));
  }

 private:
  unsigned estado_;
};

void semear_itens(deriva::mapa& m, unsigned semente, int quantos) {
  sorteio s(semente);
  const deriva::grade& g = m.g();
  int postos = 0;
  for (int tentativa = 0; tentativa < 4000 && postos < quantos; ++tentativa) {
    const deriva::vetor2 p{s.ate(g.largura()), s.ate(g.altura())};
    deriva::celula& c = m.g().em(p);
    if (c.glifo != '.') continue;
    c.glifo = '!';
    c.massa = 3;
    c.energia = 1;
    ++postos;
  }
}

struct passo_do_roteiro {
  std::string comando;
  deriva::vetor2 delta;
};

[[nodiscard]] std::vector<passo_do_roteiro> ler_roteiro(const std::string& caminho) {
  std::vector<passo_do_roteiro> passos;
  std::ifstream arq(caminho);
  std::string linha;
  while (std::getline(arq, linha)) {
    if (linha.empty() || linha.front() == '#') continue;
    // ligação estruturada (C++17) sobre a tabela de comandos
    static const std::pair<std::string_view, deriva::vetor2> tabela[] = {
        {"norte", {0, -1}}, {"sul", {0, 1}}, {"leste", {1, 0}},
        {"oeste", {-1, 0}}, {"esperar", {0, 0}}};
    for (const auto& [nome, delta] : tabela) {
      if (linha == nome) {
        passos.push_back({linha, delta});
        break;
      }
    }
  }
  return passos;
}

/// Monta o mundo da v1.2: o setor, a sonda na entrada, os drones de patrulha e
/// os itens semeados. Determinístico dada a semente.
[[nodiscard]] deriva::mundo montar_mundo(deriva::mapa m, unsigned semente) {
  semear_itens(m, semente, 6);
  const deriva::vetor2 entrada = m.entrada();

  // Antes de tomar posse do mapa, colher onde os itens ficaram: eles viram
  // entidades, e o terreno volta a ser piso.
  std::vector<deriva::vetor2> onde_itens;
  for (int y = 0; y < m.g().altura(); ++y) {
    for (int x = 0; x < m.g().largura(); ++x) {
      const deriva::vetor2 p{x, y};
      if (m[p].glifo == '!') {
        onde_itens.push_back(p);
        m[p].glifo = '.';
        m[p].massa = 0;
        m[p].energia = 0;
      }
    }
  }

  deriva::mundo w(std::move(m));
  w.acrescentar(std::make_unique<deriva::sonda>(entrada));
  w.acrescentar(std::make_unique<deriva::sonda_reparadora>(
      deriva::vetor2{entrada.x, entrada.y + 1}));

  sorteio s(semente ^ 0x9E37u);
  for (int k = 0; k < 2; ++k) {
    const deriva::vetor2 rumo = k == 0 ? deriva::vetor2{1, 0} : deriva::vetor2{0, 1};
    for (int tentativa = 0; tentativa < 500; ++tentativa) {
      const deriva::vetor2 p{s.ate(w.setor().g().largura()),
                             s.ate(w.setor().g().altura())};
      if (w.livre(p)) {
        w.acrescentar(std::make_unique<deriva::drone>(p, rumo));
        break;
      }
    }
  }
  for (const deriva::vetor2& p : onde_itens) {
    w.acrescentar(std::make_unique<deriva::item>(p, "sucata", 3));
  }
  return w;
}

int replay(const std::string& caminho_mapa, const std::string& roteiro,
           unsigned semente) {
  std::optional<deriva::mapa> m = deriva::mapa::carregar(caminho_mapa);
  if (!m) {
    std::cerr << "deriva: nao foi possivel carregar o mapa '" << caminho_mapa << "'\n";
    return 2;
  }
  deriva::mundo w = montar_mundo(std::move(*m), semente);

  deriva::entidade* sonda_ptr = w.primeira_com('@');
  int carga = 0;

  std::cout << "replay semente=" << semente << " mapa=" << w.setor().nome() << '\n';
  std::cout << "entidades " << w.quantas() << '\n';
  std::cout << "sonda " << sonda_ptr->pos().x << ',' << sonda_ptr->pos().y
            << " carga=0\n";

  for (const passo_do_roteiro& p : ler_roteiro(roteiro)) {
    const deriva::vetor2 alvo = sonda_ptr->pos() + p.delta;
    const bool livre = w.livre(alvo);
    if (livre) {
      sonda_ptr->mover_para(alvo);
      // Item na célula de destino: a sonda o recolhe, e ele deixa o mundo.
      if (std::unique_ptr<deriva::entidade> pegou = w.retirar_de(alvo)) {
        if (const auto* it = dynamic_cast<const deriva::item*>(pegou.get())) {
          carga += it->massa();
        } else {
          (void)w.acrescentar(std::move(pegou));   // não era item: devolve
        }
      }
    }
    w.turno();   // e só então o resto do mundo age
    std::cout << p.comando << ' ' << (livre ? "ok" : "bloqueado") << ' '
              << sonda_ptr->pos().x << ',' << sonda_ptr->pos().y
              << " carga=" << carga << '\n';
  }
  std::cout << w.despejar();
  return 0;
}

void imprimir_leiaute() {
  using namespace deriva;
  std::cout << "estrutura                bytes\n"
            << "vetor2                   " << sizeof(vetor2) << '\n'
            << "celula                   " << sizeof(celula) << '\n'
            << "celula_ingenua           " << sizeof(celula_ingenua) << '\n'
            << "leiaute::entidade_simples " << sizeof(leiaute::entidade_simples) << '\n'
            << "leiaute::drone_simples   " << sizeof(leiaute::drone_simples) << '\n'
            << "leiaute::entidade        " << sizeof(leiaute::entidade) << '\n'
            << "leiaute::drone           " << sizeof(leiaute::drone) << '\n'
            << "leiaute::drone_com_carga " << sizeof(leiaute::drone_com_carga) << '\n'
            << "custo do vptr            "
            << sizeof(leiaute::entidade) - sizeof(leiaute::entidade_simples) << '\n';
}

int inspecionar_tudo(const std::string& caminho_mapa, unsigned semente) {
  std::optional<deriva::mapa> m = deriva::mapa::carregar(caminho_mapa);
  if (!m) {
    std::cerr << "deriva: nao foi possivel carregar o mapa\n";
    return 2;
  }
  const deriva::mundo w = montar_mundo(std::move(*m), semente);
  std::cout << "inspecao de " << w.quantas() << " entidade(s)\n";
  for (std::size_t i = 0; i < w.quantas(); ++i) {
    std::cout << "  " << deriva::inspecionar(w.em(i)) << '\n';
  }
  std::cout << deriva::listar_reparadoras(w);
  return 0;
}

int mostrar_fov(const std::string& caminho_mapa, unsigned semente, int raio) {
  std::optional<deriva::mapa> m = deriva::mapa::carregar(caminho_mapa);
  if (!m) {
    std::cerr << "deriva: nao foi possivel carregar o mapa\n";
    return 2;
  }
  const deriva::vetor2 origem = m->entrada();
  semear_itens(*m, semente, 6);
  std::cout << deriva::despejar_fov(*m, origem, raio);
  return 0;
}

void ajuda() {
  std::cout <<
      "uso: deriva [opcoes]\n"
      "  --render                desenha o setor e sai\n"
      "  --inspecionar           lista as entidades por tipo dinamico (v1.8)\n"
      "  --fov [RAIO]            campo de visao a partir da entrada (v1.6)\n"
      "  --replay ROTEIRO        executa o roteiro e despeja o estado final\n"
      "  --semente N             semente do sorteio (padrao 7)\n"
      "  --mapa CAMINHO          mapa a carregar (padrao mapas/estacao-01.txt)\n"
      "  --contadores            imprime vivos=N depois de tudo destruido\n"
      "  --instrumentar          ecoa construcao e destruicao em stderr\n"
      "  --traco                 imprime o traco de ciclo de vida no fim\n"
      "  --leiaute               imprime o sizeof de cada estrutura\n";
}

}  // namespace

int main(int argc, char** argv) {
  std::string caminho_mapa = "mapas/estacao-01.txt";
  std::string roteiro;
  unsigned semente = 7;
  bool quer_render = false, quer_contadores = false, quer_traco = false;
  bool quer_inspecao = false, quer_fov = false;
  int raio = 6;

  for (int i = 1; i < argc; ++i) {
    const std::string_view a = argv[i];
    const auto proximo = [&](std::string& destino) {
      if (i + 1 < argc) destino = argv[++i];
    };
    if (a == "--render") quer_render = true;
    else if (a == "--inspecionar") quer_inspecao = true;
    else if (a == "--fov") {
      quer_fov = true;
      if (i + 1 < argc && argv[i + 1][0] != '-') raio = std::atoi(argv[++i]);
    }
    else if (a == "--replay") proximo(roteiro);
    else if (a == "--mapa") proximo(caminho_mapa);
    else if (a == "--semente") { std::string s; proximo(s); semente = static_cast<unsigned>(std::strtoul(s.c_str(), nullptr, 10)); }
    else if (a == "--contadores") quer_contadores = true;
    else if (a == "--instrumentar") deriva::instrumento::ecoar(true);
    else if (a == "--traco") quer_traco = true;
    else if (a == "--leiaute") { imprimir_leiaute(); return 0; }
    else if (a == "--ajuda" || a == "-h") { ajuda(); return 0; }
    else { std::cerr << "deriva: opcao desconhecida '" << a << "'\n"; ajuda(); return 2; }
  }

  int saida = 0;
  {
    // Escopo explícito: tudo tem de morrer ANTES de o contador ser lido. Se o
    // `vivos` fosse impresso aqui dentro, ele nunca acusaria vazamento algum.
    const deriva::terminal_bruto term;
    (void)term;

    if (!roteiro.empty()) {
      saida = replay(caminho_mapa, roteiro, semente);
    } else if (quer_inspecao) {
      saida = inspecionar_tudo(caminho_mapa, semente);
    } else if (quer_fov) {
      saida = mostrar_fov(caminho_mapa, semente, raio);
    } else if (quer_render) {
      std::optional<deriva::mapa> m = deriva::mapa::carregar(caminho_mapa);
      if (!m) {
        std::cerr << "deriva: nao foi possivel carregar o mapa '" << caminho_mapa << "'\n";
        saida = 2;
      } else {
        semear_itens(*m, semente, 6);
        std::cout << m->despejar();
      }
    } else if (!quer_contadores && !quer_traco) {
      ajuda();
    }
  }

  if (quer_traco) std::cout << deriva::instrumento::despejo();
  if (quer_contadores) {
    std::cout << "vivos=" << deriva::total_vivos() + deriva::entidades_vivas()
              << " criados=" << deriva::contador_mapa::criados +
                                 deriva::contador_terminal::criados << '\n';
  }
  return saida;
}
