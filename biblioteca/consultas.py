from .dominio import Emprestimo, Livro


def filtrar_livros_por_categoria(
    livros: tuple[Livro, ...], categoria: str
) -> tuple[Livro, ...]:
    return tuple(filter(lambda livro: livro.categoria == categoria, livros))


def emprestimos_ativos(
    emprestimos: tuple[Emprestimo, ...],
) -> tuple[Emprestimo, ...]:
    return tuple(filter(lambda emprestimo: emprestimo.esta_ativo(), emprestimos))


def esta_disponivel(livro: Livro, emprestimos: tuple[Emprestimo, ...]) -> bool:
    emprestimos_do_livro = filter(
        lambda emprestimo: emprestimo.livro.identificador == livro.identificador,
        emprestimos_ativos(emprestimos),
    )
    return len(tuple(emprestimos_do_livro)) == 0


def livros_disponiveis(
    livros: tuple[Livro, ...], emprestimos: tuple[Emprestimo, ...]
) -> tuple[Livro, ...]:
    return tuple(filter(lambda livro: esta_disponivel(livro, emprestimos), livros))


def proximo_identificador(prefixo: str, quantidade_cadastrada: int) -> str:
    return f"{prefixo}{quantidade_cadastrada + 1}"
