from sqlalchemy import Table, Column, Integer, String, Float, MetaData
from sqlalchemy.orm import mapper, relationship

from ..domain import model

metadata = MetaData()

sandwiches = Table(
    "sandwiches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("rating", Float),
)


def start_mappers():
    sandwich_mapper = mapper(model.Sandwich, sandwiches)
