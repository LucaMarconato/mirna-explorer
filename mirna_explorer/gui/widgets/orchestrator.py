import PySide2.QtWidgets as QtWidgets
from gui.widgets.graph import GraphWidget


class Orchestrator(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        graph_widget = GraphWidget()
        grid.addWidget(graph_widget, 1, 0)

        self.setLayout(grid)
