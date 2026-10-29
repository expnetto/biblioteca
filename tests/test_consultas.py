from datetime import date

from biblioteca.consultas import (
    emprestimos_ativos,
    esta_disponivel,
    filtrar_livros_por_categoria,
    livros_disponiveis,
    proximo_identificador,
)
from biblioteca.dominio import Emprestimo, Livro, Usuario

LIVRO_A = Livro("L1", "Dom Casmurro", "Machado de Assis", "Literatura Brasileira")
LIVRO_B = Livro("L2", "Codigo Limpo", "Robert C. Martin", "Computacao")
LIVRO_C = Livro("L3", "Estruturas de Dados", "Niklaus Wirth", "Computacao")
USUARIO = Usuario("U1", "Eraldo Xavier Pimentel Netto", "2023110001")
ACERVO = (LIVRO_A, LIVRO_B, LIVRO_C)


def construir(identificador, livro, devolucao=None):
    return Emprestimo(
        identificador=identificador,
        livro=livro,
        usuario=USUARIO,
        data_emprestimo=date(2026, 10, 1),
        data_prevista_devolucao=date(2026, 10, 15),
        data_devolucao=devolucao,
    )


def test_filtragem_por_categoria_retorna_apenas_a_categoria_pedida():
    assert filtrar_livros_por_categoria(ACERVO, "Computacao") == (LIVRO_B, LIVRO_C)


def test_filtragem_por_categoria_inexistente_retorna_vazio():
    assert filtrar_livros_por_categoria(ACERVO, "Matematica") == ()


def test_filtragem_por_categoria_nao_altera_a_colecao_original():
    livros = [LIVRO_A, LIVRO_B, LIVRO_C]
    copia = list(livros)
    filtrar_livros_por_categoria(livros, "Computacao")
    assert livros == copia


def test_emprestimos_ativos_ignora_devolvidos():
    ativo = construir("E1", LIVRO_A)
    devolvido = construir("E2", LIVRO_B, date(2026, 10, 12))
    assert emprestimos_ativos((ativo, devolvido)) == (ativo,)


def test_livro_sem_emprestimo_esta_disponivel():
    assert esta_disponivel(LIVRO_A, ()) is True


def test_livro_com_emprestimo_ativo_nao_esta_disponivel():
    assert esta_disponivel(LIVRO_A, (construir("E1", LIVRO_A),)) is False


def test_livro_devolvido_volta_a_estar_disponivel():
    devolvido = construir("E1", LIVRO_A, date(2026, 10, 12))
    assert esta_disponivel(LIVRO_A, (devolvido,)) is True


def test_livros_disponiveis_exclui_os_emprestados():
    emprestimos = (construir("E1", LIVRO_B),)
    assert livros_disponiveis(ACERVO, emprestimos) == (LIVRO_A, LIVRO_C)


def test_proximo_identificador_comeca_em_um():
    assert proximo_identificador("L", 0) == "L1"


def test_proximo_identificador_segue_a_quantidade_cadastrada():
    assert proximo_identificador("L", 6) == "L7"


def test_proximo_identificador_respeita_o_prefixo():
    assert proximo_identificador("E", 2) == "E3"
