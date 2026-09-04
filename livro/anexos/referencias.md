# Referências Bibliográficas

A regra que organiza esta lista está no plano do livro: **a bibliografia do livro se alinha à do plano de ensino, e não o contrário.** A do plano de ensino passou por auditoria; a do livro v1 não tinha passado, e o que segue é o resultado de a ter alinhado. As decisões que a auditoria produziu estão registradas aqui, e não em nota de rodapé, porque uma bibliografia é lista de decisões e não lista de títulos.

Três correções de autoria e de edição entraram. A do Catch2 é a maior: no v1 a referência aparecia **sem autoria nenhuma**, e a biblioteca é de **Phil Nash e Martin Hořeňovský**. O *Programming: Principles and Practice Using C++* está na **3ª edição, de 2024**, e não constava da lista do livro, apesar de constar da do plano de ensino. E o **FTXUI é de Arthur Sonzogni**, o que vale registrar porque uma versão anterior deste material atribuía a biblioteca a outra pessoa - invenção, e não erro de digitação, que é a categoria de defeito que uma auditoria de bibliografia existe para pegar.

Uma referência entrou por decisão de escopo: **Josuttis, *C++17 - The Complete Guide***, que cobre o padrão-alvo construção por construção e é a fonte do Anexo B. Ele é publicado pelo próprio autor, pela Leanpub, e o registro dessa natureza fica aqui para que a escolha seja informada: título autopublicado costuma ser motivo de recusa, e neste caso não é, porque Josuttis é membro do comitê de padronização e o livro é a cobertura mais completa do C++17 que existe.

Duas referências do v1 **saíram**, e as duas por não estarem na bibliografia do plano de ensino. A primeira era uma *Introdução à programação orientada a objetos com C++* entrada por `MENDES`, e a auditoria encontrou nela um defeito de autoria antes de encontrar o de escopo: a obra é de Antônio Mendes da Silva Filho, sobrenome composto tratado como nome do meio, e a entrada correta começaria por `SILVA FILHO`. Corrigir a entrada e mantê-la seria alinhar o livro a si mesmo em vez de ao plano, e por isso ela foi retirada. A segunda era um *C++: como programar* de Deitel e Deitel, sem edição e sem ano, com a nota "edição mais recente disponível no acervo" no lugar do dado - o que funciona num plano de ensino, que é documento anual, e deixa uma referência de livro sem identificação. Nenhuma das duas foi substituída por invenção, e a decisão de retirar é reversível pelo caminho normal: se qualquer das duas voltar à bibliografia do plano, ela volta a esta lista com os dados conferidos no acervo.

Sobre duplicatas, a conferência foi feita e não achou nenhuma. Os pares que parecem duplicata não são: Stroustrup aparece três vezes, Meyers duas, Martin duas, Fowler duas e Josuttis duas, sempre com obras distintas. O par que mais se confunde é o de Josuttis, e vale desfazer a confusão de uma vez - *The C++ Standard Library* (2012) é referência de biblioteca padrão, e *C++17 - The Complete Guide* (2019) é o do padrão-alvo desta disciplina.

Uma última decisão, e ela é a que o v1 mais precisava: onde a obra original e a tradução brasileira coexistem, **o original é a referência**, como no plano de ensino, e as traduções ficam num bloco separado ao fim, identificadas como tais e registradas por serem os exemplares que o estudante encontra no acervo da BC/UFPB. O v1 citava as traduções nas listas principais e o site citava os originais, o que é exatamente a divergência entre livro e site que a arquitetura de fonte única existe para impedir.

## Referências Básicas

1\. STROUSTRUP, Bjarne. *A Tour of C++*. 3. ed. Boston: Addison-Wesley, 2022.

2\. STROUSTRUP, Bjarne. *Programming: Principles and Practice Using C++*. 3. ed. Boston: Addison-Wesley, 2024.

3\. MEYERS, Scott. *Effective Modern C++: 42 Specific Ways to Improve Your Use of C++11 and C++14*. Sebastopol: O'Reilly, 2014.

4\. JOSUTTIS, Nicolai M. *C++17 - The Complete Guide*. Leanpub, 2019.

5\. GAMMA, Erich; HELM, Richard; JOHNSON, Ralph; VLISSIDES, John. *Design Patterns: Elements of Reusable Object-Oriented Software*. Boston: Addison-Wesley, 1994.

## Referências Complementares

1\. ISO/IEC 14882:2017. *Programming languages - C++* (C++17).

2\. STROUSTRUP, Bjarne. *The C++ Programming Language*. 4. ed. Boston: Addison-Wesley, 2013.

3\. STROUSTRUP, Bjarne; SUTTER, Herb (eds.). *C++ Core Guidelines*. Disponível em: https://isocpp.github.io/CppCoreGuidelines

4\. SUTTER, Herb; ALEXANDRESCU, Andrei. *C++ Coding Standards: 101 Rules, Guidelines, and Best Practices*. Boston: Addison-Wesley, 2004.

5\. VANDEVOORDE, David; JOSUTTIS, Nicolai M.; GREGOR, Douglas. *C++ Templates: The Complete Guide*. 2. ed. Boston: Addison-Wesley, 2017.

6\. MARTIN, Robert C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Boston: Prentice Hall, 2017.

7\. OUSTERHOUT, John. *A Philosophy of Software Design*. 2. ed. Palo Alto: Yaknyam Press, 2021.

8\. FREEMAN, Steve; PRYCE, Nat. *Growing Object-Oriented Software, Guided by Tests*. Boston: Addison-Wesley, 2009.

9\. FOWLER, Martin. *Refactoring: Improving the Design of Existing Code*. 2. ed. Boston: Addison-Wesley, 2018.

10\. FOWLER, Martin; SCOTT, Kendall. *UML Distilled*. 3. ed. Boston: Addison-Wesley, 2003.

11\. CHACON, Scott; STRAUB, Ben. *Pro Git*. 2. ed. New York: Apress, 2014. Disponível em: https://git-scm.com/book

12\. BERRYMAN, John; ZIEGLER, Albert. *Prompt Engineering for LLMs*. Sebastopol: O'Reilly, 2024.

## Documentação de Ferramenta e de Biblioteca

As versões são fixadas e publicadas no início do semestre, e o Cap. 2 explica por que a tag não flutua.

1\. cppreference.com. *Referência do C++*. Disponível em: https://en.cppreference.com

2\. SONZOGNI, Arthur. *FTXUI - Functional Terminal (X) User interface*. Disponível em: https://github.com/ArthurSonzogni/FTXUI. Versão fixada para o semestre: `v5.0.0`.

3\. NASH, Phil; HOŘEŇOVSKÝ, Martin *et al*. *Catch2 - A modern, C++-native test framework*. Disponível em: https://github.com/catchorg/Catch2. Versão fixada para o semestre.

4\. THE QT COMPANY. *Qt Documentation*. Disponível em: https://doc.qt.io

5\. LOHMANN, Niels. *JSON for Modern C++*. Disponível em: https://github.com/nlohmann/json

## Referências em Português, no Acervo da BC/UFPB

Estas são as edições em português das obras acima, ou obras próximas a elas, e estão registradas por serem as que o estudante encontra no acervo. Onde a tradução e o original coexistem na lista, **o original é a referência**, e a tradução é o exemplar consultável.

1\. MEYERS, Scott. *C++ Moderno e Eficaz: 42 formas específicas de aprimorar seu uso de C++11 e C++14*. Rio de Janeiro: Alta Books, 2015. [Tradução de *Effective Modern C++*.]

2\. MEYERS, Scott. *C++ eficaz: 55 maneiras de aprimorar seus programas e projetos*. 3. ed. Porto Alegre: Bookman, 2011. [Tradução de *Effective C++*, 3ª ed.]

3\. GAMMA, Erich; HELM, Richard; JOHNSON, Ralph; VLISSIDES, John. *Padrões de projeto: soluções reutilizáveis de software orientados a objetos*. Porto Alegre: Bookman, 2000. [Tradução de *Design Patterns*.]

4\. MARTIN, Robert C. *Arquitetura limpa: o guia do artesão para estrutura e design de software*. Rio de Janeiro: Alta Books, 2019. [Tradução de *Clean Architecture*.]

5\. MARTIN, Robert C. *Código limpo: habilidades práticas do Agile Software*. Rio de Janeiro: Alta Books, 2009.

6\. FOWLER, Martin. *UML essencial: um breve guia para a linguagem-padrão de modelagem de objetos*. 3. ed. Porto Alegre: Bookman, 2005. [Tradução de *UML Distilled*.]

7\. JOSUTTIS, Nicolai M. *The C++ Standard Library: a tutorial and reference*. 2. ed. Boston: Addison-Wesley, 2012.

## Material da Disciplina

BATISTA, Carlos Eduardo Coelho Freire. *Programação Orientada a Objetos em C++ - POO/UFPB*. Livro, 26 aulas com exemplos interativos, e o repositório do **Deriva** com as versões que compilam. Distribuído via SIGAA e pelo site da disciplina.

## Nota sobre a seção de documentação

Duas entradas da seção de ferramenta e de biblioteca não constam do plano de ensino, e as duas ficam por razão declarada. A documentação do **Qt** fica porque o Cap. 26 depende dela para ser conduzido, mesmo sendo aquela aula demonstração sem entrega. E o **`nlohmann/json`** fica com a autoria creditada, como reconhecimento de API: o Cap. 23 decide **não** usar JSON no Deriva, e a §23.6 explica por quê, de forma que a entrada serve ao estudante que vai encontrar a biblioteca fora daqui, e não a uma dependência deste repositório - o `CMakeLists.txt` fixa FTXUI e Catch2, e mais nada.

A conformidade com a ABNT, incluindo a forma de entrada de sobrenome composto e o uso de itálico, é trabalho de normalização e não entra aqui. As entradas seguem o formato que o plano de ensino já usa.
