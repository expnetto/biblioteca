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


def quantidade_de_livros_por_categoria(livros: tuple[Livro, ...]) -> dict[str, int]:
    return reduce(
        lambda contagem, livro: {
            **contagem,
            livro.categoria: contagem.get(livro.categoria, 0) + 1,
        },
        livros,
        {},
    )


def quantidade_de_emprestimos_por_usuario(
    emprestimos: tuple[Emprestimo, ...],
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


def quantidade_de_emprestimos_ativos(emprestimos: tuple[Emprestimo, ...]) -> int:
    return len(emprestimos_ativos(emprestimos))


def quantidade_de_emprestimos_ativos_em_atraso(
    emprestimos: tuple[Emprestimo, ...], data_referencia: date
) -> int:
    return len(emprestimos_atrasados(emprestimos, data_referencia))


def valor_total_das_multas(
    emprestimos: tuple[Emprestimo, ...], data_referencia: date
) -> float:
    return relatorio_de_multas(emprestimos, data_referencia).total


def consolidar_estatisticas(
    livros: tuple[Livro, ...],
    emprestimos: tuple[Emprestimo, ...],
    data_referencia: date,
) -> Estatisticas:
    return Estatisticas(
        data_referencia=data_referencia,
        livros_por_categoria=quantidade_de_livros_por_categoria(livros),
        emprestimos_por_usuario=quantidade_de_emprestimos_por_usuario(emprestimos),
        emprestimos_ativos=quantidade_de_emprestimos_ativos(emprestimos),
        emprestimos_ativos_em_atraso=quantidade_de_emprestimos_ativos_em_atraso(
            emprestimos, data_referencia
        ),
        valor_total_das_multas=valor_total_das_multas(emprestimos, data_referencia),
    )
