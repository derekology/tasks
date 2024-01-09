import os

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from src import ASSETS_FOLDER_PATH


WINDOW_ICONS_PATH: str = os.path.join(ASSETS_FOLDER_PATH, "icons")


def createAppIcon() -> QIcon:
    """
    Create the main app icon.

    :return: the main app icon
    """
    appIcon: QIcon = QIcon(os.path.join(WINDOW_ICONS_PATH, "main.ico"))

    return appIcon
