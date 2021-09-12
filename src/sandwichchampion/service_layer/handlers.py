from dataclasses import dataclass
from ..domain import model


class Command:
    pass


@dataclass
class CreateSandwichCommand(Command):
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


command_handlers = {CreateSandwichCommand: create_sandwich}
