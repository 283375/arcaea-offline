import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# region sqlalchemy fixtures
engine = create_engine("sqlite:///:memory:")
Session = sessionmaker()


@pytest.fixture(scope="session")
def db_conn():
    conn = engine.connect()
    yield conn
    conn.close()


@pytest.fixture()
def db_session(db_conn):
    session = Session(bind=db_conn)
    yield session
    session.close()

    # drop everything
    query_tables = db_conn.execute(
        text("SELECT name FROM sqlite_master WHERE type='table'")
    ).fetchall()
    for row in query_tables:
        table_name = row[0]
        db_conn.execute(text(f"DROP TABLE {table_name}"))

    query_views = db_conn.execute(
        text("SELECT name FROM sqlite_master WHERE type='view'")
    ).fetchall()
    for row in query_views:
        view_name = row[0]
        db_conn.execute(text(f"DROP VIEW {view_name}"))

    query_indexes = db_conn.execute(
        text("SELECT name FROM sqlite_master WHERE type='index'")
    ).fetchall()
    for row in query_indexes:
        index_name = row[0]
        db_conn.execute(text(f"DROP INDEX {index_name}"))

    query_triggers = db_conn.execute(
        text("SELECT name FROM sqlite_master WHERE type='trigger'")
    ).fetchall()
    for row in query_triggers:
        trigger_name = row[0]
        db_conn.execute(text(f"DROP TRIGGER {trigger_name}"))


# endregion
