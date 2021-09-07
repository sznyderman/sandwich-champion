from __future__ import annotations
from typing import TYPE_CHECKING

import abc

from ..domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, sandwich: model.Sandwich):
        ...

    @abc.abstractmethod
    def get_sandwich(self, name: str) -> model.Sandwich:
        ...


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, sandwich: model.Sandwich):
        self.session.add(sandwich)

    def get_sandwich(self, name: str) -> model.Sandwich:
        return self.session.query(model.Sandwich).filter_by(name=name).first()
