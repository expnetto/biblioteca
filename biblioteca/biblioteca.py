from __future__ import annotations

from datetime import date

from .consultas import esta_disponivel, proximo_identificador
from .dominio import Emprestimo, Livro, Usuario
from .estatisticas import Estatisticas, consolidar_estatisticas
from .multas import RelatorioMultas, relatorio_de_multas


class ErroDeBiblioteca(Exception):
    pass


class IdentificadorDuplicadoError(ErroDeBiblioteca):
    pass


class CadastroInexistenteError(ErroDeBiblioteca):
    pass


class LivroIndisponivelError(ErroDeBiblioteca):
    pass


class EmprestimoInexistenteError(ErroDeBiblioteca):
    pass


class EmprestimoJaDevolvidoError(ErroDeBiblioteca):
    pass


class Biblioteca:
    def __init__(self) -> None:
        self._livros: list[Livro] = []
        self._usuarios: list[Usuario] = []
        self._emprestimos: list[Emprestimo] = []

    def livros(self) -> tuple[Livro, ...]:
        return tuple(self._livros)

    def usuarios(self) -> tuple[Usuario, ...]:
        return tuple(self._usuarios)

    def emprestimos(self) -> tuple[Emprestimo, ...]:
        return tuple(self._emprestimos)

    def buscar_livro(self, identificador: str) -> Livro:
        for livro in self._livros:
            if livro.identificador == identificador:
                return livro
        raise CadastroInexistenteError(f"Livro nao cadastrado: {identificador}")

    def buscar_usuario(self, identificador: str) -> Usuario:
        for usuario in self._usuarios:
            if usuario.identificador == identificador:
                return usuario
        raise CadastroInexistenteError(f"Usuario nao cadastrado: {identificador}")

    def buscar_emprestimo(self, identificador: str) -> Emprestimo:
        for emprestimo in self._emprestimos:
            if emprestimo.identificador == identificador:
                return emprestimo
        raise EmprestimoInexistenteError(
            f"Emprestimo nao encontrado: {identificador}"
        )

    def cadastrar_livro(self, livro: Livro) -> Livro:
        for cadastrado in self._livros:
            if cadastrado.identificador == livro.identificador:
                raise IdentificadorDuplicadoError(
                    f"Livro ja cadastrado: {livro.identificador}"
                )
        self._livros.append(livro)
        return livro

    def cadastrar_usuario(self, usuario: Usuario) -> Usuario:
        for cadastrado in self._usuarios:
            if cadastrado.identificador == usuario.identificador:
                raise IdentificadorDuplicadoError(
                    f"Usuario ja cadastrado: {usuario.identificador}"
                )
            if cadastrado.matricula == usuario.matricula:
                raise IdentificadorDuplicadoError(
                    f"Matricula ja cadastrada: {usuario.matricula}"
                )
        self._usuarios.append(usuario)
        return usuario

    def proximo_identificador_de_livro(self) -> str:
        return proximo_identificador(
            "L", tuple(livro.identificador for livro in self._livros)
        )

    def proximo_identificador_de_usuario(self) -> str:
        return proximo_identificador(
            "U", tuple(usuario.identificador for usuario in self._usuarios)
        )

    def registrar_emprestimo(
        self,
        identificador_livro: str,
        identificador_usuario: str,
        data_emprestimo: date,
        data_prevista_devolucao: date,
    ) -> Emprestimo:
        livro = self.buscar_livro(identificador_livro)
        usuario = self.buscar_usuario(identificador_usuario)
        if not esta_disponivel(livro, self.emprestimos()):
            raise LivroIndisponivelError(
                f"Livro emprestado no momento: {livro.identificador}"
            )
        if data_prevista_devolucao < data_emprestimo:
            raise ErroDeBiblioteca(
                "Data prevista de devolucao anterior a data do emprestimo"
            )
        emprestimo = Emprestimo(
            identificador=proximo_identificador(
                "E", tuple(item.identificador for item in self._emprestimos)
            ),
            livro=livro,
            usuario=usuario,
            data_emprestimo=data_emprestimo,
            data_prevista_devolucao=data_prevista_devolucao,
        )
        self._emprestimos.append(emprestimo)
        return emprestimo

    def registrar_devolucao(
        self, identificador_emprestimo: str, data_devolucao: date
    ) -> Emprestimo:
        emprestimo = self.buscar_emprestimo(identificador_emprestimo)
        if not emprestimo.esta_ativo():
            raise EmprestimoJaDevolvidoError(
                f"Emprestimo ja devolvido: {identificador_emprestimo}"
            )
        devolvido = emprestimo.devolvido_em(data_devolucao)
        self._emprestimos[self._emprestimos.index(emprestimo)] = devolvido
        return devolvido

    def relatorio_de_multas(self, data_referencia: date) -> RelatorioMultas:
        return relatorio_de_multas(self.emprestimos(), data_referencia)

    def estatisticas(self, data_referencia: date) -> Estatisticas:
        return consolidar_estatisticas(
            self.livros(), self.emprestimos(), data_referencia
        )
