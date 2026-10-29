from datetime import date, datetime, timedelta

from .biblioteca import Biblioteca, ErroDeBiblioteca
from .cenarios import CENARIOS
from .comparacao import total_de_multas_funcional, total_de_multas_imperativo
from .consultas import (
    emprestimos_ativos,
    esta_disponivel,
    filtrar_livros_por_categoria,
    livros_disponiveis,
)
from .dominio import Emprestimo, Livro, Usuario
from .multas import VALOR_MULTA_DIARIA, emprestimos_atrasados

PRAZO_PADRAO_EM_DIAS = 14


def formatar_reais(valor: float) -> str:
    return f"R$ {valor:.2f}".replace(".", ",")


def formatar_data(valor: date) -> str:
    return valor.strftime("%d/%m/%Y")


def imprimir_titulo(texto: str) -> None:
    print()
    print(texto)
    print("-" * len(texto))


def ler_texto(rotulo: str) -> str:
    valor = input(f"{rotulo}: ").strip()
    while valor == "":
        print("Valor obrigatorio.")
        valor = input(f"{rotulo}: ").strip()
    return valor


def converter_data(entrada: str) -> date | None:
    try:
        return datetime.strptime(entrada, "%d/%m/%Y").date()
    except ValueError:
        return None


def ler_data(rotulo: str, sugestao: date) -> date:
    rotulo_completo = f"{rotulo} [dd/mm/aaaa, vazio = {formatar_data(sugestao)}]"
    while True:
        entrada = input(f"{rotulo_completo}: ").strip()
        if entrada == "":
            return sugestao
        convertida = converter_data(entrada)
        if convertida is not None:
            return convertida
        print("Data invalida. Use o formato dd/mm/aaaa.")


def exibir_livros(biblioteca: Biblioteca, livros: tuple[Livro, ...]) -> None:
    if len(livros) == 0:
        print("Nenhum livro.")
        return
    todos_os_emprestimos = biblioteca.emprestimos()
    for livro in livros:
        situacao = (
            "disponivel"
            if esta_disponivel(livro, todos_os_emprestimos)
            else "emprestado"
        )
        print(
            f"{livro.identificador} | {livro.titulo} | {livro.autor} "
            f"| {livro.categoria} | {situacao}"
        )


def exibir_usuarios(biblioteca: Biblioteca) -> None:
    usuarios = biblioteca.usuarios()
    if len(usuarios) == 0:
        print("Nenhum usuario.")
        return
    for usuario in usuarios:
        print(f"{usuario.identificador} | {usuario.nome} | {usuario.matricula}")


def exibir_emprestimos(emprestimos: tuple[Emprestimo, ...]) -> None:
    if len(emprestimos) == 0:
        print("Nenhum emprestimo.")
        return
    for emprestimo in emprestimos:
        devolucao = (
            formatar_data(emprestimo.data_devolucao)
            if emprestimo.data_devolucao is not None
            else "em aberto"
        )
        print(
            f"{emprestimo.identificador} | {emprestimo.livro.titulo} "
            f"| {emprestimo.usuario.nome} | saida {formatar_data(emprestimo.data_emprestimo)} "
            f"| prevista {formatar_data(emprestimo.data_prevista_devolucao)} "
            f"| devolucao {devolucao}"
        )


def cadastrar_livro(biblioteca: Biblioteca) -> None:
    imprimir_titulo("Cadastrar livro")
    identificador = biblioteca.proximo_identificador_de_livro()
    livro = Livro(
        identificador=identificador,
        titulo=ler_texto("Titulo"),
        autor=ler_texto("Autor"),
        categoria=ler_texto("Categoria"),
    )
    biblioteca.cadastrar_livro(livro)
    print(f"Livro {identificador} cadastrado.")


def cadastrar_usuario(biblioteca: Biblioteca) -> None:
    imprimir_titulo("Cadastrar usuario")
    identificador = biblioteca.proximo_identificador_de_usuario()
    usuario = Usuario(
        identificador=identificador,
        nome=ler_texto("Nome"),
        matricula=ler_texto("Matricula"),
    )
    biblioteca.cadastrar_usuario(usuario)
    print(f"Usuario {identificador} cadastrado.")


def listar_livros(biblioteca: Biblioteca) -> None:
    imprimir_titulo("Livros")
    print("1 - Todos")
    print("2 - Somente disponiveis")
    print("3 - Por categoria")
    escolha = input("Opcao: ").strip()
    if escolha == "2":
        exibir_livros(
            biblioteca, livros_disponiveis(biblioteca.livros(), biblioteca.emprestimos())
        )
    elif escolha == "3":
        categoria = ler_texto("Categoria")
        exibir_livros(
            biblioteca, filtrar_livros_por_categoria(biblioteca.livros(), categoria)
        )
    else:
        exibir_livros(biblioteca, biblioteca.livros())


def registrar_emprestimo(biblioteca: Biblioteca, hoje: date) -> None:
    imprimir_titulo("Registrar emprestimo")
    exibir_livros(
        biblioteca, livros_disponiveis(biblioteca.livros(), biblioteca.emprestimos())
    )
    exibir_usuarios(biblioteca)
    identificador_livro = ler_texto("Identificador do livro")
    identificador_usuario = ler_texto("Identificador do usuario")
    data_emprestimo = ler_data("Data do emprestimo", hoje)
    data_prevista = ler_data(
        "Data prevista de devolucao",
        data_emprestimo + timedelta(days=PRAZO_PADRAO_EM_DIAS),
    )
    emprestimo = biblioteca.registrar_emprestimo(
        identificador_livro, identificador_usuario, data_emprestimo, data_prevista
    )
    print(f"Emprestimo {emprestimo.identificador} registrado.")


def registrar_devolucao(biblioteca: Biblioteca, hoje: date) -> None:
    imprimir_titulo("Registrar devolucao")
    exibir_emprestimos(emprestimos_ativos(biblioteca.emprestimos()))
    identificador = ler_texto("Identificador do emprestimo")
    data_devolucao = ler_data("Data da devolucao", hoje)
    devolvido = biblioteca.registrar_devolucao(identificador, data_devolucao)
    print(
        f"Emprestimo {devolvido.identificador} devolvido em "
        f"{formatar_data(devolvido.data_devolucao)}. "
        f"Livro {devolvido.livro.identificador} disponivel novamente."
    )


def listar_emprestimos(biblioteca: Biblioteca, hoje: date) -> None:
    imprimir_titulo("Emprestimos")
    print("1 - Todos")
    print("2 - Somente ativos")
    print("3 - Ativos em atraso numa data")
    escolha = input("Opcao: ").strip()
    if escolha == "2":
        exibir_emprestimos(emprestimos_ativos(biblioteca.emprestimos()))
    elif escolha == "3":
        data_referencia = ler_data("Data de referencia", hoje)
        exibir_emprestimos(
            emprestimos_atrasados(biblioteca.emprestimos(), data_referencia)
        )
    else:
        exibir_emprestimos(biblioteca.emprestimos())


def exibir_relatorio_de_multas(biblioteca: Biblioteca, hoje: date) -> None:
    imprimir_titulo("Relatorio de multas")
    data_referencia = ler_data("Data de referencia", hoje)
    relatorio = biblioteca.relatorio_de_multas(data_referencia)
    print(f"Data de referencia: {formatar_data(relatorio.data_referencia)}")
    print(f"Multa diaria: {formatar_reais(VALOR_MULTA_DIARIA)}")
    if len(relatorio.itens) == 0:
        print("Nenhum emprestimo ativo em atraso.")
    for item in relatorio.itens:
        print(
            f"{item.emprestimo.identificador} | {item.emprestimo.usuario.nome} "
            f"| {item.emprestimo.livro.titulo} | {item.dias_de_atraso} dia(s) "
            f"| {formatar_reais(item.valor)}"
        )
    print(f"Total: {formatar_reais(relatorio.total)}")


def exibir_estatisticas(biblioteca: Biblioteca, hoje: date) -> None:
    imprimir_titulo("Estatisticas")
    data_referencia = ler_data("Data de referencia", hoje)
    estatisticas = biblioteca.estatisticas(data_referencia)
    print("Livros por categoria:")
    for categoria, quantidade in estatisticas.livros_por_categoria.items():
        print(f"  {categoria}: {quantidade}")
    print("Emprestimos por usuario:")
    for identificador, quantidade in estatisticas.emprestimos_por_usuario.items():
        print(f"  {biblioteca.buscar_usuario(identificador).nome}: {quantidade}")
    print(f"Emprestimos ativos: {estatisticas.emprestimos_ativos}")
    print(f"Emprestimos ativos em atraso: {estatisticas.emprestimos_ativos_em_atraso}")
    print(
        f"Valor total das multas: {formatar_reais(estatisticas.valor_total_das_multas)}"
    )


def exibir_comparacao(biblioteca: Biblioteca, hoje: date) -> None:
    imprimir_titulo("Comparacao entre paradigmas")
    data_referencia = ler_data("Data de referencia", hoje)
    emprestimos = biblioteca.emprestimos()
    funcional = total_de_multas_funcional(emprestimos, data_referencia)
    imperativo = total_de_multas_imperativo(emprestimos, data_referencia)
    print(f"Versao funcional (filter, map, reduce): {formatar_reais(funcional)}")
    print(f"Versao imperativa (laco e acumulador): {formatar_reais(imperativo)}")
    print(f"Resultados equivalentes: {funcional == imperativo}")


def escolher_cenario(hoje: date) -> Biblioteca:
    imprimir_titulo("Escolha o cenario")
    for posicao, (nome, _) in enumerate(CENARIOS, start=1):
        print(f"{posicao} - {nome}")
    escolha = input("Opcao: ").strip()
    for posicao, (nome, fabrica) in enumerate(CENARIOS, start=1):
        if escolha == str(posicao):
            print(f"Cenario carregado: {nome}")
            return fabrica(hoje)
    print("Opcao invalida. Carregando o cenario com atrasos.")
    return CENARIOS[0][1](hoje)


MENU = """
1 - Cadastrar livro
2 - Cadastrar usuario
3 - Listar livros
4 - Listar usuarios
5 - Registrar emprestimo
6 - Registrar devolucao
7 - Listar emprestimos
8 - Relatorio de multas
9 - Estatisticas
10 - Comparacao imperativa x funcional
11 - Trocar de cenario
0 - Sair
"""


def executar() -> None:
    hoje = date.today()
    print("Sistema de Gerenciamento de Biblioteca")
    print(f"Data de hoje: {formatar_data(hoje)}")
    biblioteca = escolher_cenario(hoje)
    while True:
        print(MENU)
        escolha = input("Opcao: ").strip()
        try:
            if escolha == "0":
                print("Encerrando.")
                return
            elif escolha == "1":
                cadastrar_livro(biblioteca)
            elif escolha == "2":
                cadastrar_usuario(biblioteca)
            elif escolha == "3":
                listar_livros(biblioteca)
            elif escolha == "4":
                imprimir_titulo("Usuarios")
                exibir_usuarios(biblioteca)
            elif escolha == "5":
                registrar_emprestimo(biblioteca, hoje)
            elif escolha == "6":
                registrar_devolucao(biblioteca, hoje)
            elif escolha == "7":
                listar_emprestimos(biblioteca, hoje)
            elif escolha == "8":
                exibir_relatorio_de_multas(biblioteca, hoje)
            elif escolha == "9":
                exibir_estatisticas(biblioteca, hoje)
            elif escolha == "10":
                exibir_comparacao(biblioteca, hoje)
            elif escolha == "11":
                biblioteca = escolher_cenario(hoje)
            else:
                print("Opcao invalida.")
        except ErroDeBiblioteca as erro:
            print(f"Operacao recusada: {erro}")
        except (EOFError, KeyboardInterrupt):
            print()
            print("Encerrando.")
            return
