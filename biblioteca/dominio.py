from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Livro:
    identificador: str
    titulo: str
    autor: str
    categoria: str


@dataclass(frozen=True)
class Usuario:
    identificador: str
    nome: str
    matricula: str


@dataclass(frozen=True)
class Emprestimo:
    identificador: str
    livro: Livro
    usuario: Usuario
    data_emprestimo: date
    data_prevista_devolucao: date
    data_devolucao: date | None = None

    def esta_ativo(self) -> bool:
        return self.data_devolucao is None

    def esta_atrasado(self, data_referencia: date) -> bool:
        return self.esta_ativo() and self.data_prevista_devolucao < data_referencia

    def dias_de_atraso(self, data_referencia: date) -> int:
        if not self.esta_atrasado(data_referencia):
            return 0
        return (data_referencia - self.data_prevista_devolucao).days

    def devolvido_em(self, data: date) -> "Emprestimo":
        return Emprestimo(
            identificador=self.identificador,
            livro=self.livro,
            usuario=self.usuario,
            data_emprestimo=self.data_emprestimo,
            data_prevista_devolucao=self.data_prevista_devolucao,
            data_devolucao=data,
        )
