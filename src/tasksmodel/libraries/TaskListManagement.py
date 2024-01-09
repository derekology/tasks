from typing import List, Dict

from components.TaskItem import TaskItem
from utilities.enumerations.TaskSectionEnum import TaskSectionEnum


def createNewTaskList() -> Dict[str, List[TaskItem]]:
    """
    Create a new, blank task list.
    Based on sections enumerated in TaskSectionEnum.

    :return: a blank task list
    """
    return {taskSection.name: [] for taskSection in TaskSectionEnum}


def sortTaskList(taskList: Dict[str, List[TaskItem]], targetTaskSections: List[TaskSectionEnum] = None) -> None:
    """
    Sort each task list section in-place by name.
    Will sort all sections if none target sections are provided.

    :param taskList: the current task list
    :param targetTaskSections: (optional) the task sections to sort
    """
    if not targetTaskSections:
        targetTaskSections = [taskSection for taskSection in TaskSectionEnum]

    for taskSection in targetTaskSections:
        taskList[taskSection.name].sort(key=lambda task: task.name)
