from dataclasses import dataclass
from datetime import date
from functools import reduce

from .dominio import Emprestimo

VALOR_MULTA_DIARIA = 2.00


@dataclass(frozen=True)
class ItemMulta:
    emprestimo: Emprestimo
    dias_de_atraso: int
    valor: float


@dataclass(frozen=True)
class RelatorioMultas:
    data_referencia: date
    itens: tuple[ItemMulta, ...]
    total: float


def calcular_multa(dias_atraso: int, valor_diario: float) -> float:
    if dias_atraso <= 0:
        return 0.0
    return dias_atraso * valor_diario


def emprestimos_atrasados(
    emprestimos: tuple[Emprestimo, ...], data_referencia: date
) -> tuple[Emprestimo, ...]:
    return tuple(
        filter(
            lambda emprestimo: emprestimo.esta_atrasado(data_referencia), emprestimos
        )
    )


def multa_do_emprestimo(
    emprestimo: Emprestimo,
    data_referencia: date,
    valor_diario: float = VALOR_MULTA_DIARIA,
) -> ItemMulta:
    dias = emprestimo.dias_de_atraso(data_referencia)
    return ItemMulta(
        emprestimo=emprestimo,
        dias_de_atraso=dias,
        valor=calcular_multa(dias, valor_diario),
    )


def relatorio_de_multas(
    emprestimos: tuple[Emprestimo, ...],
    data_referencia: date,
    valor_diario: float = VALOR_MULTA_DIARIA,
) -> RelatorioMultas:
    atrasados = emprestimos_atrasados(emprestimos, data_referencia)
    itens = tuple(
        map(
            lambda emprestimo: multa_do_emprestimo(
                emprestimo, data_referencia, valor_diario
            ),
            atrasados,
        )
    )
    total = reduce(lambda acumulado, item: acumulado + item.valor, itens, 0.0)
    return RelatorioMultas(data_referencia=data_referencia, itens=itens, total=total)
