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
        event_handlers: Dict[Type[handlers.Event], Callable],
        notifications,
    ):
        self.uow = uow
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers
        self.notifications = notifications

    def handle(self, message: handlers.Command):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, handlers.Event):
                self.handle_event(message, self.notifications)
            elif isinstance(message, handlers.Command):
                self.handle_command(message)

    def handle_command(self, command: handlers.Command):
        handler = self.command_handlers[type(command)]
        handler(command, self.uow)
        self.queue.extend(self.uow.events)

    def handle_event(self, event: handlers.Event, notifications):
        handler = self.event_handlers[type(event)]
        handler(event, notifications)
