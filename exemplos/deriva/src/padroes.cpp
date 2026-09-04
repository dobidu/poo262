#include "deriva/padroes.hpp"

#include <utility>

#include "deriva/mundo.hpp"

namespace deriva {

std::unique_ptr<i_tela> tela_mapa::comando(std::string_view c) {
  if (c == "i") return std::make_unique<tela_inventario>();
  if (c == "x") return std::make_unique<tela_inspecao>();
  return nullptr;   // fica onde está
}

std::unique_ptr<i_tela> tela_inventario::comando(std::string_view c) {
  if (c == "esc") return std::make_unique<tela_mapa>();
  return nullptr;
}

std::unique_ptr<i_tela> tela_inspecao::comando(std::string_view c) {
  if (c == "esc") return std::make_unique<tela_mapa>();
  if (c == "i") return std::make_unique<tela_inventario>();
  return nullptr;
}

console::console() : atual_(std::make_unique<tela_mapa>()) {}

void console::comando(std::string_view c) {
  historico_.emplace_back(atual_->nome());
  if (std::unique_ptr<i_tela> proxima = atual_->comando(c)) {
    atual_ = std::move(proxima);
  }
}

void com_numero_de_linha::desenhar(const mundo& m) {
  ++linha_;
  dentro_->mensagem("[" + std::to_string(linha_) + "]");
  dentro_->desenhar(m);
}

void com_numero_de_linha::mensagem(std::string_view texto) {
  ++linha_;
  dentro_->mensagem("[" + std::to_string(linha_) + "] " + std::string(texto));
}

void com_moldura::desenhar(const mundo& m) {
  // Caracteres reais de box-drawing, os mesmos do site.
  dentro_->mensagem("┌─┤ " + titulo_ + " ├─┐");
  dentro_->desenhar(m);
  dentro_->mensagem("└──┘");
}

void com_moldura::mensagem(std::string_view texto) { dentro_->mensagem(texto); }

registro_global& registro_global::instancia() {
  // Singleton de Meyers: estático local, inicializado uma vez, seguro entre
  // threads desde C++11. É a versão correta da forma errada.
  static registro_global unico;
  return unico;
}

void registro_global::anotar(std::string_view evento) {
  eventos_.emplace_back(evento);
}

void anotar_em(i_observador& onde, std::string_view evento) {
  onde.aconteceu(evento);
}

}  // namespace deriva
