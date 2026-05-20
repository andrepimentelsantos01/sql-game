import re
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from pathlib import Path

from app.schemas import QueryResult

MAX_ROWS = 100
QUERY_TIMEOUT_SECONDS = 2

BLOCKED_WORDS = {
    "alter",
    "attach",
    "create",
    "delete",
    "detach",
    "drop",
    "insert",
    "pragma",
    "replace",
    "update",
    "vacuum",
}

DENIED_ACTIONS = {
    sqlite3.SQLITE_ALTER_TABLE,
    sqlite3.SQLITE_ATTACH,
    sqlite3.SQLITE_CREATE_INDEX,
    sqlite3.SQLITE_CREATE_TABLE,
    sqlite3.SQLITE_CREATE_TEMP_INDEX,
    sqlite3.SQLITE_CREATE_TEMP_TABLE,
    sqlite3.SQLITE_CREATE_TEMP_TRIGGER,
    sqlite3.SQLITE_CREATE_TEMP_VIEW,
    sqlite3.SQLITE_CREATE_TRIGGER,
    sqlite3.SQLITE_CREATE_VIEW,
    sqlite3.SQLITE_DELETE,
    sqlite3.SQLITE_DETACH,
    sqlite3.SQLITE_DROP_INDEX,
    sqlite3.SQLITE_DROP_TABLE,
    sqlite3.SQLITE_DROP_TEMP_INDEX,
    sqlite3.SQLITE_DROP_TEMP_TABLE,
    sqlite3.SQLITE_DROP_TEMP_TRIGGER,
    sqlite3.SQLITE_DROP_TEMP_VIEW,
    sqlite3.SQLITE_DROP_TRIGGER,
    sqlite3.SQLITE_DROP_VIEW,
    sqlite3.SQLITE_INSERT,
    sqlite3.SQLITE_PRAGMA,
    sqlite3.SQLITE_TRANSACTION,
    sqlite3.SQLITE_UPDATE,
}


class QueryRejectedError(ValueError):
    pass


def ensure_read_query(query: str) -> None:
    stripped = query.strip()
    lowered = stripped.lower()
    if not lowered.startswith(("select", "with")):
        raise QueryRejectedError("Use apenas consultas SELECT ou WITH.")
    if ";" in stripped.rstrip(";"):
        raise QueryRejectedError("Envie apenas uma consulta por vez.")

    tokens = set(re.findall(r"\b[a-z_]+\b", lowered))
    blocked = sorted(tokens & BLOCKED_WORDS)
    if blocked:
        raise QueryRejectedError(f"Comando bloqueado: {blocked[0].upper()}.")


def _authorizer(action: int, *_args: object) -> int:
    if action in DENIED_ACTIONS:
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK


def _execute(database_path: Path, query: str) -> QueryResult:
    ensure_read_query(query)
    connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True, check_same_thread=False)
    connection.set_authorizer(_authorizer)
    deadline = time.monotonic() + QUERY_TIMEOUT_SECONDS
    connection.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 1000)
    try:
        cursor = connection.execute(query)
        columns = [description[0] for description in cursor.description or []]
        rows = cursor.fetchmany(MAX_ROWS + 1)
        if len(rows) > MAX_ROWS:
            raise QueryRejectedError(f"A consulta retornou mais de {MAX_ROWS} linhas. Refine o resultado.")
        return QueryResult(columns=columns, rows=[list(row) for row in rows])
    finally:
        connection.close()


def run_select_query(database_path: Path, query: str) -> QueryResult:
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_execute, database_path, query)
    try:
        return future.result(timeout=QUERY_TIMEOUT_SECONDS + 0.2)
    except TimeoutError as exc:
        raise QueryRejectedError("A consulta demorou demais. Tente simplificar sua SQL.") from exc
    except sqlite3.Error as exc:
        raise QueryRejectedError(f"SQLite respondeu: {exc}") from exc
    finally:
        executor.shutdown(wait=False, cancel_futures=True)
