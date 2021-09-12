import abc


class AbstractNotification(abc.ABC):
    @abc.abstractmethod
    def send(self, message):
        ...
