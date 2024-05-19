import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# region sqlalchemy fixtures
# from https://medium.com/@vittorio.camisa/agile-database-integration-tests-with-python-sqlalchemy-and-factory-boy-6824e8fe33a1
engine = create_engine("sqlite:///:memory:")
Session = sessionmaker()


@pytest.fixture(scope="module")
def db_conn():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def db_session(db_conn):
    transaction = db_conn.begin()
    session = Session(bind=db_conn)
    yield session
    session.close()
    transaction.rollback()


# endregion
