from dataclasses import dataclass
from ..domain import model


class Command:
    pass


@dataclass
class CreateSandwichCommand(Command):
    name: str


class Event:
    pass


@dataclass
class SandwichCreated(Event):
    name: str


class DuplicateSandwichNameError(RuntimeError):
    pass


def create_sandwich(cmd: CreateSandwichCommand, uow):
    sandwich = model.Sandwich(cmd.name)

    with uow:
        if uow.sandwiches.get_sandwich(cmd.name):
            raise DuplicateSandwichNameError(
                f"Cannot create a sandwich with the name {cmd.name} because there is already another sandwich with that name."
            )
        uow.sandwiches.add(sandwich)
        uow.commit()

        uow.events.append(SandwichCreated(sandwich.name))


def send_new_sandwich_notification(event: SandwichCreated, notifications):
    notifications.send(f"New sandwich: {event.name}.")


command_handlers = {CreateSandwichCommand: create_sandwich}
event_handlers = {SandwichCreated: send_new_sandwich_notification}
