// v1.8 · Aula 18 - polimorfismo dinâmico, RTTI e dynamic_cast
#ifndef DERIVA_INSPETOR_HPP
#define DERIVA_INSPETOR_HPP

#include <string>

#include "deriva/entidade.hpp"

namespace deriva {

class mundo;

/// O inspetor do console: aponta para uma entidade e diz o que ela é.
///
/// É o **único** lugar do Deriva onde `dynamic_cast` é a resposta e não o
/// sintoma, e a diferença tem critério: aqui a pergunta é "de que tipo é
/// isto?", feita por uma ferramenta de diagnóstico que existe justamente para
/// olhar de fora. Em código de domínio, `dynamic_cast` quase sempre significa
/// que uma função virtual está faltando (Aula 18).
///
/// Compare com `entidade::descrever`, que resolve o mesmo problema por
/// despacho virtual, sem perguntar o tipo, e é a forma correta para o domínio.
[[nodiscard]] std::string inspecionar(const entidade& e);

/// Só as entidades que sabem reparar, encontradas por `dynamic_cast`. É a
/// consulta que herança pública não expressa: "quem implementa esta
/// interface?".
[[nodiscard]] std::string listar_reparadoras(const mundo& m);

/// O nome do tipo dinâmico, sem desembaralhar. Serve para mostrar que
/// `typeid` responde sobre o tipo REAL, e que o nome que ele devolve é
/// definido pela implementação - não é para ser exibido a usuário.
[[nodiscard]] std::string tipo_cru(const entidade& e);

}  // namespace deriva

#endif
