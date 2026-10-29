from datetime import date

import pytest

from biblioteca.biblioteca import (
    Biblioteca,
    CadastroInexistenteError,
    EmprestimoInexistenteError,
    EmprestimoJaDevolvidoError,
    IdentificadorDuplicadoError,
    LivroIndisponivelError,
)
from biblioteca.consultas import esta_disponivel
from biblioteca.dominio import Livro, Usuario

LIVRO_A = Livro("L1", "Dom Casmurro", "Machado de Assis", "Literatura Brasileira")
LIVRO_B = Livro("L2", "Codigo Limpo", "Robert C. Martin", "Computacao")
USUARIO_A = Usuario("U1", "Eraldo Xavier Pimentel Netto", "2023110001")
USUARIO_B = Usuario("U2", "Mariana Alves de Souza", "2023110002")
SAIDA = date(2026, 10, 1)
PREVISTA = date(2026, 10, 15)


def biblioteca_com_cadastros():
    biblioteca = Biblioteca()
    biblioteca.cadastrar_livro(LIVRO_A)
    biblioteca.cadastrar_livro(LIVRO_B)
    biblioteca.cadastrar_usuario(USUARIO_A)
    biblioteca.cadastrar_usuario(USUARIO_B)
    return biblioteca


def test_biblioteca_nova_esta_vazia():
    biblioteca = Biblioteca()
    assert biblioteca.livros() == ()
    assert biblioteca.usuarios() == ()
    assert biblioteca.emprestimos() == ()


def test_consulta_devolve_tupla_que_nao_reflete_mudancas_posteriores():
    biblioteca = biblioteca_com_cadastros()
    livros = biblioteca.livros()
    biblioteca.cadastrar_livro(
        Livro("L3", "Estruturas de Dados", "Niklaus Wirth", "Computacao")
    )
    assert len(livros) == 2
    assert len(biblioteca.livros()) == 3


def test_cadastro_de_livro_duplicado_e_recusado():
    biblioteca = biblioteca_com_cadastros()
    with pytest.raises(IdentificadorDuplicadoError):
        biblioteca.cadastrar_livro(LIVRO_A)


def test_cadastro_de_usuario_duplicado_e_recusado():
    biblioteca = biblioteca_com_cadastros()
    with pytest.raises(IdentificadorDuplicadoError):
        biblioteca.cadastrar_usuario(USUARIO_A)


def test_matricula_repetida_e_recusada():
    biblioteca = biblioteca_com_cadastros()
    with pytest.raises(IdentificadorDuplicadoError):
        biblioteca.cadastrar_usuario(Usuario("U9", "Outro Nome", "2023110001"))


def test_emprestimo_de_livro_nao_cadastrado_e_recusado():
    biblioteca = biblioteca_com_cadastros()
    with pytest.raises(CadastroInexistenteError):
        biblioteca.registrar_emprestimo("L99", "U1", SAIDA, PREVISTA)


def test_emprestimo_para_usuario_nao_cadastrado_e_recusado():
    biblioteca = biblioteca_com_cadastros()
    with pytest.raises(CadastroInexistenteError):
        biblioteca.registrar_emprestimo("L1", "U99", SAIDA, PREVISTA)


def test_emprestimo_registrado_recebe_identificador_sequencial():
    biblioteca = biblioteca_com_cadastros()
    primeiro = biblioteca.registrar_emprestimo("L1", "U1", SAIDA, PREVISTA)
    segundo = biblioteca.registrar_emprestimo("L2", "U2", SAIDA, PREVISTA)
    assert primeiro.identificador == "E1"
    assert segundo.identificador == "E2"


def test_livro_emprestado_fica_indisponivel():
    biblioteca = biblioteca_com_cadastros()
    biblioteca.registrar_emprestimo("L1", "U1", SAIDA, PREVISTA)
    assert esta_disponivel(LIVRO_A, biblioteca.emprestimos()) is False


def test_mesmo_livro_nao_pode_ser_emprestado_duas_vezes():
    biblioteca = biblioteca_com_cadastros()
    biblioteca.registrar_emprestimo("L1", "U1", SAIDA, PREVISTA)
    with pytest.raises(LivroIndisponivelError):
        biblioteca.registrar_emprestimo("L1", "U2", SAIDA, PREVISTA)


def test_livro_pode_ser_emprestado_novamente_depois_da_devolucao():
    biblioteca = biblioteca_com_cadastros()
    emprestimo = biblioteca.registrar_emprestimo("L1", "U1", SAIDA, PREVISTA)
    biblioteca.registrar_devolucao(emprestimo.identificador, date(2026, 10, 12))
    novo = biblioteca.registrar_emprestimo("L1", "U2", date(2026, 10, 13), PREVISTA)
    assert novo.identificador == "E2"
    assert esta_disponivel(LIVRO_A, biblioteca.emprestimos()) is False


def test_devolucao_registra_a_data_e_mantem_o_emprestimo_no_historico():
    biblioteca = biblioteca_com_cadastros()
    emprestimo = biblioteca.registrar_emprestimo("L1", "U1", SAIDA, PREVISTA)
    devolvido = biblioteca.registrar_devolucao(
        emprestimo.identificador, date(2026, 10, 12)
    )
    assert devolvido.data_devolucao == date(2026, 10, 12)
    assert emprestimo.data_devolucao is None
    assert len(biblioteca.emprestimos()) == 1
    assert biblioteca.emprestimos()[0].data_devolucao == date(2026, 10, 12)


def test_devolucao_de_emprestimo_inexistente_e_recusada():
    biblioteca = biblioteca_com_cadastros()
    with pytest.raises(EmprestimoInexistenteError):
        biblioteca.registrar_devolucao("E99", date(2026, 10, 12))


def test_devolucao_repetida_e_recusada():
    biblioteca = biblioteca_com_cadastros()
    emprestimo = biblioteca.registrar_emprestimo("L1", "U1", SAIDA, PREVISTA)
    biblioteca.registrar_devolucao(emprestimo.identificador, date(2026, 10, 12))
    with pytest.raises(EmprestimoJaDevolvidoError):
        biblioteca.registrar_devolucao(emprestimo.identificador, date(2026, 10, 13))


def test_biblioteca_disponibiliza_o_relatorio_de_multas():
    biblioteca = biblioteca_com_cadastros()
    biblioteca.registrar_emprestimo("L1", "U1", SAIDA, PREVISTA)
    relatorio = biblioteca.relatorio_de_multas(date(2026, 10, 20))
    assert len(relatorio.itens) == 1
    assert relatorio.total == 10.00


def test_biblioteca_disponibiliza_as_estatisticas():
    biblioteca = biblioteca_com_cadastros()
    biblioteca.registrar_emprestimo("L1", "U1", SAIDA, PREVISTA)
    estatisticas = biblioteca.estatisticas(date(2026, 10, 20))
    assert estatisticas.emprestimos_ativos == 1
    assert estatisticas.emprestimos_ativos_em_atraso == 1
    assert estatisticas.valor_total_das_multas == 10.00
    assert estatisticas.livros_por_categoria == {
        "Literatura Brasileira": 1,
        "Computacao": 1,
    }
