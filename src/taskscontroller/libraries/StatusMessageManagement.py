from typing import List, Dict

from components.TaskItem import TaskItem
from utilities.enumerations.TaskSectionEnum import TaskSectionEnum


def countTasks(taskList: Dict[str, List[TaskItem]]) -> Dict[str, int]:
    """
    Counts the tasks by section.

    :param taskList: the current task list
    :return: the task count per section
    """
    return {TaskSectionEnum[taskSection].value["name"]: len(tasks) for taskSection, tasks in taskList.items()}


def generateTaskCountSummary(taskList: Dict[str, List[TaskItem]]) -> str:
    """
    Generates a summary of the number of tasks in each section.
    Uses " | " as a seperator between sections and their counts.

    :param taskList: the current task list
    :return: the task count summary
    """
    taskCountSummary: List[str] = \
        [f"{taskSectionName}: {taskCount}" for taskSectionName, taskCount in countTasks(taskList=taskList).items()]

    return " ｜ ".join(taskCountSummary)
