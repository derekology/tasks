from typing import List, Tuple

from components.TaskItem import TaskItem


def addTask(taskSectionList: List[TaskItem], newTask) -> TaskItem:
    """
    Add a task to the task list.

    :param taskSectionList: the section that the task should be added to
    :param newTask: the new task to be added
    :return: the new task item
    """
    taskSectionList.append(newTask)
    return newTask


def deleteTask(targetTaskList: List[TaskItem], taskToDelete: TaskItem) -> TaskItem:
    """
    Delete a task from a task list.

    :param targetTaskList: the task list that contains the task to delete
    :param taskToDelete: the task to delete
    :return: the deleted task item
    """
    try:
        targetTaskList.remove(taskToDelete)

    except ValueError:
        pass

    return taskToDelete


def editTask(taskToEdit: TaskItem, updateData: Tuple[str, float, float]) -> TaskItem:
    """
    Edit a task from the task list.

    :param taskToEdit: the task to edit
    :param updateData: the update data containing the task name(idx1), target time (idx2), and elapsed time (idx3)
    :return: the edited task item
    """
    taskToEdit.name = updateData[0]
    taskToEdit.targetTime = updateData[1]
    taskToEdit.elapsedTime = updateData[2]

    return taskToEdit
