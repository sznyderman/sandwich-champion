from __future__ import annotations
from typing import Dict, Type, Callable, TYPE_CHECKING

from . import handlers

if TYPE_CHECKING:
    from . import unit_of_work


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        command_handlers: Dict[Type[handlers.Command], Callable],
    ):
        self.uow = uow
        self.command_handlers = command_handlers

    def handle(self, message: handlers.Command):
        self.handle_command(message)

    def handle_command(self, command: handlers.Command):
        handler = self.command_handlers[type(command)]
        handler(command, self.uow)
