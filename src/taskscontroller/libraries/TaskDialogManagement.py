from typing import Tuple

from PyQt6.QtWidgets import QWidget

from components.TaskItem import TaskItem
from dialogwindows.AddTaskDialog import AddTaskDialog
from dialogwindows.CompletedTaskDialog import CompletedTaskDialog
from dialogwindows.EditTaskDialog import EditTaskDialog
from utilities.enumerations.TaskSectionEnum import TaskSectionEnum


def showAddTaskDialog(parent: QWidget, taskSection: TaskSectionEnum) -> Tuple[bool, Tuple[str, float] | None]:
    """
    Show the dialog to add a new task.

    :param parent: the parent window
    :param taskSection: the section to add the task to
    :return: whether the data was successfully captured (idx1) and the data captured (idx2)
             containing the updated task's name (idx1) and target time (idx2)
    """
    addTaskDialogWindow: AddTaskDialog = AddTaskDialog(taskSection=taskSection, parent=parent)
    addTaskDialogWindowResult: int = addTaskDialogWindow.exec()

    return (True, addTaskDialogWindow.getUserInput()) if addTaskDialogWindowResult else (False, None)


def showCompletedTaskDialog(parent: QWidget, completedTask: TaskItem) -> Tuple[bool, Tuple[str, float, float] | None]:
    """
    Show the dialog upon completion of a task.
    Congratulates the user and prompts for the final elapsed time.

    :param parent: the parent window
    :param completedTask: the completed task
    :return: whether the data was successfully captured (idx1) and the completed task's
             elapsed time (idx2)
    """
    completedTaskDialogWindow: CompletedTaskDialog = CompletedTaskDialog(parent=parent, completedTask=completedTask)
    completedTaskDialogWindowResult: int = completedTaskDialogWindow.exec()

    return (True, completedTaskDialogWindow.getUserInput()) if completedTaskDialogWindowResult else (False, None)


def showEditTaskDialog(parent: QWidget, taskToEdit: TaskItem) -> Tuple[bool, Tuple[str, float, float] | None]:
    """
    Show the dialog to edit a task.

    :param parent: the parent window
    :param taskToEdit: the task to edit
    :return: whether the data was successfully captured (idx1) and the data captured (idx2)
             containing the updated task's name (idx1), target time (idx2), and elapsed time (idx3)
    """
    editTaskDialogWindow: EditTaskDialog = EditTaskDialog(parent=parent, taskToEdit=taskToEdit)
    editTaskDialogWindowResult: int = editTaskDialogWindow.exec()

    return (True, editTaskDialogWindow.getUserInput()) if editTaskDialogWindowResult else (False, None)
