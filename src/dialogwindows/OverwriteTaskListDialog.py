from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLayout, QPushButton, QLabel

from dialogwindows import EXIT_BUTTON_LABEL, CONFIRM_BUTTON_LABEL
from dialogwindows.ButtonWidget import ButtonWidget

WINDOW_TITLE: str = "Overwrite Task List"
OVERWRITE_TASKS_LIST_MESSAGE: str = "Would you like to overwrite your task list with a new one?"


class OverwriteTaskListDialog(QDialog):
    """
    An Overwrite Task List dialog.
    """
    def __init__(self, parent: QWidget, message: str):
        """
        Create an Overwrite Tasks List dialog.

        :param parent: the parent widget
        :param message: the message to generate
        """
        super().__init__(parent=parent)
        self.setWindowTitle(WINDOW_TITLE)
        self.setLayout(self._setUpLayout(message))

    def _generateButtons(self) -> QWidget:
        """
        Generate the buttons in the Overwrite Tasks List dialog.

        :return: the buttons for the dialog
        """
        buttonWidget: ButtonWidget = ButtonWidget()
        buttonLayout = buttonWidget.layout()

        exitButton: QPushButton = QPushButton(text=EXIT_BUTTON_LABEL, parent=self)
        exitButton.clicked.connect(self.reject)
        buttonLayout.addWidget(exitButton)

        confirmButton: QPushButton = QPushButton(text=CONFIRM_BUTTON_LABEL, parent=self)
        confirmButton.clicked.connect(self.accept)
        buttonLayout.addWidget(confirmButton)

        return buttonWidget

    def _generateMessage(self, message: str) -> QWidget:
        """
        Generate the message of the Overwrite Tasks List dialog.

        :param message: the message to generate
        :return: the message for the dialog
        """
        messageWidget: QWidget = QWidget()
        messageLayout: QLayout = QVBoxLayout()
        messageLayout.setContentsMargins(0, 0, 0, 0)
        messageWidget.setLayout(messageLayout)

        messageLayout.addWidget(QLabel(text=message, parent=self))
        messageLayout.addWidget(QLabel(text=OVERWRITE_TASKS_LIST_MESSAGE, parent=self))

        return messageWidget

    def _setUpLayout(self, message: str) -> QLayout:
        """
        Set up the layout of the Overwrite Tasks List dialog.

        :param message: the message to generate
        :return: the layout of the dialog
        """
        dialogLayout: QLayout = QVBoxLayout()
        dialogLayout.addWidget(self._generateMessage(message))
        dialogLayout.addWidget(self._generateButtons())

        return dialogLayout
