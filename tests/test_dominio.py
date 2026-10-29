from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from biblioteca.dominio import Emprestimo, Livro, Usuario

LIVRO = Livro("L1", "Dom Casmurro", "Machado de Assis", "Literatura Brasileira")
USUARIO = Usuario("U1", "Eraldo Xavier Pimentel Netto", "2023110001")


def emprestimo(data_devolucao=None):
    return Emprestimo(
        identificador="E1",
        livro=LIVRO,
        usuario=USUARIO,
        data_emprestimo=date(2026, 10, 1),
        data_prevista_devolucao=date(2026, 10, 15),
        data_devolucao=data_devolucao,
    )


def test_livro_nao_aceita_alteracao_de_atributo():
    with pytest.raises(FrozenInstanceError):
        LIVRO.titulo = "Outro titulo"


def test_usuario_nao_aceita_alteracao_de_atributo():
    with pytest.raises(FrozenInstanceError):
        USUARIO.nome = "Outro nome"


def test_emprestimo_sem_data_de_devolucao_esta_ativo():
    assert emprestimo().esta_ativo() is True


def test_emprestimo_com_data_de_devolucao_nao_esta_ativo():
    assert emprestimo(date(2026, 10, 10)).esta_ativo() is False


def test_nao_ha_atraso_antes_do_vencimento():
    assert emprestimo().esta_atrasado(date(2026, 10, 14)) is False


def test_nao_ha_atraso_no_dia_exato_do_vencimento():
    assert emprestimo().esta_atrasado(date(2026, 10, 15)) is False


def test_ha_atraso_no_dia_seguinte_ao_vencimento():
    assert emprestimo().esta_atrasado(date(2026, 10, 16)) is True


def test_emprestimo_devolvido_nunca_esta_atrasado():
    devolvido_com_atraso = emprestimo(date(2026, 10, 20))
    assert devolvido_com_atraso.esta_atrasado(date(2026, 10, 30)) is False


def test_dias_de_atraso_conta_do_vencimento_ate_a_referencia():
    assert emprestimo().dias_de_atraso(date(2026, 10, 20)) == 5


def test_dias_de_atraso_e_zero_sem_atraso():
    assert emprestimo().dias_de_atraso(date(2026, 10, 10)) == 0


def test_devolucao_produz_novo_emprestimo_sem_alterar_o_original():
    original = emprestimo()
    devolvido = original.devolvido_em(date(2026, 10, 18))
    assert original.data_devolucao is None
    assert devolvido.data_devolucao == date(2026, 10, 18)
    assert devolvido is not original
    assert devolvido.identificador == original.identificador
