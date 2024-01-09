from enum import Enum


class TaskActionEnum(Enum):
    """
    The actions that can be taken on a task.
    """
    ADD = "ADD"
    EDIT = "EDIT"
    MOVE = "MOVE"
    DELETE = "DELETE"
    MOVE_ALL = "MOVE ALL"
