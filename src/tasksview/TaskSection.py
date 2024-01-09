from typing import Dict

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from components.TaskListView import TaskListView
from utilities.enumerations.TaskSectionEnum import TaskSectionEnum


class TaskSection(QWidget):
    def __init__(self, taskSection: TaskSectionEnum):
        """
        Create a TaskSection instance.

        :param taskSection the task section to create
        """
        super().__init__()
        self._taskSection: TaskSectionEnum = taskSection
        self._taskSectionName: str = taskSection.name
        self._taskSectionLabel: str = taskSection.value["name"]
        self._actionButtons: Dict[str, QPushButton] = {}
        self._taskSectionWidget: QWidget = self._createTaskSection()

    @property
    def actionButtons(self) -> Dict[str, QPushButton]:
        """
        Get the current task section's action buttons.

        :return: the current task section's action buttons
        """
        return self._actionButtons

    @property
    def taskSectionLabel(self) -> str:
        """
        Get the current task section label.

        :return: the current task section label
        """
        return self._taskSectionLabel

    @property
    def taskSectionName(self) -> str:
        """
        Get the current task section name.

        :return: the current task section name
        """
        return self._taskSectionName

    @property
    def taskListView(self) -> TaskListView:
        """
        Get the current task section's task list view.

        :return: the current task section's task list view
        """
        return self._taskListView

    @property
    def taskSectionWidget(self) -> QWidget:
        """
        Get the current task section widget.

        :return: the current task section widget
        """
        return self._taskSectionWidget

    def _createTaskSection(self) -> QWidget:
        """
        Create a task section widget for this application.

        :return: a task section widget for this application
        """
        taskSectionWidget: QWidget = QWidget(self)
        taskSectionLayout: QLayout = QVBoxLayout()
        taskSectionLayout.setContentsMargins(0, 0, 0, 0)
        taskSectionLayout.setSpacing(0)
        taskSectionWidget.setLayout(taskSectionLayout)

        taskSectionHeaderWidget: QWidget = self._createTaskSectionHeader()
        taskSectionLayout.addWidget(taskSectionHeaderWidget)

        taskListSectionWidget: QWidget = QWidget(self)
        taskListSectionLayout: QLayout = QVBoxLayout()
        taskListSectionLayout.setContentsMargins(0, 0, 0, 10)
        taskListSectionWidget.setLayout(taskListSectionLayout)

        taskListView: TaskListView = TaskListView(name=self.taskSectionName)
        taskListSectionLayout.addWidget(taskListView)

        self._taskListView = taskListView
        taskSectionLayout.addWidget(taskListSectionWidget)

        return taskSectionWidget

    def _createTaskSectionHeader(self) -> QWidget:
        """
        Create a task section header widget for this application.

        :return: a task section header widget for this application
        """
        taskSectionHeaderWidget: QWidget = QWidget(self)
        taskSectionHeaderLayout: QLayout = QHBoxLayout()
        taskSectionHeaderLayout.setContentsMargins(0, 0, 0, 5)
        taskSectionHeaderWidget.setLayout(taskSectionHeaderLayout)
        taskSectionHeaderWidget.setFixedHeight(25)

        taskSectionHeaderLayout.addWidget(QLabel(text=self.taskSectionLabel, parent=self), 3)

        actionButtonsArray: QWidget = QWidget(self)
        actionButtonsArrayLayout: QHBoxLayout = QHBoxLayout()
        actionButtonsArrayLayout.setContentsMargins(0, 0, 0, 0)
        actionButtonsArray.setLayout(actionButtonsArrayLayout)

        for actionButton in self._taskSection.value["actionButtons"]:
            button: QPushButton = QPushButton(text=actionButton["label"], parent=self)
            actionButtonsArrayLayout.addWidget(button, 0, Qt.AlignmentFlag.AlignRight)
            self.actionButtons[actionButton["name"]]: QPushButton = button

        taskSectionHeaderLayout.addWidget(actionButtonsArray)

        return taskSectionHeaderWidget
