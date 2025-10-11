# app/db/pool.py
from __future__ import annotations
import logging
import sys
import os
from pathlib import Path
from typing import Literal, Any
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from app.utils.config import db_settings, app_name
from app.utils.logging import setup_logging
# Prefer package-relative imports. When the module is executed as a script (python app/db/dbConnectionPool.py)
# the package context is not set and relative imports will fail. Try relative imports first and fall back
# to adjusting sys.path so `app` is importable by absolute name. This makes the module flexible for dev runs.
# try:
#     from app.utils.config import db_settings, app_name
#     from app.utils.logging import setup_logging
# except Exception:
#     # Running as a script: add project root to sys.path and import by package name
#     project_root = Path(__file__).resolve().parents[2]
#     sys.path.insert(0, str(project_root))
#     from app.utils.config import db_settings, app_name
#     from app.utils.logging import setup_logging

_logger = logging.getLogger(__name__)
_connection_pool: ThreadedConnectionPool | None = None

def init_pool():
    """Initialize global connection pool (idempotent)."""

    global _connection_pool
    if _connection_pool is not None:
        _logger.info("DB pool already initialized.")
        return

    db_config = db_settings()
    _connection_pool = ThreadedConnectionPool(
                                                minconn=db_config["minconn"],
                                                maxconn=db_config["maxconn"],
                                                host=db_config["host"],
                                                port=db_config["port"],
                                                dbname=db_config["name"],
                                                user=db_config["user"],
                                                password=db_config["password"],
                                                connect_timeout=db_config["connect_timeout"],
                                                application_name=app_name(),
                                            )
    _logger.info("DB pool initialized to %s@%s:%s (%s..%s)",db_config["name"], db_config["host"], db_config["port"], db_config["minconn"], db_config["maxconn"])

def close_pool():
    global _connection_pool
    if _connection_pool is not None:
        _connection_pool.closeall()
        _logger.info("DB connection pool closed.")
        _connection_pool = None

def _get_conn():
    if _connection_pool is None:
        init_pool()
        # raise RuntimeError("DB pool not initialized. Call init_pool() first.")
    return _connection_pool.getconn()

def _release_conn(conn):
    if _connection_pool is not None and conn is not None:
        _connection_pool.putconn(conn)

def execute(
    query: str,
    params: tuple | list | None = None,
    fetch: Literal["one", "all", None] = None,
    commit: bool = False,
) -> Any:
    """
    Low-level safe executor used by repositories.
    Returns dict(s) for SELECT via RealDictCursor.
    """
    conn = None
    cur = None
    try:
        conn = _get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, params or ())

        result = None
        if fetch == "one":
            result = cur.fetchone()
        elif fetch == "all":
            result = cur.fetchall()

        if commit:
            conn.commit()
        return result
    except Exception:
        if conn:
            conn.rollback()
        _logger.exception("DB error: %s | params=%s", query, params)
        raise
    finally:
        if cur:
            try:
                cur.close()
            except Exception:
                pass
        if conn:
            _release_conn(conn)

def ping() -> str:
    row = execute("SELECT 'pong' AS ping;", fetch="one")
    return row["ping"] if row else "no-response"

if __name__ == "__main__":
    init_pool()
    try:
        print("Ping:", ping())
    finally:
        close_pool()
