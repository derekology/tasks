from typing import Tuple

from PyQt6.QtWidgets import QDialog, QFormLayout, QPushButton, QLabel, QWidget

from components.TaskItem import TaskItem
from dialogwindows import TASK_NAME_FIELD_LABEL, ESTIMATED_HOURS_FIELD_LABEL, ACTUAL_HOURS_FIELD_LABEL, \
    SAVE_BUTTON_LABEL
from dialogwindows.DialogField import TimeDialogField, TaskNameDialogField

WINDOW_TITLE = "Edit Task"


class EditTaskDialog(QDialog):
    """
    An Edit Task dialog.
    """
    def __init__(self, parent: QWidget, taskToEdit: TaskItem):
        """
        Create an Edit Task dialog.

        :param parent: the parent widget
        :param taskToEdit: the task to edit
        """
        super().__init__(parent=parent)
        self._taskToEdit: TaskItem = taskToEdit

        self.setWindowTitle(WINDOW_TITLE)
        self.setLayout(self._setUpLayout())
        self._taskElapsedTimeField.setFocus()

    def getUserInput(self) -> Tuple[str, float, float]:
        """
        Get the user's input for task name, task target time, and task elapsed time.

        :return: the updated task's name (idx1), target time (idx2), and elapsed time (idx3)
        """
        return self._taskName, self._taskTargetTime, self._taskElapsedTime

    def _handleConfirm(self) -> None:
        """
        Process the confirmation of a task update.
        """
        if self._taskNameField.text():
            self._taskName: str = self._taskNameField.text()
            self._taskTargetTime: float = float(self._taskTargetTimeField.text()) \
                if (self._taskTargetTimeField.text() and float(self._taskTargetTimeField.text()) > 0) else 0
            self._taskElapsedTime: float = float(self._taskElapsedTimeField.text()) \
                if (self._taskElapsedTimeField.text() and float(self._taskElapsedTimeField.text()) > 0) else 0
            self.accept()
        else:
            self.reject()

    def _setUpLayout(self) -> QFormLayout:
        """
        Set up the fields in the Edit Task dialog.

        :return: the fields for the Edit Task dialog
        """
        dialogLayout: QFormLayout = QFormLayout()

        self._taskNameField: TaskNameDialogField = TaskNameDialogField(initialText=self._taskToEdit.name)
        dialogLayout.addRow(QLabel(text=TASK_NAME_FIELD_LABEL, parent=self), self._taskNameField)

        self._taskTargetTimeField: TimeDialogField = TimeDialogField(initialText=str(self._taskToEdit.targetTime))
        dialogLayout.addRow(QLabel(text=ESTIMATED_HOURS_FIELD_LABEL, parent=self), self._taskTargetTimeField)

        self._taskElapsedTimeField: TimeDialogField = TimeDialogField(initialText=str(self._taskToEdit.elapsedTime))
        dialogLayout.addRow(QLabel(text=ACTUAL_HOURS_FIELD_LABEL, parent=self), self._taskElapsedTimeField)

        confirmButton: QPushButton = QPushButton(text=SAVE_BUTTON_LABEL, parent=self)
        confirmButton.clicked.connect(self._handleConfirm)
        dialogLayout.addRow(confirmButton)

        return dialogLayout
