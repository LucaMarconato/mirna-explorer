from PySide2.QtWidgets import QWidget, QGridLayout
from gui.widgets.graph import GraphWidget


class Orchestrator(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        grid = QGridLayout()
        grid.setSpacing(10)
        graph_widget = GraphWidget()
        grid.addWidget(graph_widget, 1, 0)

        self.setLayout(grid)
