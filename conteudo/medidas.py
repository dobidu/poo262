# -*- coding: utf-8 -*-
"""GERADO por build/medir_deriva.py - não edite.

Os números que a prosa do site e do livro afirmam, medidos no Deriva que
compila. Para mudar um número, mude o CÓDIGO.

Medido na versão v2.7: 188 testes verdes, vptr de 8 bytes, ciclo de shared_ptr prendendo 160 bytes.
"""

MEDIDAS = {
    'versao': 'v2.7',
    'testes_por_versao': {
        'v0.1': 4,
        'v0.2': 12,
        'v0.3': 8,
        'v1.0': 7,
        'v1.2': 7,
        'v1.3': 4,
        'v1.4': 5,
        'v1.5': 5,
        'v1.6': 5,
        'v1.7': 6,
        'v1.8': 5,
        'v2.0': 8,
        'v2.2': 6,
        'v2.3': 8,
        'v2.4': 5,
        'v2.5': 7,
        'v2.6': 27,
    },
    'testes_por_aula': {
        'Aula 01': 7,
        'Aula 03': 5,
        'Aula 04': 6,
        'Aula 05': 6,
        'Aula 06': 8,
        'Aula 07/11': 4,
        'Aula 13': 5,
        'Aula 14': 4,
        'Aula 22': 2,
    },
    'testes_deriva': 176,
    'testes_labs': 12,
    'variantes_escritas': ['v0.2-quebrada', 'v0.3-quebrada', 'v1.1-quebrada', 'v2.6-antes'],
    'testes': 188,
    'sizeof': {
        'celula': 12,
        'celula_ingenua': 16,
        'drone': 16,
        'drone_com_carga': 24,
        'drone_simples': 8,
        'entidade': 16,
        'entidade_simples': 8,
        'vetor2': 8,
    },
    'vptr': 8,
    'no': 64,
    'diamante': {
        'composta': 56,
        'duplicada': 40,
        'unica': 48,
    },
    'construcoes_de_texto': 2,
    'ciclo_bytes': 160,
    'padrao': 'c++17',
    'avisos': 0,
}

# GERADO junto: o comando e o arquivo que fixam cada medida.
PROCEDENCIA = {
    'avisos': ('make verifica', 'Makefile'),
    'celula': ('./build/deriva --leiaute', 'include/deriva/celula.hpp'),
    'ciclo_bytes': ('./build/testes "*copiar*"', 'testes/test_posse.cpp'),
    'construcoes_de_texto': ('./build/testes "*mapa*"', 'testes/test_mapa.cpp'),
    'diamante': ('./build/testes "*heranca virtual custa mais*"', 'include/deriva/diamante.hpp'),
    'no': ('./build/testes "*copiar*"', 'testes/test_posse.cpp'),
    'sizeof': ('./build/deriva --leiaute', 'include/deriva/leiaute.hpp'),
    'testes': ('ctest --test-dir build', 'CMakeLists.txt'),
    'testes_deriva': ('ctest --test-dir build', 'CMakeLists.txt'),
    'testes_labs': ('ctest --test-dir build -N', 'laboratorios/CMakeLists.txt'),
    'variantes_escritas': ('ls variantes/', 'variantes/'),
    'vptr': ('./build/deriva --leiaute', 'testes/test_leiaute.cpp'),
}
