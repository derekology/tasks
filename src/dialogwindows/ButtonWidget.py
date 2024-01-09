from PyQt6.QtWidgets import QWidget, QLayout, QHBoxLayout


class ButtonWidget(QWidget):
    """
    A QWidget for dialog window buttons.
    """
    def __init__(self):
        """
        Create a ButtonWidget instance.
        """
        super().__init__()
        buttonLayout: QLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(0, 10, 0, 0)
        self.setLayout(buttonLayout)
