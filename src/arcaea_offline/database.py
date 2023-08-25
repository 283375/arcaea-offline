from sqlalchemy import Engine
from sqlalchemy.orm import Session

from .models.common import *
from .models.scores import *
from .models.songs import *


def init(engine: Engine, checkfirst: bool = True):
    # sqlalchemy-utils issue #396
    # view.create_view() causes DuplicateTableError on Base.metadata.create_all(checkfirst=True)
    # https://github.com/kvesteri/sqlalchemy-utils/issues/396
    if checkfirst:
        ScoresViewBase.metadata.drop_all(engine)

    SongsBase.metadata.create_all(engine, checkfirst=checkfirst)
    ScoresBase.metadata.create_all(engine, checkfirst=checkfirst)
    ScoresViewBase.metadata.create_all(engine)
    CommonBase.metadata.create_all(engine, checkfirst=checkfirst)
    with Session(engine) as session:
        session.add(Property(id="version", value="2"))
        session.commit()
