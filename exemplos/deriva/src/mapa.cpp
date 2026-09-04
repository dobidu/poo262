#include "deriva/mapa.hpp"

#include <fstream>
#include <sstream>
#include <utility>
#include <vector>

namespace deriva {

mapa::mapa(std::string nome, int largura, int altura)
    : nome_(std::move(nome)),
      grade_(largura, altura),
      marca_("mapa:" + nome_) {
  ++contador_mapa::vivos;
  ++contador_mapa::criados;
}

mapa::~mapa() { --contador_mapa::vivos; }

// Destrutor declarado → a cópia precisa ser declarada também: é a regra do
// três (Aula 09). Aqui ela é rasa de propósito? Não: `grade_` é um vector, e
// copiá-lo copia as células. O que a cópia manual acrescenta é só o
// incremento do contador - sem ele, `vivos` fecharia negativo, porque o
// destrutor da cópia decrementaria algo que ninguém incrementou.
mapa::mapa(const mapa& o)
    : nome_(o.nome_), grade_(o.grade_), entrada_(o.entrada_), marca_(o.marca_) {
  ++contador_mapa::vivos;
  ++contador_mapa::criados;
}

mapa& mapa::operator=(const mapa& o) {
  if (this != &o) {
    nome_ = o.nome_;
    grade_ = o.grade_;
    entrada_ = o.entrada_;
    marca_ = o.marca_;
  }
  return *this;  // o contador não muda: nenhum objeto nasceu nem morreu
}

// Mover um mapa não copia a grade: o `std::vector` de dentro dela transfere o
// ponteiro do heap. O que ainda custa é o contador - um objeto NASCEU, mesmo
// que sem alocar, e por isso `criados` sobe.
//
// `noexcept` não é decoração: `std::vector<mapa>` só usa o movimento ao
// realocar se ele for `noexcept`; sem a palavra, ele copia (Aula 14).
mapa::mapa(mapa&& o) noexcept
    : nome_(std::move(o.nome_)),
      grade_(std::move(o.grade_)),
      entrada_(o.entrada_),
      marca_(std::move(o.marca_)) {
  ++contador_mapa::vivos;
  ++contador_mapa::criados;
}

mapa& mapa::operator=(mapa&& o) noexcept {
  if (this != &o) {
    nome_ = std::move(o.nome_);
    grade_ = std::move(o.grade_);
    entrada_ = o.entrada_;
    marca_ = std::move(o.marca_);
  }
  return *this;   // nem nasceu nem morreu ninguém: o contador não muda
}

std::optional<mapa> mapa::de_texto(std::string_view texto, std::string nome) {
  // `string_view` não possui os bytes: `texto` tem de continuar vivo durante
  // toda esta função. É por isso que as fileiras abaixo são `string_view`
  // para dentro de `texto`, e nada disso é guardado depois (Aula 03).
  std::vector<std::string_view> fileiras;
  std::size_t inicio = 0;
  while (inicio <= texto.size()) {
    const std::size_t fim = texto.find('\n', inicio);
    std::string_view linha = texto.substr(
        inicio, fim == std::string_view::npos ? std::string_view::npos : fim - inicio);
    if (!linha.empty()) fileiras.push_back(linha);
    if (fim == std::string_view::npos) break;
    inicio = fim + 1;
  }

  if (fileiras.empty()) return std::nullopt;

  const std::size_t largura = fileiras.front().size();
  for (std::string_view f : fileiras) {
    if (f.size() != largura) return std::nullopt;  // fileira torta: não é mapa
  }

  mapa m(std::move(nome), static_cast<int>(largura),
         static_cast<int>(fileiras.size()));

  // Ligação estruturada sobre índice e conteúdo seria mais elegante com
  // `enumerate`, que é C++23. Aqui, um laço com índice explícito.
  for (int y = 0; y < static_cast<int>(fileiras.size()); ++y) {
    for (int x = 0; x < static_cast<int>(largura); ++x) {
      const char c = fileiras[static_cast<std::size_t>(y)][static_cast<std::size_t>(x)];
      celula& cel = m.grade_.em({x, y});
      cel.glifo = c;
      switch (c) {
        case '#': cel.massa = 1000; break;             // parede: não se move
        case '!': cel.massa = 3; cel.energia = 1; break;
        case '@': m.entrada_ = {x, y}; cel.glifo = '.'; break;
        default: break;
      }
    }
  }
  return m;
}

std::optional<mapa> mapa::carregar(const std::filesystem::path& caminho) {
  std::error_code ec;
  if (!std::filesystem::exists(caminho, ec) || ec) return std::nullopt;
  if (!std::filesystem::is_regular_file(caminho, ec) || ec) return std::nullopt;

  std::ifstream arq(caminho);
  if (!arq) return std::nullopt;
  std::ostringstream buf;
  buf << arq.rdbuf();
  const std::string texto = buf.str();
  return de_texto(texto, caminho.stem().string());
}

std::string mapa::despejar() const {
  std::string s;
  s.reserve(static_cast<std::size_t>(grade_.largura() + 1) *
            static_cast<std::size_t>(grade_.altura()) + 64);
  s.append("mapa ").append(nome_).append(" ")
   .append(std::to_string(grade_.largura())).append("x")
   .append(std::to_string(grade_.altura())).append("\n");
  s.append("entrada ").append(std::to_string(entrada_.x)).append(",")
   .append(std::to_string(entrada_.y)).append("\n");
  for (int y = 0; y < grade_.altura(); ++y) {
    for (int x = 0; x < grade_.largura(); ++x) s.push_back(grade_.em({x, y}).glifo);
    s.push_back('\n');
  }
  return s;
}

std::ostream& operator<<(std::ostream& os, const mapa& m) {
  return os << m.despejar();
}

}  // namespace deriva
