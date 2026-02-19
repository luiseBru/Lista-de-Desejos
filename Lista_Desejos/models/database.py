from sqlite3 import Connection, connect, Cursor
from typing import Any, Self, Optional, Type
from types import TracebackType
import logging
import os

logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DATABASE", "./data/tarefas.sqlite3")


def init_db(db_path: str = DB_PATH) -> None:
    """Inicializa o banco de dados criando a tabela de desejos se não existir."""
    with connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS desejos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                data_limite TEXT,
                categoria TEXT DEFAULT 'Geral',
                prioridade INTEGER DEFAULT 1
            );
        """
        )
        logger.info("Banco de dados inicializado com sucesso.")


class Database:
    """
    Gerenciador de conexão SQLite com suporte a context manager.
    Uso recomendado: `with Database() as db: ...`
    """

    def __init__(self, db_path: str = DB_PATH) -> None:
        self._conn: Connection = connect(db_path)
        self._cursor: Cursor = self._conn.cursor()

    @property
    def cursor(self) -> Cursor:
        return self._cursor

    def executar(self, query: str, params: tuple = ()) -> Cursor:
        """Executa uma query com commit automático."""
        self._cursor.execute(query, params)
        self._conn.commit()
        return self._cursor

    def buscar_todos(self, query: str, params: tuple = ()) -> list[Any]:
        """Executa uma query SELECT e retorna todos os resultados."""
        self._cursor.execute(query, params)
        return self._cursor.fetchall()

    def buscar_um(self, query: str, params: tuple = ()) -> Optional[Any]:
        """Executa uma query SELECT e retorna um único resultado."""
        self._cursor.execute(query, params)
        return self._cursor.fetchone()

    def fechar(self) -> None:
        """Fecha a conexão com o banco de dados."""
        self._conn.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            logger.error(
                "Erro no contexto do banco: %s — %s",
                exc_type.__name__,
                exc_val,
            )
            self._conn.rollback()
        self.fechar()
