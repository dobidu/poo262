// Aula 13 - o que um ciclo de shared_ptr realmente vaza
#ifndef DERIVA_MEDIDA_POSSE_HPP
#define DERIVA_MEDIDA_POSSE_HPP

#include <cstddef>
#include <memory>
#include <string>

namespace deriva::medida {

/// Como `leiaute.hpp`, este cabeçalho não entra no jogo: existe para que o
/// número que o interativo "grafo de posse" exibe seja o que esta libstdc++
/// realmente vaza, e não uma estimativa.
///
/// O grafo de conexões da estação chega na v1.3 (Aula 13). Aqui está só o nó
/// mínimo que responde à pergunta: quantos bytes ficam presos quando dois
/// `shared_ptr` seguram um ao outro?
struct no {
  std::string nome;
  std::shared_ptr<no> vizinho;   // posse: conta na referência
  std::weak_ptr<no> volta;       // observação: não conta
};

/// Os contadores vivem FORA do template, e há um motivo que custou uma
/// depuração: `std::allocate_shared` não usa o alocador que você passa. Ele o
/// rebinda para o tipo interno do bloco de controle, e um `inline static`
/// dentro de `contando<T>` passaria a contar em `contando<no>` enquanto as
/// alocações reais aconteceriam em `contando<_Sp_counted_ptr_inplace<...>>`.
/// A primeira versão deste cabeçalho media zero byte vazado por isso.
struct contagem {
  inline static std::size_t pedidos = 0;
  inline static std::size_t devolvidos = 0;
  inline static std::size_t bytes_pedidos = 0;
  inline static std::size_t bytes_devolvidos = 0;

  static void zerar() noexcept {
    pedidos = devolvidos = bytes_pedidos = bytes_devolvidos = 0;
  }
  [[nodiscard]] static std::size_t vazados() noexcept {
    return bytes_pedidos - bytes_devolvidos;
  }
};

/// Alocador que conta. Passado a `std::allocate_shared`, ele vê exatamente o
/// que o `shared_ptr` pede: o bloco de controle e o objeto, na mesma
/// alocação. Contar com um `operator new` global misturaria as alocações do
/// próprio arcabouço de teste.
template <class T>
struct contando {
  using value_type = T;

  contando() noexcept = default;
  template <class U>
  explicit contando(const contando<U>&) noexcept {}

  [[nodiscard]] T* allocate(std::size_t n) {
    ++contagem::pedidos;
    contagem::bytes_pedidos += n * sizeof(T);
    return static_cast<T*>(::operator new(n * sizeof(T)));
  }
  void deallocate(T* p, std::size_t n) noexcept {
    ++contagem::devolvidos;
    contagem::bytes_devolvidos += n * sizeof(T);
    ::operator delete(p);
  }
  template <class U>
  bool operator==(const contando<U>&) const noexcept { return true; }
  template <class U>
  bool operator!=(const contando<U>&) const noexcept { return false; }
};

/// Monta o ciclo, deixa os dois `shared_ptr` locais morrerem, e devolve
/// quantos bytes ficaram presos. Com `usar_weak`, uma das pontas passa a
/// observar em vez de possuir, e o resultado tem de ser zero.
template <class Aloc>
[[nodiscard]] std::size_t bytes_presos(bool usar_weak) {
  contagem::zerar();
  {
    auto a = std::allocate_shared<no>(Aloc{}, no{"eclusa", nullptr, {}});
    auto b = std::allocate_shared<no>(Aloc{}, no{"corredor", nullptr, {}});
    a->vizinho = b;
    if (usar_weak) {
      b->volta = a;      // observa: a contagem de `a` não sobe
    } else {
      b->vizinho = a;    // possui: fecha o ciclo, e ninguém chega a zero
    }
  }
  return contagem::vazados();
}

}  // namespace deriva::medida

#endif

namespace deriva::medida {

// ---------------------------------------------------------------------------
// Aula 12 · quanto custa um `unique_ptr`
//
// O Cap. 12 afirma que `unique_ptr` com deletor padrão é do tamanho de um
// ponteiro cru, e que um deletor COM ESTADO cobra o estado dele. Os dois
// números vinham sem lastro; aqui estão medidos.
// ---------------------------------------------------------------------------

/// Deletor sem estado. É uma classe vazia, e a otimização de base vazia faz o
/// `unique_ptr` caber num ponteiro.
struct deletor_sem_estado {
  void operator()(int* p) const noexcept { delete p; }
};

/// Deletor COM estado: guarda de onde o objeto veio, para registrar. O estado
/// não tem onde caber senão dentro do `unique_ptr`.
struct deletor_com_estado {
  const char* origem = nullptr;
  void operator()(int* p) const noexcept { delete p; }
};

static_assert(sizeof(std::unique_ptr<int>) == sizeof(int*),
              "com o deletor padrao, um ponteiro e nada mais");
static_assert(sizeof(std::unique_ptr<int, deletor_sem_estado>) == sizeof(int*),
              "deletor vazio: a otimizacao de base vazia o absorve");
static_assert(sizeof(std::unique_ptr<int, deletor_com_estado>) ==
                  sizeof(int*) + sizeof(const char*),
              "deletor com estado cobra o estado dele, e o dobro e visivel");

/// E a comparação que o capítulo usa: `shared_ptr` é o dobro de um ponteiro,
/// porque leva também o ponteiro para o bloco de controle.
static_assert(sizeof(std::shared_ptr<int>) == 2 * sizeof(int*),
              "objeto mais bloco de controle");
static_assert(sizeof(std::weak_ptr<int>) == 2 * sizeof(int*),
              "weak carrega o mesmo par, e nao possui");

}  // namespace deriva::medida
