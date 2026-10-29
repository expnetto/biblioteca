from __future__ import annotations

from collections.abc import Iterable

from .dominio import Emprestimo, Livro


def filtrar_livros_por_categoria(
    livros: Iterable[Livro], categoria: str
) -> tuple[Livro, ...]:
    return tuple(filter(lambda livro: livro.categoria == categoria, livros))


def emprestimos_ativos(emprestimos: Iterable[Emprestimo]) -> tuple[Emprestimo, ...]:
    return tuple(filter(lambda emprestimo: emprestimo.esta_ativo(), emprestimos))


def emprestimos_ativos_do_livro(
    livro: Livro, emprestimos: Iterable[Emprestimo]
) -> tuple[Emprestimo, ...]:
    return tuple(
        filter(
            lambda emprestimo: emprestimo.livro.identificador == livro.identificador,
            emprestimos_ativos(emprestimos),
        )
    )


def esta_disponivel(livro: Livro, emprestimos: Iterable[Emprestimo]) -> bool:
    return len(emprestimos_ativos_do_livro(livro, emprestimos)) == 0


def livros_disponiveis(
    livros: Iterable[Livro], emprestimos: Iterable[Emprestimo]
) -> tuple[Livro, ...]:
    emprestimos_fixados = tuple(emprestimos)
    return tuple(
        filter(lambda livro: esta_disponivel(livro, emprestimos_fixados), livros)
    )


def proximo_identificador(prefixo: str, identificadores: Iterable[str]) -> str:
    sufixos = filter(
        lambda identificador: identificador.startswith(prefixo)
        and identificador[len(prefixo) :].isdigit(),
        identificadores,
    )
    numeros = tuple(
        map(lambda identificador: int(identificador[len(prefixo) :]), sufixos)
    )
    return f"{prefixo}{max(numeros, default=0) + 1}"
