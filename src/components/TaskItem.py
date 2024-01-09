from uuid import uuid4, UUID


class TaskItem:
    """
    A task item object.
    """

    def __init__(self, name: str = None, targetTime: float = 0, elapsedTime: float = 0):
        """
        Create a taskItem instance.

        :param name: the name of the task
        :param targetTime: the target time duration in hours
        :param elapsedTime: the elapsed time in hours
        """
        self._id: UUID = uuid4()
        self.name: str = name
        self.targetTime: float = targetTime
        self.elapsedTime: float = elapsedTime

    @property
    def id(self) -> UUID:
        """
        Get the id of the TaskItem object.

        :return: the id of the TaskItem object
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Get the current name of the TaskItem object.

        :return: the current name
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the TaskItem object.

        :param value: the new name
        """
        self._name: str = value

    @property
    def targetTime(self) -> float:
        """
        Get the current target time of the TaskItem object.

        :return: the current target time
        """
        return self._targetTime

    @targetTime.setter
    def targetTime(self, value: float) -> None:
        """
        Set the target time of the TaskItem object.

        :param value: the new target time
        """
        self._targetTime: float = value

    @property
    def elapsedTime(self) -> float:
        """
        Get the current elapsed time for the TaskItem object.

        :return: the current elapsed time
        """
        return self._elapsedTime

    @elapsedTime.setter
    def elapsedTime(self, value: float) -> None:
        """
        Set the elapsed time for the TaskItem object.

        :param value: the new elapsed time
        """
        self._elapsedTime: float = value
