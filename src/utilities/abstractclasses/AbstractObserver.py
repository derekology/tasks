from abc import ABC, abstractmethod
from typing import Any

from utilities.enumerations.EventTypeEnum import EventTypeEnum


class AbstractObserver(ABC):
    """
    An Observer blueprint.
    For use in an observer pattern setup.
    """
    @abstractmethod
    def notify(self, event: EventTypeEnum, data: Any = None) -> None:
        """
        Notify this observer of an event.

        :param event: the event
        :param data: (optional) additional data needed to respond
        """
        pass

    @abstractmethod
    def getResponse(self) -> Any:
        """
        Get the response of an observed event.

        :return: the response of an observed event
        """
        pass
