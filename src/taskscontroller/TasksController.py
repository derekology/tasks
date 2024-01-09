from functools import partial
from typing import Any, Callable, Tuple

from taskscontroller.libraries.DataManagement import saveTaskList, loadTaskList
from taskscontroller.libraries.StatusMessageManagement import generateTaskCountSummary
from taskscontroller.libraries.TaskDialogManagement import (showAddTaskDialog, showEditTaskDialog,
                                                            showCompletedTaskDialog)
from utilities.enumerations.EventTypeEnum import EventTypeEnum
from utilities.abstractclasses.AbstractObserver import AbstractObserver
from utilities.enumerations.TaskActionEnum import TaskActionEnum
from utilities.enumerations.TaskSectionEnum import TaskSectionEnum
from tasksview.TasksView import TasksView
from tasksmodel.TasksModel import TasksModel


class TasksController(AbstractObserver):
    """
    The Tasks App.
    """

    def __init__(self, model: TasksModel, view: TasksView):
        """
        Create an instance of Tasks App.

        :param model: the Tasks App model
        :param view: the Tasks App view
        """
        self._model: TasksModel = model
        self._view: TasksView = view
        self.saveTaskList: Callable = saveTaskList
        self.loadTaskList: Callable = loadTaskList
        self._eventResponse: Any = None

        self._connectButtonsToSlots()
        self._model.addObserver(self)
        self._model.taskList = self.loadTaskList(parent=self._view)
        self._model.sortTaskList()
        self._model.populateTaskListViews()
        self._view.statusBar.message = generateTaskCountSummary(taskList=self._model.taskList)

    def getResponse(self) -> Any:
        """
        Get the response of an observed event and reset the response value.

        :return: the response of an observed event
        """
        response: Any = self._eventResponse
        self._eventResponse: Any = None
        return response

    def notify(self, event: EventTypeEnum, **kwargs) -> None:
        """
        Notify the controller of an event.

        :param event: the event
        :param kwargs: additional data needed to respond
        """
        if event == EventTypeEnum.TASK_LIST_MODIFIED:
            self._view.statusBar.message = generateTaskCountSummary(taskList=self._model.taskList)
            self.notify(event=EventTypeEnum.SAVE_REQUESTED, data={"taskListToSave": self._model.taskList})

        elif event == EventTypeEnum.ADD_TASK_DIALOG_REQUESTED:
            self._eventResponse: Tuple[bool, Tuple[str, float]] = (
                showAddTaskDialog(parent=self._view, taskSection=kwargs["data"]["taskSection"]))

        elif event == EventTypeEnum.EDIT_TASK_DIALOG_REQUESTED:
            self._eventResponse: Tuple[bool, Tuple[str, float, float]] = (
                showEditTaskDialog(parent=self._view, taskToEdit=kwargs["data"]["taskToEdit"]))

        elif event == EventTypeEnum.COMPLETED_TASK_DIALOG_REQUESTED:
            self._eventResponse: Tuple[bool, Tuple[str, float, float] | None] = (
                showCompletedTaskDialog(parent=self._view, completedTask=kwargs["data"]["completedTask"]))

        elif event == EventTypeEnum.SAVE_REQUESTED:
            currentStatusBarMessage: str = self._view.statusBar.message
            self._view.statusBar.message = "Saving..."
            self.saveTaskList(taskListToSave=kwargs["data"]["taskListToSave"])
            self._view.statusBar.message = currentStatusBarMessage

    def _connectButtonsToSlots(self) -> None:
        """
        Connect buttons in view to action slots.
        """
        for taskSection, contents in self._view.taskListViewButtons.items():
            for buttonName, button in contents.items():
                if taskSection == TaskSectionEnum.IN_PROGRESS and buttonName == "Clear":
                    button.clicked.connect(lambda: self._model.modifyTask(taskAction=TaskActionEnum.MOVE_ALL,
                                                                          taskSection=TaskSectionEnum.IN_PROGRESS,
                                                                          newTaskSection=TaskSectionEnum.TO_DO,
                                                                          targetTaskSections=[
                                                                              TaskSectionEnum.IN_PROGRESS,
                                                                              TaskSectionEnum.TO_DO
                                                                          ]))
                elif buttonName == "Add":
                    button.clicked.connect(partial(self._model.modifyTask, TaskActionEnum.ADD,
                                                   taskSection, [taskSection]))
