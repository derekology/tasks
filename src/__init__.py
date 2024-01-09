import os
import sys

ASSETS_FOLDER_PATH: str = os.path.join(getattr(sys, "_MEIPASS", os.path.abspath(".")), "assets")
DATA_FOLDER_PATH: str = os.path.join(os.path.expanduser("~\\Documents"), "derekwco", "tasks")
