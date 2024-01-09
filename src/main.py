import sys

from PyQt6.QtWidgets import QApplication

from taskscontroller.TasksController import TasksController
from tasksmodel.TasksModel import TasksModel
from tasksview.TasksView import TasksView


def main():
    """
    Drives the program.
    """
    tasksApp: QApplication = QApplication([])
    tasksView: TasksView = TasksView()
    tasksModel: TasksModel = TasksModel(tasksView.taskListViews)
    tasksView.show()

    _tasksController: TasksController = TasksController(model=tasksModel, view=tasksView)
    sys.exit(tasksApp.exec())


if __name__ == "__main__":
    main()
