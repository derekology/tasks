from typing import Tuple

from PyQt6.QtWidgets import QDialog, QFormLayout, QPushButton, QLabel, QWidget, QLayout, QVBoxLayout

from components.TaskItem import TaskItem
from dialogwindows import ACTUAL_HOURS_FIELD_LABEL, SAVE_BUTTON_LABEL
from dialogwindows.DialogField import TimeDialogField

WINDOW_TITLE = "Task completed"
COMPLETED_MESSAGE = "Nice! How long did it take?"


class CompletedTaskDialog(QDialog):
    """
    A Completed Task dialog.
    """
    def __init__(self, parent: QWidget, completedTask: TaskItem):
        """
        Create a Completed Task dialog.

        :param parent: the parent widget
        :param completedTask: the task to edit
        """
        super().__init__(parent=parent)
        self._completedTask: TaskItem = completedTask

        self.setWindowTitle(WINDOW_TITLE)
        self.setLayout(self._setUpLayout())
        self._taskElapsedTimeField.setFocus()

    def getUserInput(self) -> Tuple[str, float, float]:
        """
        Get the user's input for task elapsed time.

        :return: the completed task's name (idx1), target time (idx2), and elapsed time (idx3)
        """
        return self._completedTask.name, self._completedTask.targetTime, self._taskElapsedTime

    def _generateMessage(self) -> QWidget:
        """
        Generate the message of the Completed Task dialog.

        :return: the message for the dialog
        """
        messageWidget: QWidget = QWidget()
        messageLayout: QLayout = QVBoxLayout()
        messageLayout.setContentsMargins(0, 0, 0, 5)
        messageWidget.setLayout(messageLayout)

        messageLayout.addWidget(QLabel(text=COMPLETED_MESSAGE, parent=self))

        return messageWidget

    def _handleConfirm(self) -> None:
        """
        Process the confirmation of a completed task update.
        """
        if self._taskElapsedTimeField.text():
            self._taskElapsedTime: float = float(self._taskElapsedTimeField.text())
            self.accept()
        else:
            self.reject()

    def _setUpLayout(self) -> QFormLayout:
        """
        Set up the fields in the Completed Task dialog.

        :return: the fields for the Completed Task dialog
        """
        dialogLayout: QFormLayout = QFormLayout()
        elapsedTimeInitial: float = self._completedTask.elapsedTime if self._completedTask.elapsedTime > 0 \
            else self._completedTask.targetTime

        dialogLayout.addRow(self._generateMessage())

        dialogLayout.addRow(QLabel("Task Name", parent=self), QLabel(text=self._completedTask.name, parent=self))
        dialogLayout.addRow(QLabel("Est. Time", parent=self), QLabel(text=str(self._completedTask.targetTime),
                                                                     parent=self))

        self._taskElapsedTimeField: TimeDialogField = TimeDialogField(initialText=str(elapsedTimeInitial))
        dialogLayout.addRow(QLabel(text=ACTUAL_HOURS_FIELD_LABEL, parent=self), self._taskElapsedTimeField)

        confirmButton: QPushButton = QPushButton(text=SAVE_BUTTON_LABEL, parent=self)
        confirmButton.clicked.connect(self._handleConfirm)
        dialogLayout.addRow(confirmButton)

        return dialogLayout
