from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QLineEdit

from dialogwindows import FLOAT_VALIDATION_REGEX


class TimeDialogField(QLineEdit):
    """
    An input field specific to time in hours.
    Allows only floats.
    """
    def __init__(self, initialText: str = None):
        """
        Create a TimeDialogField instance.

        :param initialText: (optional) the initial text in the field
        """
        super().__init__()
        if initialText:
            self.setText(initialText)
        self.setValidator(QRegularExpressionValidator(QRegularExpression(FLOAT_VALIDATION_REGEX)))


class TaskNameDialogField(QLineEdit):
    """
    An input field specific to task names.
    """
    def __init__(self, initialText: str = None):
        """
        Create a TaskNameDialogField instance.

        :param initialText: (optional) the initial text in the field
        """
        super().__init__()
        if initialText:
            self.setText(initialText)
