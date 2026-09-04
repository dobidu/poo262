// LAB-02 · solução de referência · prepara a Aula 3
// Portão: os quatro casos de tempo de vida reproduzidos e explicados; nenhum
// deles lê memória liberada.
#include <cstdio>
#include <cstring>
#include <map>
#include <string>
#include <string_view>

namespace {

/// (1) A vista aponta, não possui. Mesmo endereço, e nenhuma cópia.
[[nodiscard]] bool caso_aponta() {
  const std::string dono = "eclusa-norte-setor-03";
  const std::string_view vista = dono;
  return vista.data() == dono.data() && vista.size() == dono.size();
}

/// (2) `substr` de vista não copia; de string, sim.
[[nodiscard]] bool caso_substr() {
  const std::string dono = "###.@.###";
  const std::string copiado = dono.substr(3, 3);
  const std::string_view visto = std::string_view(dono).substr(3, 3);
  return copiado.data() != dono.data() + 3 && visto.data() == dono.data() + 3;
}

/// (3) A vista não termina em nul. `strlen` sobre `data()` lê além dela.
[[nodiscard]] bool caso_sem_nul() {
  const std::string dono = "eclusa-norte";
  const std::string_view prefixo = std::string_view(dono).substr(0, 6);
  return prefixo.size() == 6 && std::strlen(prefixo.data()) == dono.size();
}

/// (4) O que a função GUARDA tem de possuir. `nome` é `std::string` por isso.
struct setor {
  std::string nome;                      // possui: sobrevive à chamada
  explicit setor(std::string_view n) : nome(n) {}   // recebe vista, guarda cópia
};

[[nodiscard]] bool caso_guarda() {
  setor s{"efemero"};
  {
    const std::string temporario = "setor-que-vai-morrer";
    s = setor{temporario};
  }  // `temporario` morreu, e `s.nome` continua íntegro
  return s.nome == "setor-que-vai-morrer";
}

/// Ligação estruturada sobre `std::map`, por referência const.
[[nodiscard]] std::string glifos_ordenados() {
  const std::map<char, std::string_view> tabela{
      {'#', "parede"}, {'.', "piso"}, {'@', "entrada"}, {'!', "item"}};
  std::string s;
  for (const auto& [glifo, nome] : tabela) {   // const auto&: nada é copiado
    s.push_back(glifo);
    s.push_back('=');
    s.append(nome);
    s.push_back(' ');
  }
  return s;
}

/// `[[nodiscard]]` no que devolve status: ignorar é sempre erro.
[[nodiscard]] bool carregou(std::string_view texto) { return !texto.empty(); }

}  // namespace

int main() {
  struct caso { const char* nome; bool ok; };
  const caso casos[] = {
      {"1 a vista aponta, nao possui", caso_aponta()},
      {"2 substr de vista nao copia", caso_substr()},
      {"3 a vista nao termina em nul", caso_sem_nul()},
      {"4 o que se guarda tem de possuir", caso_guarda()},
  };

  bool tudo = true;
  for (const caso& c : casos) {
    std::printf("  %-36s %s\n", c.nome, c.ok ? "OK" : "FALHA");
    tudo = tudo && c.ok;
  }
  std::printf("\nglifos: %s\n", glifos_ordenados().c_str());
  const bool leu = carregou("#@#");
  std::printf("carregou: %s\n", leu ? "sim" : "nao");

  std::printf("\nportao LAB-02: %s\n", tudo && leu ? "OK" : "FALHA");
  return tudo && leu ? 0 : 1;
}
