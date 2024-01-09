from PyQt6.QtWidgets import QStatusBar, QLabel

INITIAL_STATUS_BAR_MESSAGE = "Loading..."


class StatusBar(QStatusBar):
    def __init__(self):
        """
        Create a status bar.
        """
        super().__init__()
        self._message: QLabel = QLabel(text=INITIAL_STATUS_BAR_MESSAGE, parent=self)
        self.addPermanentWidget(self._message)

    @property
    def message(self) -> str:
        """
        Get the current message shown in the status bar.

        :return: the current status bar message
        """
        return self._message.text()

    @message.setter
    def message(self, value: str) -> None:
        """
        Set the message shown in the status bar.

        :param value: the message to be shown in the status bar
        """
        self._message.setText(value)
