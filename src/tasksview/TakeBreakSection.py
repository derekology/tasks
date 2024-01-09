from functools import partial
from time import strftime, gmtime
from typing import Dict

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QLayout, QVBoxLayout

from dialogwindows.BreakEndedDialog import BreakEndedDialog

TAKE_BREAK_BUTTON_NAME: str = "takeBreakButton"
TAKE_A_BREAK_TEXT: str = "☕ Take a 10-minute break"
TAKING_BREAK_TEXT: str = "😌 Taking a break..."
DEFAULT_BREAK_TIME: int = 600  # Default break time in seconds.


def _showBreakEndedDialog(parent: QWidget) -> None:
    """
    Show the break ended dialog.

    :param parent: the parent window
    """
    BreakEndedDialog(parent=parent).exec()


class TakeBreakSection(QWidget):
    """
    A Take Break section.
    """

    def __init__(self, parent: QWidget):
        """
        Create a TakeBreakSection instance.
        
        :param parent: the parent widget
        """
        super().__init__()
        self._breakTimer: QTimer | None = None
        self._parent: QWidget = parent
        self._createTakeBreakSection()

    @property
    def breakSectionWidget(self) -> QWidget:
        """
        Get the current Take Break section widget.

        :return: the current Take Break section widget
        """
        return self._takeBreakSectionWidget

    def toggleBreakTimer(self, breakTimeInSeconds: int = 0) -> None:
        """
        Toggle the break timer.
        Will end the break if break time is 0 seconds.

        :param breakTimeInSeconds: (optional) the total break time in seconds
        """
        if not self._breakTimer and breakTimeInSeconds > 0:
            self._breakTimer: QTimer = QTimer()
            timeLeft: int = breakTimeInSeconds

            def decrementTimeLeft() -> None:
                """
                Decrement the time left variable by one and display it on the break button.
                """
                nonlocal timeLeft
                timeLeft -= 1

                if timeLeft > 0:
                    self._displayTakeBreakButtonTimer(timeLeft)
                else:
                    self._displayTakeBreakButtonTimer()
                    self._breakTimer.stop()
                    self._breakTimer = None
                    _showBreakEndedDialog(parent=self._parent)

            self._breakTimer.timeout.connect(decrementTimeLeft)
            self._breakTimer.start(1000)

        else:
            self._displayTakeBreakButtonTimer()

            if self._breakTimer:
                self._breakTimer.stop()
                self._breakTimer: QTimer | None = None

    def _createTakeBreakSection(self) -> None:
        """
        Create a take break section.

        :return: the take break section (idx1) and associated buttons (idx2)
        """
        takeBreakSectionWidget: QWidget = QWidget()
        takeBreakSectionLayout: QLayout = QVBoxLayout()
        takeBreakSectionLayout.setContentsMargins(0, 0, 0, 0)
        takeBreakSectionWidget.setLayout(takeBreakSectionLayout)

        takeBreakButton: QPushButton = QPushButton(text=TAKE_A_BREAK_TEXT)
        takeBreakSectionLayout.addWidget(takeBreakButton)

        self._takeBreakSectionWidget: QWidget = takeBreakSectionWidget
        self._takeBreakSectionButtons: Dict[str, QPushButton] = {TAKE_BREAK_BUTTON_NAME: takeBreakButton}

        for button in self._takeBreakSectionButtons.values():
            button.clicked.connect(partial(self.toggleBreakTimer, DEFAULT_BREAK_TIME))

    def _displayTakeBreakButtonTimer(self, remainingTimeInSeconds: int = 0) -> None:
        """
        Display the remaining break time on the take a break button.
        Will reset the button label if time remaining is 0.

        :param remainingTimeInSeconds: the remaining break time in seconds
        """
        timeRemainingText: str = strftime("%H:%M:%S", gmtime(remainingTimeInSeconds))

        self._takeBreakSectionButtons[TAKE_BREAK_BUTTON_NAME].setText(f"{TAKING_BREAK_TEXT} ({timeRemainingText})") \
            if remainingTimeInSeconds > 0 else \
            self._takeBreakSectionButtons[TAKE_BREAK_BUTTON_NAME].setText(TAKE_A_BREAK_TEXT)
