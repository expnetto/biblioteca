from __future__ import annotations

from collections.abc import Iterable
from datetime import date
from functools import reduce

from .dominio import Emprestimo
from .multas import VALOR_MULTA_DIARIA, calcular_multa, emprestimos_atrasados


def total_de_multas_funcional(
    emprestimos: Iterable[Emprestimo],
    data_referencia: date,
    valor_diario: float = VALOR_MULTA_DIARIA,
) -> float:
    atrasados = emprestimos_atrasados(emprestimos, data_referencia)
    valores = map(
        lambda emprestimo: calcular_multa(
            emprestimo.dias_de_atraso(data_referencia), valor_diario
        ),
        atrasados,
    )
    return reduce(lambda acumulado, valor: acumulado + valor, valores, 0.0)


def total_de_multas_imperativo(
    emprestimos: Iterable[Emprestimo],
    data_referencia: date,
    valor_diario: float = VALOR_MULTA_DIARIA,
) -> float:
    total = 0.0
    for emprestimo in emprestimos:
        if emprestimo.data_devolucao is None:
            if emprestimo.data_prevista_devolucao < data_referencia:
                dias = (data_referencia - emprestimo.data_prevista_devolucao).days
                total = total + dias * valor_diario
    return total
