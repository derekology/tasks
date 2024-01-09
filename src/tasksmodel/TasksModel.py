from functools import partial
from typing import Any, Callable, List, Dict, Tuple, Set

from PyQt6 import QtCore
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QAbstractItemView

from components.TaskItem import TaskItem
from components.TaskListView import TaskListView
from tasksmodel.libraries.ContextMenuManagement import showContextMenu
from tasksmodel.libraries.TaskListManagement import createNewTaskList, sortTaskList
from tasksmodel.libraries.TaskManagement import addTask, deleteTask, editTask
from utilities.abstractclasses.AbstractObserver import AbstractObserver
from utilities.abstractclasses.AbstractSubject import AbstractSubject
from utilities.enumerations.EventTypeEnum import EventTypeEnum
from utilities.enumerations.TaskActionEnum import TaskActionEnum
from utilities.enumerations.TaskSectionEnum import TaskSectionEnum


class TasksModel(AbstractSubject):
    """
    The model of a Tasks application.
    """

    def __init__(self, taskListViews: Dict[str, TaskListView]):
        """
        Create a TasksModel instance.

        :param taskListViews: the taskListViews of the TaskApp
        """
        super().__init__()

        self.createNewTaskList: Callable = createNewTaskList

        self._observers: List[AbstractObserver] = []
        self._taskList: Dict[str, List[TaskItem]] = {section: [] for section in
                                                     [taskSectionEnum.name for taskSectionEnum in
                                                      list(TaskSectionEnum)]}
        self._taskListViews: Dict[str, TaskListView] = taskListViews
        self.sortTaskList: Callable = partial(sortTaskList, self._taskList)

    @property
    def taskList(self) -> Dict[str, List[TaskItem]]:
        """
        Get the current task list.

        :return: the current task list
        """
        return self._taskList

    @taskList.setter
    def taskList(self, value: Dict[str, List[TaskItem]]) -> None:
        """
        Set the task list to a new value.

        :param value: the new task list
        """
        self._taskList: Dict[str, List[TaskItem]] = value

    def modifyTask(self, taskAction: TaskActionEnum, taskSection: TaskSectionEnum,
                   targetTaskSections: List[TaskSectionEnum], **kwargs) -> None:
        """
        Modify a task.

        :param taskAction: the modification action
        :param taskSection: the section of the affected task
        :param targetTaskSections: the affected sections
        :param kwargs: other arguments specific to the modification action
        """
        if taskAction == TaskActionEnum.ADD:
            addTaskDialogResult: Tuple[bool, Tuple[str, float]] = (
                self._notifyObservers(event=EventTypeEnum.ADD_TASK_DIALOG_REQUESTED, taskSection=taskSection))[0]

            if addTaskDialogResult[0] and len(addTaskDialogResult[1]) == 2:
                newTask: TaskItem = TaskItem(name=addTaskDialogResult[1][0], targetTime=addTaskDialogResult[1][1])
                addTask(taskSectionList=self.taskList[taskSection.name], newTask=newTask)

        elif taskAction == TaskActionEnum.EDIT:
            tasksToEdit: Set[TaskItem] = set([taskItem for taskItem in self.taskList[taskSection.name] if
                                              taskItem.id == kwargs["taskId"]])
            for task in tasksToEdit:
                if taskSection == TaskSectionEnum.COMPLETED:
                    editTaskDialogResult: Tuple[bool, Tuple[str, float, float]] = (
                        self._notifyObservers(event=EventTypeEnum.COMPLETED_TASK_DIALOG_REQUESTED,
                                              completedTask=task))[0]
                else:
                    editTaskDialogResult: Tuple[bool, Tuple[str, float, float]] = (
                        self._notifyObservers(event=EventTypeEnum.EDIT_TASK_DIALOG_REQUESTED, taskToEdit=task))[0]

                if editTaskDialogResult[0] and len(editTaskDialogResult[1]) == 3:
                    editTask(taskToEdit=task, updateData=editTaskDialogResult[1])

        elif taskAction == TaskActionEnum.DELETE:
            tasksToDelete: Set[TaskItem] = set([taskItem for taskItem in self.taskList[taskSection.name] if
                                                taskItem.id == kwargs["taskId"]])

            for task in tasksToDelete:
                deleteTask(targetTaskList=self.taskList[taskSection.name], taskToDelete=task)

        elif taskAction == TaskActionEnum.MOVE:
            tasksToMove: Set[TaskItem] = set([taskItem for taskItem in self.taskList[taskSection.name] if
                                              taskItem.id == kwargs["taskId"]])
            for task in tasksToMove:
                deleteTask(targetTaskList=self.taskList[taskSection.name], taskToDelete=task)
                addTask(taskSectionList=self.taskList[kwargs["newTaskSection"].name], newTask=task)

                if kwargs["newTaskSection"] == TaskSectionEnum.COMPLETED:
                    self.modifyTask(taskAction=TaskActionEnum.EDIT,
                                    taskSection=kwargs["newTaskSection"],
                                    targetTaskSections=[kwargs["newTaskSection"]],
                                    taskId=kwargs["taskId"]
                                    )

        elif taskAction == TaskActionEnum.MOVE_ALL:
            for task in self.taskList[taskSection.name]:
                self.modifyTask(taskAction=TaskActionEnum.MOVE,
                                taskSection=taskSection,
                                newTaskSection=kwargs["newTaskSection"],
                                targetTaskSections=[taskSection, kwargs["newTaskSection"]],
                                taskId=task.id)

        self.sortTaskList()
        self.populateTaskListViews(targetTaskSections=targetTaskSections)
        self._notifyObservers(event=EventTypeEnum.TASK_LIST_MODIFIED)

    def populateTaskListViews(self, targetTaskSections: List[TaskSectionEnum] = None) -> None:
        """
        Populate the task list view with the current task list.
        Will populate all task list views if no target is given.

        :param targetTaskSections: (optional) the task sections to update
        """
        if not targetTaskSections:
            targetTaskSections: List[TaskSectionEnum] = [taskSection for taskSection in TaskSectionEnum
                                                         if taskSection.name in self._taskListViews.keys()]

        for taskSection in targetTaskSections:
            taskListView: TaskListView = self._taskListViews[taskSection.name]
            model: QStandardItemModel = QStandardItemModel()
            taskListView.setModel(model)
            taskListView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

            if not taskListView.contextMenuSignalConnected:
                taskListView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
                taskListView.customContextMenuRequested.connect(
                    partial(showContextMenu, self.modifyTask, self._taskListViews[taskSection.name])
                )
                taskListView.contextMenuSignalConnected = True

            for task in self.taskList[taskSection.name]:
                taskText = f"{task.name} (Est: {task.targetTime} hrs"
                taskText += f" | Act: {task.elapsedTime} hrs)" if task.elapsedTime else ")"
                taskItem: QStandardItem = QStandardItem(taskText)
                taskItem.setData(task.id, QtCore.Qt.ItemDataRole.UserRole)
                model.appendRow(taskItem)

    def _notifyObservers(self, event: EventTypeEnum, **kwargs) -> List[Any]:
        """
        Notify all observers of an event.

        :param event: the event
        :param kwargs: additional event data
        """
        responses = []

        for observer in self._observers:
            observer.notify(event, data=kwargs)
            responses.append(observer.getResponse())

        return responses
