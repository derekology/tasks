import ctypes
from typing import Dict

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLayout, QStatusBar

from components.TaskListView import TaskListView
from tasksview.TakeBreakSection import TakeBreakSection
from tasksview.libraries.BrandingManagement import createAppIcon
from tasksview.StatusBar import StatusBar
from tasksview.TaskSection import TaskSection
from utilities.enumerations.TaskSectionEnum import TaskSectionEnum


APP_ID = "derekw.productivity.tasks"
WINDOW_TITLE: str = "Tasks"
DEFAULT_WINDOW_WIDTH: int = 475
DEFAULT_WINDOW_HEIGHT: int = 445


class TasksView(QMainWindow):
    """
    The view of a Tasks application.
    """

    def __init__(self):
        """
        Create a TasksView instance.
        """
        super().__init__()

        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

        except Exception:
            pass

        self._generalLayout: QLayout = QVBoxLayout()
        self._statusBar: StatusBar = StatusBar()
        self._taskListViewButtons: Dict[TaskSectionEnum, Dict[str, QPushButton]] = {}
        self._taskListViews: Dict[str, TaskListView] = {}

        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        self.setMinimumSize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(createAppIcon())
        self.setCentralWidget(self._createCentralWidget())

        for taskSection in TaskSectionEnum:
            taskSectionObject: TaskSection = TaskSection(taskSection)
            self._taskListViews[taskSection.name]: TaskListView = taskSectionObject.taskListView
            self._taskListViewButtons[taskSection]: Dict[str, QPushButton] = taskSectionObject.actionButtons
            self._generalLayout.addWidget(taskSectionObject.taskSectionWidget)

        self._takeBreakSection: TakeBreakSection = TakeBreakSection(parent=self)
        self._generalLayout.addWidget(self._takeBreakSection.breakSectionWidget)
        
        self.setStatusBar(self._statusBar)

    @property
    def takeBreakSection(self) -> TakeBreakSection:
        """
        Get the current take break section.

        :return: the current take break section
        """
        return self._takeBreakSection

    @property
    def statusBar(self) -> QStatusBar:
        """
        Get the current status bar.

        :return: the current status bar
        """
        return self._statusBar

    @property
    def taskListViews(self) -> Dict[str, TaskListView]:
        """
        Get the current taskListViews.

        :return: the current taskListViews per section
        """
        return self._taskListViews

    @property
    def taskListViewButtons(self) -> Dict[TaskSectionEnum, Dict[str, QPushButton]]:
        """
        Get the current taskListViewButtons.

        :return: the current taskListViewButtons per section
        """
        return self._taskListViewButtons

    def _createCentralWidget(self) -> QWidget:
        """
        Create the central widget for this application.

        :return: the central widget for this application
        """
        centralWidget: QWidget = QWidget(self)
        centralWidget.setLayout(self._generalLayout)
        self._generalLayout.setContentsMargins(15, 13, 15, 13)

        return centralWidget
