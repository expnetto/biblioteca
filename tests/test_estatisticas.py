from datetime import date

from biblioteca.dominio import Emprestimo, Livro, Usuario
from biblioteca.estatisticas import (
    consolidar_estatisticas,
    quantidade_de_emprestimos_ativos,
    quantidade_de_emprestimos_ativos_em_atraso,
    quantidade_de_emprestimos_por_usuario,
    quantidade_de_livros_por_categoria,
    valor_total_das_multas,
)

LIVRO_A = Livro("L1", "Dom Casmurro", "Machado de Assis", "Literatura Brasileira")
LIVRO_B = Livro("L2", "Codigo Limpo", "Robert C. Martin", "Computacao")
LIVRO_C = Livro("L3", "Estruturas de Dados", "Niklaus Wirth", "Computacao")
USUARIO_A = Usuario("U1", "Eraldo Xavier Pimentel Netto", "2023110001")
USUARIO_B = Usuario("U2", "Mariana Alves de Souza", "2023110002")
HOMONIMO = Usuario("U3", "Mariana Alves de Souza", "2023110003")
REFERENCIA = date(2026, 10, 28)
ACERVO = (LIVRO_A, LIVRO_B, LIVRO_C)


def construir(identificador, livro, usuario, prevista, devolucao=None):
    return Emprestimo(
        identificador=identificador,
        livro=livro,
        usuario=usuario,
        data_emprestimo=date(2026, 10, 1),
        data_prevista_devolucao=prevista,
        data_devolucao=devolucao,
    )


ATRASADO = construir("E1", LIVRO_A, USUARIO_A, date(2026, 10, 23))
EM_DIA = construir("E2", LIVRO_B, USUARIO_A, date(2026, 11, 10))
DEVOLVIDO = construir("E3", LIVRO_C, USUARIO_B, date(2026, 10, 10), date(2026, 10, 20))
TODOS = (ATRASADO, EM_DIA, DEVOLVIDO)


def test_livros_por_categoria_conta_cada_categoria():
    assert quantidade_de_livros_por_categoria(ACERVO) == {
        "Literatura Brasileira": 1,
        "Computacao": 2,
    }


def test_livros_por_categoria_de_acervo_vazio_e_dicionario_vazio():
    assert quantidade_de_livros_por_categoria(()) == {}


def test_livros_por_categoria_nao_altera_a_colecao_recebida():
    livros = [LIVRO_A, LIVRO_B, LIVRO_C]
    copia = list(livros)
    quantidade_de_livros_por_categoria(livros)
    assert livros == copia


def test_emprestimos_por_usuario_conta_por_identificador():
    assert quantidade_de_emprestimos_por_usuario(TODOS) == {"U1": 2, "U2": 1}


def test_emprestimos_por_usuario_separa_usuarios_homonimos():
    emprestimos = (
        construir("E1", LIVRO_A, USUARIO_B, date(2026, 10, 23)),
        construir("E2", LIVRO_B, HOMONIMO, date(2026, 10, 23)),
    )
    assert quantidade_de_emprestimos_por_usuario(emprestimos) == {"U2": 1, "U3": 1}


def test_quantidade_de_ativos_ignora_devolvidos():
    assert quantidade_de_emprestimos_ativos(TODOS) == 2


def test_quantidade_de_ativos_em_atraso():
    assert quantidade_de_emprestimos_ativos_em_atraso(TODOS, REFERENCIA) == 1


def test_valor_total_das_multas_considera_apenas_ativos_atrasados():
    assert valor_total_das_multas(TODOS, REFERENCIA) == 10.00


def test_consolidado_reune_as_cinco_estatisticas():
    estatisticas = consolidar_estatisticas(ACERVO, TODOS, REFERENCIA)
    assert estatisticas.data_referencia == REFERENCIA
    assert estatisticas.livros_por_categoria == {
        "Literatura Brasileira": 1,
        "Computacao": 2,
    }
    assert estatisticas.emprestimos_por_usuario == {"U1": 2, "U2": 1}
    assert estatisticas.emprestimos_ativos == 2
    assert estatisticas.emprestimos_ativos_em_atraso == 1
    assert estatisticas.valor_total_das_multas == 10.00
