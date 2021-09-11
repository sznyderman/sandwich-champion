import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from sandwichchampion.domain import model
from sandwichchampion.adapters.orm import metadata, start_mappers
from sandwichchampion.service_layer import unit_of_work


@pytest.fixture
def mappers():
    start_mappers()
    try:
        yield
    finally:

        clear_mappers()


pytestmark = pytest.mark.usefixtures("mappers")


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


def insert_sandwich(session, name, rating):
    session.execute(
        "INSERT INTO sandwiches (name, rating) VALUES (:name, :rating)",
        dict(name=name, rating=rating),
    )


def test_add_sandwich(sqlite_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)

    with uow:
        sw = model.Sandwich("Bahn Mi")
        uow.sandwiches.add(sw)
        uow.commit()

    session = sqlite_session_factory()
    rows = list(session.execute('SELECT name, rating FROM "sandwiches"'))
    assert rows == [("Bahn Mi", 1000)]


def test_get_sandwich(sqlite_session_factory):
    session = sqlite_session_factory()
    insert_sandwich(session, "Grilled Cheese", 1000)
    insert_sandwich(session, "Caprese", 1000)

    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    with uow:
        sw = uow.sandwiches.get_sandwich("Grilled Cheese")
        assert sw.name == "Grilled Cheese"


def test_rolls_back_uncommitted_word_by_default(sqlite_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    with uow:
        insert_sandwich(uow.session, "Bahn Mi", 1000)

    session = sqlite_session_factory()
    rows = list(session.execute('SELECT * FROM "sandwiches"'))
    assert rows == []


def test_rolls_back_on_error(sqlite_session_factory):
    class MyException(Exception):
        pass

    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_sandwich(uow.session, "Grilled Cheese", 1000)
            raise MyException()

    new_session = sqlite_session_factory()
    rows = list(new_session.execute('SELECT * FROM "sandwiches"'))
    assert rows == []
