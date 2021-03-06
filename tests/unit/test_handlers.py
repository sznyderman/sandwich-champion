from __future__ import annotations

import pytest

from sandwichchampion.domain import model
from sandwichchampion.adapters import repository, notifications
from sandwichchampion.service_layer import unit_of_work, handlers, messagebus


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


class FakeNotifications(notifications.AbstractNotification):
    def __init__(self):
        self.sent = []

    def send(self, message):
        self.sent.append(message)


@pytest.fixture
def bus():
    uow = FakeUnitOfWork()
    bus = messagebus.MessageBus(
        uow, handlers.command_handlers, handlers.event_handlers, FakeNotifications()
    )
    return bus


class TestCreateSandwich:
    def test_add_sandwich(self, bus):
        bus.handle(handlers.CreateSandwichCommand(name="Grilled Cheese"))

        assert bus.uow.sandwiches.get_sandwich("Grilled Cheese") is not None
        assert bus.uow.committed

    def test_adding_a_sandwich_with_a_name_that_is_already_assigned_raises(self, bus):
        bus.handle(handlers.CreateSandwichCommand(name="Grilled Cheese"))

        with pytest.raises(handlers.DuplicateSandwichNameError):
            bus.handle(handlers.CreateSandwichCommand(name="Grilled Cheese"))

    def test_sends_notification_that_a_new_sandwich_was_created(self, bus):
        bus.handle(handlers.CreateSandwichCommand(name="Grilled Cheese"))

        assert bus.notifications.sent == ["New sandwich: Grilled Cheese."]
