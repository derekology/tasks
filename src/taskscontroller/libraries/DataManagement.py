import base64
import binascii
import json
import os
import shutil
import sys
from json import JSONDecodeError
from typing import Any, List, Dict
from uuid import UUID

from PyQt6.QtWidgets import QWidget

from components.TaskItem import TaskItem
from dialogwindows.OverwriteTaskListDialog import OverwriteTaskListDialog
from src import DATA_FOLDER_PATH
from tasksmodel.libraries.TaskListManagement import createNewTaskList

SAVE_FILE_NAME: str = "tasks.dat"


def saveTaskList(taskListToSave: Dict[str, List[TaskItem]]) -> None:
    """
    Save the current task list to an external file.
    Will create a backup in the same folder.
    """
    backUpFileName: str = SAVE_FILE_NAME.split(sep=".")[0]
    os.makedirs(DATA_FOLDER_PATH, exist_ok=True)

    try:
        shutil.copy(src=os.path.join(DATA_FOLDER_PATH, SAVE_FILE_NAME),
                    dst=os.path.join(DATA_FOLDER_PATH, f"{backUpFileName}.bak"))

    except FileNotFoundError:
        pass

    saveData: str = json.dumps(obj=taskListToSave, cls=CustomTaskListJSONEncoder)
    obfuscated_data: str = base64.b64encode(s=saveData.encode()).decode()
    with open(os.path.join(DATA_FOLDER_PATH, SAVE_FILE_NAME), "w") as file:
        file.write(obfuscated_data)


def loadTaskList(parent: QWidget) -> Dict[str, List[TaskItem]]:
    """
    Attempt to load the existing task list.
    Creates a new one if none exists, or if existing data is corrupted.

    :param parent: the parent window
    :return: the existing or blank task list
    """
    try:
        os.makedirs(DATA_FOLDER_PATH, exist_ok=True)
        with open(os.path.join(DATA_FOLDER_PATH, SAVE_FILE_NAME), "r") as file:
            obfuscated_data = file.read()

        saved_data = base64.b64decode(obfuscated_data.encode()).decode()
        return json.loads(saved_data, object_hook=CustomTaskListJSONEncoder.decode)

    except FileNotFoundError:
        return createNewTaskList()

    except (JSONDecodeError, UnicodeDecodeError, binascii.Error):
        return createNewTaskList() if _showOverwriteTaskListDialog(parent=parent) else sys.exit()


def _showOverwriteTaskListDialog(parent: QWidget) -> int:
    """
    Show the dialog to ask the user to confirm task list overwrite.

    :param parent: the parent window
    :return: whether the dialog was accepted
    """
    return OverwriteTaskListDialog(parent=parent, message="Unable to load previous data.").exec()


class CustomTaskListJSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder.
    Necessary to handle saving and loading TaskItem objects.
    """

    @staticmethod
    def decode(data: dict) -> dict | UUID | TaskItem:
        """
        Check to see if data is a TaskItem and instantiate one as needed.

        :param data: the save data being loaded
        :return: the save data
        """
        if "__type__" in data and data["__type__"] == "TaskItem":
            taskItem: TaskItem = TaskItem()
            taskItem.__dict__.update(data["data"])

            return taskItem

        elif "__type__" in data and data["__type__"] == "UUID":
            return UUID(data["data"])

        return data

    def default(self, obj: Any) -> Any:
        """
        Check type of object and encode appropriately.

        :param obj: the object being encoded
        :return: the encoded object
        """
        if isinstance(obj, TaskItem):
            return {"__type__": "TaskItem", "data": obj.__dict__}

        elif isinstance(obj, UUID):
            return {"__type__": "UUID", "data": str(obj)}

        elif isinstance(obj, dict):
            return {key: self.default(value) for key, value in obj.items()}

        return super().default(obj)
