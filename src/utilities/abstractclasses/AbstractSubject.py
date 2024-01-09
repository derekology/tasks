from abc import ABC, abstractmethod
from typing import Any, List

from utilities.abstractclasses.AbstractObserver import AbstractObserver
from utilities.enumerations.EventTypeEnum import EventTypeEnum


class AbstractSubject(ABC):
    """
    A Subject blueprint.
    For use in an observer pattern setup.
    """
    def __init__(self):
        """
        Create an AbstractSubject instance.
        """
        self._observers: List[AbstractObserver] = []

    def addObserver(self, observer: AbstractObserver) -> None:
        """
        Add an observer to this subject.

        :param observer: the observer to add
        """
        self._observers.append(observer)

    def removeObserver(self, observer: AbstractObserver) -> None:
        """
        Remove an observer from this subject.

        :param observer: the observer to remove
        """
        self._observers.remove(observer)

    @abstractmethod
    def _notifyObservers(self, event: EventTypeEnum) -> List[Any]:
        """
        Notify all observers of an event.

        :param event: the event
        :return: the responses from the observers
        """
        pass
