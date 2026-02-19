from models.database import Database
from typing import Self, Any, Optional
from sqlite3 import Cursor


class Desejo:
    """
    Representa um item da lista de desejos (livro, filme, série, etc.).
    Métodos para salvar, listar, buscar por ID, atualizar e excluir.
    """

    CATEGORIAS = ["Livro", "Filme", "Série", "Anime", "Documentário", "Geral"]

    def __init__(
        self,
        titulo: str = "",
        data_limite: Optional[str] = None,
        categoria: str = "Geral",
        prioridade: int = 1,
        id_desejo: Optional[int] = None,
    ) -> None:
        self.titulo: str = titulo
        self.data_limite: Optional[str] = data_limite
        self.categoria: str = categoria
        self.prioridade: int = prioridade
        self.id_desejo: Optional[int] = id_desejo

    def __repr__(self) -> str:
        return (
            f"Desejo(titulo={self.titulo!r}, categoria={self.categoria!r}, "
            f"prioridade={self.prioridade}, id={self.id_desejo})"
        )

    # ── CRUD ──────────────────────────────────────────────

    def salvar(self) -> None:
        """Insere um novo desejo no banco de dados."""
        with Database() as db:
            query = """
                INSERT INTO desejos (titulo, data_limite, categoria, prioridade)
                VALUES (?, ?, ?, ?);
            """
            params = (self.titulo, self.data_limite, self.categoria, self.prioridade)
            db.executar(query, params)

    @classmethod
    def listar_todos(cls) -> list[Self]:
        """Retorna todos os desejos ordenados por prioridade (maior primeiro)."""
        with Database() as db:
            query = "SELECT id, titulo, data_limite, categoria, prioridade FROM desejos ORDER BY prioridade DESC, id DESC;"
            resultados: list[Any] = db.buscar_todos(query)
            return [
                cls(
                    titulo=titulo,
                    data_limite=data,
                    categoria=cat,
                    prioridade=prio,
                    id_desejo=id_,
                )
                for id_, titulo, data, cat, prio in resultados
            ]

    @classmethod
    def buscar_por_id(cls, id_desejo: int) -> Self:
        """Busca um desejo pelo ID."""
        with Database() as db:
            query = "SELECT id, titulo, data_limite, categoria, prioridade FROM desejos WHERE id = ?;"
            resultado = db.buscar_um(query, (id_desejo,))
            if resultado is None:
                raise ValueError(f"Desejo com id={id_desejo} não encontrado.")
            id_, titulo, data, cat, prio = resultado
            return cls(
                titulo=titulo,
                data_limite=data,
                categoria=cat,
                prioridade=prio,
                id_desejo=id_,
            )

    def atualizar(self) -> Cursor:
        """Atualiza o desejo no banco de dados."""
        with Database() as db:
            query = """
                UPDATE desejos
                SET titulo = ?, data_limite = ?, categoria = ?, prioridade = ?
                WHERE id = ?;
            """
            params = (
                self.titulo,
                self.data_limite,
                self.categoria,
                self.prioridade,
                self.id_desejo,
            )
            return db.executar(query, params)

    def excluir(self) -> Cursor:
        """Remove o desejo do banco de dados."""
        with Database() as db:
            query = "DELETE FROM desejos WHERE id = ?;"
            return db.executar(query, (self.id_desejo,))
