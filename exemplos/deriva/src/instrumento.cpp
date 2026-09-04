#include "deriva/instrumento.hpp"

#include <iostream>
#include <utility>

namespace deriva {
namespace {
std::vector<std::string>& traco_mutavel() {
  static std::vector<std::string> t;
  return t;
}
bool& eco() {
  static bool e = false;
  return e;
}
}  // namespace

void instrumento::anotar(std::string_view o_que, std::string_view quem) {
  std::string linha;
  linha.reserve(o_que.size() + quem.size() + 1);
  linha.append(o_que).append(quem);
  if (eco()) std::cerr << "[ciclo] " << linha << '\n';
  traco_mutavel().push_back(std::move(linha));
}

void instrumento::ecoar(bool ligado) noexcept { eco() = ligado; }

const std::vector<std::string>& instrumento::traco() noexcept {
  return traco_mutavel();
}

void instrumento::limpar() { traco_mutavel().clear(); }

std::string instrumento::despejo() {
  std::string s;
  for (const std::string& l : traco_mutavel()) s.append(l).push_back('\n');
  return s;
}

marca_de_vida::marca_de_vida(std::string nome) : nome_(std::move(nome)) {
  instrumento::anotar("+", nome_);
}

marca_de_vida::~marca_de_vida() { instrumento::anotar("-", nome_); }

// A cópia é anotada com sufixo próprio: é assim que o estudante vê, no traço,
// que houve uma cópia que ele não pediu.
marca_de_vida::marca_de_vida(const marca_de_vida& o) : nome_(o.nome_ + "'") {
  instrumento::anotar("+", nome_);
}

marca_de_vida& marca_de_vida::operator=(const marca_de_vida& o) {
  if (this != &o) {
    instrumento::anotar("=", nome_);
    nome_ = o.nome_ + "'";
  }
  return *this;
}

marca_de_vida::marca_de_vida(marca_de_vida&& o) noexcept
    : nome_(std::move(o.nome_) + "^") {
  instrumento::anotar("+", nome_);
}

marca_de_vida& marca_de_vida::operator=(marca_de_vida&& o) noexcept {
  if (this != &o) {
    instrumento::anotar("=", nome_);
    nome_ = std::move(o.nome_) + "^";
  }
  return *this;
}

}  // namespace deriva
