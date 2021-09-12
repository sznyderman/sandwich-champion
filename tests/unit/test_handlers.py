from __future__ import annotations

import pytest

from sandwichchampion.domain import model
from sandwichchampion.adapters import repository
from sandwichchampion.service_layer import unit_of_work, handlers


class FakeRepository(repository.AbstractRepository):
    def __init__(self, sandwiches):
        super().__init__()
        self._sandwiches = set(sandwiches)

    def add(self, sandwich):
        self._sandwiches.add(sandwich)

    def get_sandwich(self, name):
        return next((sw for sw in self._sandwiches if sw.name == name), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.sandwiches = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


class TestCreateSandwich:
    def test_add_sandwich(self):
        uow = FakeUnitOfWork()

        handlers.create_sandwich("Grilled Cheese", uow)

        assert uow.sandwiches.get_sandwich("Grilled Cheese") is not None
        assert uow.committed

    def test_adding_a_sandwich_with_a_name_that_is_already_assigned_raises(self):
        uow = FakeUnitOfWork()
        uow.sandwiches.add(model.Sandwich("Grilled Cheese"))

        with pytest.raises(handlers.DuplicateSandwichNameError):
            handlers.create_sandwich("Grilled Cheese", uow)
