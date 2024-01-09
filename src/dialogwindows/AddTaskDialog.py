from typing import Tuple

from PyQt6.QtWidgets import QDialog, QFormLayout, QPushButton, QLabel, QWidget

from dialogwindows import TASK_NAME_FIELD_LABEL, ESTIMATED_HOURS_FIELD_LABEL, ADD_BUTTON_LABEL
from dialogwindows.DialogField import TaskNameDialogField, TimeDialogField
from utilities.enumerations.TaskSectionEnum import TaskSectionEnum


class AddTaskDialog(QDialog):
    """
    An Add Task dialog.
    """
    def __init__(self, parent: QWidget, taskSection: TaskSectionEnum):
        """
        Create an Add Task dialog.

        :param parent: the parent widget
        :param taskSection: the task section to be added to
        """
        super().__init__(parent=parent)
        self._taskSection: TaskSectionEnum = taskSection

        self.setWindowTitle(f"Add task to \'{taskSection.value['name']}\'")
        self.setLayout(self._setUpLayout())
        self._taskNameField.setFocus()

    def getUserInput(self) -> Tuple[str, float]:
        """
        Get the user's input for task name and task target time.

        :return: the new task's name (idx1) and target time (idx2)
        """
        return self._taskName, self._taskTargetTime

    def _handleConfirm(self) -> None:
        """
        Process the confirmation of a new task to be added.
        """
        if self._taskNameField.text() and self._taskTargetTimeField.text():
            self._taskName: str = self._taskNameField.text()
            self._taskTargetTime: float = float(self._taskTargetTimeField.text())\
                if float(self._taskTargetTimeField.text()) > 0 else 0
            self.accept()
        else:
            self.reject()

    def _setUpLayout(self) -> QFormLayout:
        """
        Set up the fields in the Add Task dialog.

        :return: the fields for the Add Task dialog
        """
        dialogLayout: QFormLayout = QFormLayout()

        self._taskNameField: TaskNameDialogField = TaskNameDialogField()
        dialogLayout.addRow(QLabel(text=TASK_NAME_FIELD_LABEL, parent=self), self._taskNameField)

        self._taskTargetTimeField: TimeDialogField = TimeDialogField()
        dialogLayout.addRow(QLabel(text=ESTIMATED_HOURS_FIELD_LABEL, parent=self), self._taskTargetTimeField)

        confirmButton: QPushButton = QPushButton(text=ADD_BUTTON_LABEL, parent=self)
        confirmButton.clicked.connect(self._handleConfirm)
        dialogLayout.addRow(confirmButton)

        return dialogLayout
