from datetime import date, timedelta

from biblioteca.cenarios import cenario_com_atrasos, cenario_em_dia, cenario_misto
from biblioteca.comparacao import (
    total_de_multas_funcional,
    total_de_multas_imperativo,
)
from biblioteca.dominio import Emprestimo, Livro, Usuario

LIVRO = Livro("L1", "Dom Casmurro", "Machado de Assis", "Literatura Brasileira")
USUARIO = Usuario("U1", "Eraldo Xavier Pimentel Netto", "2023110001")
REFERENCIA = date(2026, 10, 28)


def construir(identificador, prevista, devolucao=None):
    return Emprestimo(
        identificador=identificador,
        livro=LIVRO,
        usuario=USUARIO,
        data_emprestimo=date(2026, 10, 1),
        data_prevista_devolucao=prevista,
        data_devolucao=devolucao,
    )


def test_as_duas_versoes_concordam_com_colecao_vazia():
    assert total_de_multas_funcional((), REFERENCIA) == total_de_multas_imperativo(
        (), REFERENCIA
    )


def test_as_duas_versoes_concordam_quando_ninguem_esta_atrasado():
    emprestimos = (construir("E1", date(2026, 11, 10)),)
    assert total_de_multas_funcional(
        emprestimos, REFERENCIA
    ) == total_de_multas_imperativo(emprestimos, REFERENCIA)


def test_as_duas_versoes_concordam_quando_todos_estao_atrasados():
    emprestimos = (
        construir("E1", date(2026, 10, 20)),
        construir("E2", date(2026, 10, 25)),
    )
    assert total_de_multas_funcional(
        emprestimos, REFERENCIA
    ) == total_de_multas_imperativo(emprestimos, REFERENCIA)


def test_as_duas_versoes_concordam_ignorando_devolvidos_com_atraso():
    emprestimos = (
        construir("E1", date(2026, 10, 20)),
        construir("E2", date(2026, 10, 10), date(2026, 10, 24)),
    )
    assert total_de_multas_funcional(emprestimos, REFERENCIA) == 16.00
    assert total_de_multas_imperativo(emprestimos, REFERENCIA) == 16.00


def test_as_duas_versoes_concordam_em_todos_os_cenarios():
    for fabrica in (cenario_com_atrasos, cenario_em_dia, cenario_misto):
        biblioteca = fabrica(REFERENCIA)
        for deslocamento in (-10, 0, 7, 30):
            data = REFERENCIA + timedelta(days=deslocamento)
            emprestimos = biblioteca.emprestimos()
            assert total_de_multas_funcional(
                emprestimos, data
            ) == total_de_multas_imperativo(emprestimos, data)


def test_a_versao_funcional_concorda_com_o_total_do_relatorio():
    biblioteca = cenario_misto(REFERENCIA)
    emprestimos = biblioteca.emprestimos()
    assert total_de_multas_funcional(emprestimos, REFERENCIA) == (
        biblioteca.relatorio_de_multas(REFERENCIA).total
    )
