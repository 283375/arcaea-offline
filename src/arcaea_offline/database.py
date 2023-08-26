from sqlalchemy import Engine, inspect, select
from sqlalchemy.orm import sessionmaker

from .models.config import *
from .models.scores import *
from .models.songs import *
from .singleton import Singleton


class Database(metaclass=Singleton):
    def __init__(self, engine: Engine):
        self.engine = engine

    @property
    def engine(self):
        return self.__engine

    @engine.setter
    def engine(self, value: Engine):
        if not isinstance(value, Engine):
            raise ValueError("Database.engine only accepts sqlalchemy.Engine")
        self.__engine = value
        self.__sessionmaker = sessionmaker(self.__engine)

    @property
    def sessionmaker(self):
        return self.__sessionmaker

    def init(self, checkfirst: bool = True):
        # create tables & views
        if checkfirst:
            # > https://github.com/kvesteri/sqlalchemy-utils/issues/396
            # > view.create_view() causes DuplicateTableError on Base.metadata.create_all(checkfirst=True)
            # so if `checkfirst` is True, drop these views before creating
            ScoresViewBase.metadata.drop_all(self.engine)

        SongsBase.metadata.create_all(self.engine, checkfirst=checkfirst)
        ScoresBase.metadata.create_all(self.engine, checkfirst=checkfirst)
        ScoresViewBase.metadata.create_all(self.engine)
        ConfigBase.metadata.create_all(self.engine, checkfirst=checkfirst)

        # insert version property
        with self.sessionmaker() as session:
            stmt = select(Property.value).where(Property.key == "version")
            result = session.execute(stmt).fetchone()
            if not checkfirst or not result:
                session.add(Property(key="version", value="2"))
                session.commit()

    def check_init(self) -> bool:
        # check table exists
        expect_tables = (
            list(SongsBase.metadata.tables.keys())
            + list(ScoresBase.metadata.tables.keys())
            + list(ConfigBase.metadata.tables.keys())
            + [
                Calculated.__tablename__,
                Best.__tablename__,
                CalculatedPotential.__tablename__,
            ]
        )
        return all(inspect(self.engine).has_table(t) for t in expect_tables)
