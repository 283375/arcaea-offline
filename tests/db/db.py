from sqlalchemy import Engine, create_engine, inspect


def create_engine_in_memory():
    return create_engine("sqlite:///:memory:")
