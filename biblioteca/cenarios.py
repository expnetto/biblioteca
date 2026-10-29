from __future__ import annotations

from datetime import date, timedelta

from .biblioteca import Biblioteca
from .dominio import Livro, Usuario

ACERVO = (
    ("L1", "Dom Casmurro", "Machado de Assis", "Literatura Brasileira"),
    ("L2", "Grande Sertao: Veredas", "Joao Guimaraes Rosa", "Literatura Brasileira"),
    ("L3", "Estruturas de Dados", "Niklaus Wirth", "Computacao"),
    ("L4", "Codigo Limpo", "Robert C. Martin", "Computacao"),
    ("L5", "Calculo Volume 1", "James Stewart", "Matematica"),
    ("L6", "Breve Historia do Tempo", "Stephen Hawking", "Divulgacao Cientifica"),
)

COMUNIDADE = (
    ("U1", "Eraldo Xavier Pimentel Netto", "2023110001"),
    ("U2", "Mariana Alves de Souza", "2023110002"),
    ("U3", "Joao Pedro Carvalho", "2023110003"),
    ("U4", "Beatriz Nogueira Lima", "2023110004"),
)


def biblioteca_vazia() -> Biblioteca:
    return Biblioteca()


def biblioteca_povoada() -> Biblioteca:
    biblioteca = biblioteca_vazia()
    for identificador, titulo, autor, categoria in ACERVO:
        biblioteca.cadastrar_livro(Livro(identificador, titulo, autor, categoria))
    for identificador, nome, matricula in COMUNIDADE:
        biblioteca.cadastrar_usuario(Usuario(identificador, nome, matricula))
    return biblioteca


def cenario_em_dia(data_base: date) -> Biblioteca:
    biblioteca = biblioteca_povoada()
    biblioteca.registrar_emprestimo(
        "L1", "U1", data_base - timedelta(days=3), data_base + timedelta(days=11)
    )
    biblioteca.registrar_emprestimo(
        "L3", "U2", data_base - timedelta(days=1), data_base + timedelta(days=13)
    )
    biblioteca.registrar_emprestimo("L5", "U3", data_base, data_base)
    return biblioteca


def cenario_com_atrasos(data_base: date) -> Biblioteca:
    biblioteca = biblioteca_povoada()
    biblioteca.registrar_emprestimo(
        "L1", "U1", data_base - timedelta(days=30), data_base - timedelta(days=16)
    )
    biblioteca.registrar_emprestimo(
        "L2", "U2", data_base - timedelta(days=20), data_base - timedelta(days=6)
    )
    biblioteca.registrar_emprestimo(
        "L3", "U1", data_base - timedelta(days=15), data_base - timedelta(days=1)
    )
    biblioteca.registrar_emprestimo(
        "L4", "U3", data_base - timedelta(days=40), data_base - timedelta(days=26)
    )
    return biblioteca


def cenario_misto(data_base: date) -> Biblioteca:
    biblioteca = biblioteca_povoada()
    biblioteca.registrar_emprestimo(
        "L1", "U1", data_base - timedelta(days=5), data_base + timedelta(days=9)
    )
    biblioteca.registrar_emprestimo(
        "L2", "U2", data_base - timedelta(days=25), data_base - timedelta(days=11)
    )
    biblioteca.registrar_emprestimo(
        "L3", "U3", data_base - timedelta(days=18), data_base - timedelta(days=4)
    )
    devolvido_em_dia = biblioteca.registrar_emprestimo(
        "L4", "U4", data_base - timedelta(days=20), data_base - timedelta(days=6)
    )
    biblioteca.registrar_devolucao(
        devolvido_em_dia.identificador, data_base - timedelta(days=8)
    )
    devolvido_com_atraso = biblioteca.registrar_emprestimo(
        "L5", "U1", data_base - timedelta(days=50), data_base - timedelta(days=36)
    )
    biblioteca.registrar_devolucao(
        devolvido_com_atraso.identificador, data_base - timedelta(days=30)
    )
    return biblioteca


CENARIOS = (
    ("Com atrasos", cenario_com_atrasos),
    ("Em dia", cenario_em_dia),
    ("Misto (ativos, atrasados e devolvidos)", cenario_misto),
    ("Vazio", lambda data_base: biblioteca_vazia()),
)
