from PyQt6.QtWidgets import QListView


class TaskListView(QListView):
    """
    A list view to display tasks.
    """

    def __init__(self, name: str):
        """
        Create a TaskListView instance.

        :param name: the name of the TaskListView
        """
        super().__init__()
        self._name: str = name
        self._contextMenuSignalConnected: bool = False

    @property
    def contextMenuSignalConnected(self) -> bool:
        """
        Get whether the contextMenuRequested signal is currently connected to a slot.

        :return: whether the contextMenuRequested signal is currently connected
        """
        return self._contextMenuSignalConnected

    @contextMenuSignalConnected.setter
    def contextMenuSignalConnected(self, value: bool) -> None:
        """
        Set whether the contextMenuRequested signal is currently connected to a slot.

        :param value whether the contextMenuRequested signal is currently connected
        """
        self._contextMenuSignalConnected: bool = value

    @property
    def name(self) -> str:
        """
        Get the name of the TaskListView.

        :return: the name of the TaskListView
        """
        return self._name
