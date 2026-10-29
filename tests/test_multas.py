from datetime import date

from biblioteca.dominio import Emprestimo, Livro, Usuario
from biblioteca.multas import (
    VALOR_MULTA_DIARIA,
    calcular_multa,
    emprestimos_atrasados,
    multa_do_emprestimo,
    relatorio_de_multas,
)

LIVRO_A = Livro("L1", "Dom Casmurro", "Machado de Assis", "Literatura Brasileira")
LIVRO_B = Livro("L2", "Codigo Limpo", "Robert C. Martin", "Computacao")
USUARIO_A = Usuario("U1", "Eraldo Xavier Pimentel Netto", "2023110001")
USUARIO_B = Usuario("U2", "Mariana Alves de Souza", "2023110002")
REFERENCIA = date(2026, 10, 28)


def construir(identificador, livro, usuario, prevista, devolucao=None):
    return Emprestimo(
        identificador=identificador,
        livro=livro,
        usuario=usuario,
        data_emprestimo=date(2026, 10, 1),
        data_prevista_devolucao=prevista,
        data_devolucao=devolucao,
    )


ATRASADO_CINCO_DIAS = construir("E1", LIVRO_A, USUARIO_A, date(2026, 10, 23))
EM_DIA = construir("E2", LIVRO_B, USUARIO_B, date(2026, 11, 10))
DEVOLVIDO_COM_ATRASO = construir(
    "E3", LIVRO_B, USUARIO_A, date(2026, 10, 10), date(2026, 10, 20)
)


def test_valor_da_multa_diaria_e_dois_reais():
    assert VALOR_MULTA_DIARIA == 2.00


def test_multa_de_zero_dias_e_zero():
    assert calcular_multa(0, 2.00) == 0.0


def test_multa_de_dias_negativos_e_zero():
    assert calcular_multa(-3, 2.00) == 0.0


def test_multa_de_um_dia():
    assert calcular_multa(1, 2.00) == 2.00


def test_multa_de_sete_dias():
    assert calcular_multa(7, 2.00) == 14.00


def test_multa_respeita_o_valor_diario_recebido():
    assert calcular_multa(3, 5.00) == 15.00


def test_multa_tem_transparencia_referencial():
    assert calcular_multa(4, 2.00) == calcular_multa(4, 2.00)


def test_atrasados_seleciona_apenas_ativos_vencidos():
    emprestimos = (ATRASADO_CINCO_DIAS, EM_DIA, DEVOLVIDO_COM_ATRASO)
    assert emprestimos_atrasados(emprestimos, REFERENCIA) == (ATRASADO_CINCO_DIAS,)


def test_atrasados_nao_altera_a_colecao_recebida():
    emprestimos = [ATRASADO_CINCO_DIAS, EM_DIA, DEVOLVIDO_COM_ATRASO]
    copia = list(emprestimos)
    emprestimos_atrasados(emprestimos, REFERENCIA)
    assert emprestimos == copia


def test_item_de_multa_calcula_dias_e_valor():
    item = multa_do_emprestimo(ATRASADO_CINCO_DIAS, REFERENCIA)
    assert item.dias_de_atraso == 5
    assert item.valor == 10.00


def test_relatorio_vazio_quando_nao_ha_emprestimos():
    relatorio = relatorio_de_multas((), REFERENCIA)
    assert relatorio.itens == ()
    assert relatorio.total == 0.0


def test_relatorio_ignora_em_dia_e_devolvidos():
    relatorio = relatorio_de_multas(
        (ATRASADO_CINCO_DIAS, EM_DIA, DEVOLVIDO_COM_ATRASO), REFERENCIA
    )
    assert len(relatorio.itens) == 1
    assert relatorio.itens[0].emprestimo.identificador == "E1"
    assert relatorio.total == 10.00


def test_total_do_relatorio_soma_os_itens():
    outro_atrasado = construir("E4", LIVRO_A, USUARIO_B, date(2026, 10, 25))
    relatorio = relatorio_de_multas((ATRASADO_CINCO_DIAS, outro_atrasado), REFERENCIA)
    assert relatorio.total == 16.00


def test_relatorio_guarda_a_data_de_referencia_recebida():
    assert relatorio_de_multas((), REFERENCIA).data_referencia == REFERENCIA


def test_relatorio_muda_com_a_data_de_referencia_sem_alterar_os_dados():
    emprestimos = (ATRASADO_CINCO_DIAS,)
    antes = relatorio_de_multas(emprestimos, date(2026, 10, 24)).total
    depois = relatorio_de_multas(emprestimos, date(2026, 10, 28)).total
    assert antes == 2.00
    assert depois == 10.00
    assert emprestimos[0].data_devolucao is None
