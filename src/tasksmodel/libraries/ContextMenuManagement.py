from typing import Callable, List

from PyQt6.QtCore import Qt, QPoint, QModelIndex
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

from components.TaskListView import TaskListView
from utilities.enumerations.TaskActionEnum import TaskActionEnum
from utilities.enumerations.TaskSectionEnum import TaskSectionEnum


def _createContextMenuItems(modifyTaskFunction: Callable, taskId: int, targetTaskListView: TaskListView)\
        -> List[QAction]:
    """
    Create the context menu for a specified section.

    :param modifyTaskFunction: the function to modify tasks
    :param taskId: the id of the associated task
    :param targetTaskListView: the TaskListView of the section to create a menu for
    :return: a list of context menu actions
    """
    contextActionItems: List[QAction] = []
    taskSection: TaskSectionEnum = TaskSectionEnum[targetTaskListView.name]

    editTaskAction: QAction = QAction(text="Edit", parent=targetTaskListView)
    editTaskAction.triggered.connect(lambda: modifyTaskFunction(taskAction=TaskActionEnum.EDIT,
                                                                taskSection=taskSection,
                                                                targetTaskSections=[taskSection],
                                                                taskId=taskId))
    contextActionItems.append(editTaskAction)

    deleteTaskAction: QAction = QAction(text="Delete", parent=targetTaskListView)
    deleteTaskAction.triggered.connect(lambda: modifyTaskFunction(taskAction=TaskActionEnum.DELETE,
                                                                  taskSection=taskSection,
                                                                  targetTaskSections=[taskSection],
                                                                  taskId=taskId))
    contextActionItems.append(deleteTaskAction)

    if taskSection in (TaskSectionEnum.IN_PROGRESS, TaskSectionEnum.COMPLETED):
        moveToToDoTaskAction: QAction = QAction(text="Move to To-Do", parent=targetTaskListView)
        moveToToDoTaskAction.triggered.connect(lambda: modifyTaskFunction(taskAction=TaskActionEnum.MOVE,
                                                                          taskSection=taskSection,
                                                                          newTaskSection=TaskSectionEnum.TO_DO,
                                                                          targetTaskSections=[
                                                                              taskSection, TaskSectionEnum.TO_DO
                                                                          ],
                                                                          taskId=taskId))
        contextActionItems.append(moveToToDoTaskAction)

    elif taskSection == TaskSectionEnum.TO_DO:
        moveToInProgressTaskAction: QAction = QAction(text="Move to In-Progress", parent=targetTaskListView)
        moveToInProgressTaskAction.triggered.connect(
            lambda: modifyTaskFunction(taskAction=TaskActionEnum.MOVE,
                                       taskSection=taskSection,
                                       newTaskSection=TaskSectionEnum.IN_PROGRESS,
                                       targetTaskSections=[taskSection, TaskSectionEnum.IN_PROGRESS],
                                       taskId=taskId))
        contextActionItems.append(moveToInProgressTaskAction)

    if taskSection == TaskSectionEnum.IN_PROGRESS:
        moveToCompletedTaskAction: QAction = QAction(text="Move to Completed", parent=targetTaskListView)
        moveToCompletedTaskAction.triggered.connect(lambda:
                                                    modifyTaskFunction(taskAction=TaskActionEnum.MOVE,
                                                                       taskSection=taskSection,
                                                                       newTaskSection=TaskSectionEnum.COMPLETED,
                                                                       targetTaskSections=[
                                                                           taskSection, TaskSectionEnum.COMPLETED
                                                                       ],
                                                                       taskId=taskId))
        contextActionItems.append(moveToCompletedTaskAction)

    return contextActionItems


def showContextMenu(modifyTaskFunction: Callable, targetTaskListView: TaskListView, event: QPoint) -> None:
    """
    Show the context menu for a task.

    :param modifyTaskFunction: the function to modify tasks
    :param targetTaskListView: the section to show the menu for
    :param event: the triggering event
    """
    contextMenu: QMenu = QMenu(parent=targetTaskListView)
    taskIndex: QModelIndex = targetTaskListView.indexAt(event)

    if taskIndex.isValid():
        taskId: int = taskIndex.data(Qt.ItemDataRole.UserRole)
        contextMenuItems: List[QAction] = _createContextMenuItems(modifyTaskFunction=modifyTaskFunction, taskId=taskId,
                                                                  targetTaskListView=targetTaskListView)

        for contextMenuItem in contextMenuItems:
            contextMenu.addAction(contextMenuItem)
        contextMenu.exec(targetTaskListView.mapToGlobal(event))
