// Aula 22 - quantos incrementos uma corrida de dados perde
#ifndef DERIVA_MEDIDA_CORRIDA_HPP
#define DERIVA_MEDIDA_CORRIDA_HPP

#include <cstddef>
#include <mutex>
#include <thread>
#include <vector>

namespace deriva::medida {

/// Como `leiaute.hpp` e `medida_posse.hpp`, este cabeçalho não entra no jogo.
/// Ele existe porque o interativo e o Cap. 22 afirmam que a corrida perde
/// incrementos, e afirmação sem número medido é exatamente o que este
/// repositório não aceita.
///
/// Atenção ao que se está medindo: corrida de dados é comportamento
/// indefinido, e o resultado **varia entre execuções**. Não há um número a
/// travar em `static_assert`; o que se mede é a FAIXA, e é a variação que é a
/// lição. Um bug que às vezes não aparece é pior que um bug que sempre
/// aparece, porque o teste verde não prova nada.
///
/// A thread e o mutex só chegam na v2.4 (Aula 22). Aqui está o mínimo.
struct corrida {
  int perdidos_min = 0;
  int perdidos_max = 0;
  int execucoes_sem_perda = 0;
  int execucoes = 0;
  int esperado = 0;
};

/// `vivos` compartilhado, sem proteção, incrementado por duas threads.
[[nodiscard]] inline int contar_sem_mutex(int por_thread) {
  int vivos = 0;
  auto somar = [&vivos, por_thread] {
    for (int i = 0; i < por_thread; ++i) {
      ++vivos;          // lê, soma, escreve: três passos, nenhum atômico
    }
  };
  std::thread a(somar), b(somar);
  a.join();
  b.join();
  return vivos;
}

/// O mesmo, com a seção crítica serializada. `scoped_lock` é C++17 e
/// substitui `lock_guard` por aceitar mais de um mutex.
[[nodiscard]] inline int contar_com_mutex(int por_thread) {
  int vivos = 0;
  std::mutex m;
  auto somar = [&vivos, &m, por_thread] {
    for (int i = 0; i < por_thread; ++i) {
      const std::scoped_lock trava(m);
      ++vivos;
    }
  };
  std::thread a(somar), b(somar);
  a.join();
  b.join();
  return vivos;
}

[[nodiscard]] inline corrida medir(int execucoes = 20, int por_thread = 100000) {
  corrida r;
  r.execucoes = execucoes;
  r.esperado = 2 * por_thread;
  r.perdidos_min = r.esperado;
  for (int k = 0; k < execucoes; ++k) {
    const int perdidos = r.esperado - contar_sem_mutex(por_thread);
    if (perdidos < r.perdidos_min) r.perdidos_min = perdidos;
    if (perdidos > r.perdidos_max) r.perdidos_max = perdidos;
    if (perdidos == 0) ++r.execucoes_sem_perda;
  }
  return r;
}

}  // namespace deriva::medida

#endif
