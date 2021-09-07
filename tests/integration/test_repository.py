import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from sandwichchampion.adapters.orm import metadata, start_mappers
from sandwichchampion.adapters.repository import SqlAlchemyRepository
from sandwichchampion.domain import model


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    try:
        yield sessionmaker(bind=in_memory_db)()
    finally:
        clear_mappers()


@pytest.fixture
def repo(session):
    return SqlAlchemyRepository(session)


def test_sandwich_mapper_can_load_sandwiches(repo, session):
    session.execute(
        "INSERT INTO sandwiches (name, rating) VALUES "
        '("Grilled Cheese", 1000),'
        '("Caprese", 1000)'
    )

    expected = [model.Sandwich("Grilled Cheese"), model.Sandwich("Caprese")]

    assert session.query(model.Sandwich).all() == expected
    assert repo.get_sandwich("Grilled Cheese").name == "Grilled Cheese"
    assert repo.get_sandwich("Caprese").name == "Caprese"


def test_sandwich_mapper_can_save_sandwiches(session, repo):
    new_sw = model.Sandwich("Grilled Cheese")
    repo.add(new_sw)

    session.commit()

    rows = list(session.execute('SELECT name, rating FROM "sandwiches"'))
    assert rows == [("Grilled Cheese", 1000)]
