from enum import Enum


class TaskSectionEnum(Enum):
    """
    The task sections of the app.
    """
    IN_PROGRESS = {
        "type": "taskSection",
        "name": "In-Progress",
        "actionButtons": [
            {
                "name": "Clear",
                "label": "Clear All"
            },
            {
                "name": "Add",
                "label": "Add Task"
            }
        ]
    }

    TO_DO = {
        "type": "taskSection",
        "name": "To-Do",
        "actionButtons": [
            {
                "name": "Add",
                "label": "Add Task"
            }
        ]
    }

    COMPLETED = {
        "type": "taskSection",
        "name": "Completed",
        "actionButtons": []
    }
