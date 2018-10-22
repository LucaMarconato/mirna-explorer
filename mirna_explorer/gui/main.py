import PySide2.QtWidgets as QtWidgets
from gui.graph import Graph
from gui.menubar import Menubar


class MirnaExplorer(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle(self.tr('Mirna Explorer'))
        self.resize(1024, 768)
        self._center()

        self.test_widget = Graph(self)
        self.setCentralWidget(self.test_widget)

        menubar = Menubar(self)

    def _center(self):
        geometry = self.frameGeometry()
        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center)
        self.move(geometry.topLeft())
