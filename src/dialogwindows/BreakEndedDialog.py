import os
from functools import partial

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLayout, QPushButton, QLabel
from playsound import playsound, PlaysoundException

from dialogwindows import CONFIRM_BUTTON_LABEL
from dialogwindows.ButtonWidget import ButtonWidget
from src import ASSETS_FOLDER_PATH

WINDOW_TITLE: str = "Break over"
WINDOW_WIDTH: int = 150
BREAK_ENDED_MESSAGE: str = "Get back to work!"
ALARM_PATH: str = os.path.join(ASSETS_FOLDER_PATH, "sounds", "alarm.wav")


class BreakEndedDialog(QDialog):
    """
    A Break Ended dialog with sound.
    """
    def __init__(self, parent: QWidget):
        """
        Create a Break Ended dialog.

        :param parent: the parent widget
        """
        super().__init__(parent=parent)

        self.soundTimer: QTimer = QTimer()

        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedWidth(150)
        self.setLayout(self._setUpLayout())
        self._playAlarmSound()

    def _generateButtons(self) -> QWidget:
        """
        Generate the buttons in the Break Ended dialog.

        :return: the buttons for the dialog
        """
        buttonWidget: ButtonWidget = ButtonWidget()
        buttonLayout = buttonWidget.layout()

        confirmButton: QPushButton = QPushButton(text=CONFIRM_BUTTON_LABEL, parent=self)
        confirmButton.clicked.connect(self.accept)
        buttonLayout.addWidget(confirmButton)

        return buttonWidget

    def _generateMessage(self) -> QWidget:
        """
        Generate the message of the Overwrite Tasks List dialog.

        :return: the message for the dialog
        """
        messageWidget: QWidget = QWidget()
        messageLayout: QLayout = QVBoxLayout()
        messageLayout.setContentsMargins(0, 0, 0, 0)
        messageWidget.setLayout(messageLayout)

        messageLayout.addWidget(QLabel(text=BREAK_ENDED_MESSAGE, parent=self))

        return messageWidget

    def _playAlarmSound(self) -> None:
        """
        Play the alarm sound.
        """
        try:
            playsound(ALARM_PATH, False)
            self.soundTimer.timeout.connect(partial(playsound, ALARM_PATH, False))
            self.soundTimer.start(1000)

        except PlaysoundException:
            pass

    def _setUpLayout(self) -> QLayout:
        """
        Set up the layout of the Overwrite Tasks List dialog.

        :return: the layout of the dialog
        """
        dialogLayout: QLayout = QVBoxLayout()
        dialogLayout.addWidget(self._generateMessage())
        dialogLayout.addWidget(self._generateButtons())

        return dialogLayout
