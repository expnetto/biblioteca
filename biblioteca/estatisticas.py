from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from functools import reduce

from .consultas import emprestimos_ativos
from .dominio import Emprestimo, Livro
from .multas import emprestimos_atrasados, relatorio_de_multas


@dataclass(frozen=True)
class Estatisticas:
    data_referencia: date
    livros_por_categoria: dict[str, int]
    emprestimos_por_usuario: dict[str, int]
    emprestimos_ativos: int
    emprestimos_ativos_em_atraso: int
    valor_total_das_multas: float


def quantidade_de_livros_por_categoria(livros: Iterable[Livro]) -> dict[str, int]:
    return reduce(
        lambda contagem, livro: {
            **contagem,
            livro.categoria: contagem.get(livro.categoria, 0) + 1,
        },
        livros,
        {},
    )


def quantidade_de_emprestimos_por_usuario(
    emprestimos: Iterable[Emprestimo],
) -> dict[str, int]:
    return reduce(
        lambda contagem, emprestimo: {
            **contagem,
            emprestimo.usuario.identificador: contagem.get(
                emprestimo.usuario.identificador, 0
            )
            + 1,
        },
        emprestimos,
        {},
    )


def quantidade_de_emprestimos_ativos(emprestimos: Iterable[Emprestimo]) -> int:
    return len(emprestimos_ativos(emprestimos))


def quantidade_de_emprestimos_ativos_em_atraso(
    emprestimos: Iterable[Emprestimo], data_referencia: date
) -> int:
    return len(emprestimos_atrasados(emprestimos, data_referencia))


def valor_total_das_multas(
    emprestimos: Iterable[Emprestimo], data_referencia: date
) -> float:
    return relatorio_de_multas(emprestimos, data_referencia).total


def consolidar_estatisticas(
    livros: Iterable[Livro],
    emprestimos: Iterable[Emprestimo],
    data_referencia: date,
) -> Estatisticas:
    livros_fixados = tuple(livros)
    emprestimos_fixados = tuple(emprestimos)
    return Estatisticas(
        data_referencia=data_referencia,
        livros_por_categoria=quantidade_de_livros_por_categoria(livros_fixados),
        emprestimos_por_usuario=quantidade_de_emprestimos_por_usuario(
            emprestimos_fixados
        ),
        emprestimos_ativos=quantidade_de_emprestimos_ativos(emprestimos_fixados),
        emprestimos_ativos_em_atraso=quantidade_de_emprestimos_ativos_em_atraso(
            emprestimos_fixados, data_referencia
        ),
        valor_total_das_multas=valor_total_das_multas(
            emprestimos_fixados, data_referencia
        ),
    )
