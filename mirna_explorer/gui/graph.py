import PySide2.QtWidgets as QtWidgets


class Graph(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.button1 = QtWidgets.QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.button2 = QtWidgets.QPushButton("Button 2")
        self.layout.addWidget(self.button2)

        self.setLayout(self.layout)
