from ..domain import model


class DuplicateSandwichNameError(RuntimeError):
    pass


def create_sandwich(name: str, uow):
    sandwich = model.Sandwich(name)

    with uow:
        if uow.sandwiches.get_sandwich(name):
            raise DuplicateSandwichNameError(
                f"Cannot create a sandwich with the name {name} because there is already another sandwich with that name."
            )
        uow.sandwiches.add(sandwich)
        uow.commit()
