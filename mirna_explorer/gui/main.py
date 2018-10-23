import PySide2.QtWidgets as QtWidgets
from gui.widgets.orchestrator import Orchestrator
from gui.menubar import Menubar


class MirnaExplorer(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle('Mirna Explorer')
        self.resize(1024, 768)
        self._center()

        self.orchestrator = Orchestrator(self)
        self.setCentralWidget(self.orchestrator)

        Menubar(self)

    def _center(self):
        geometry = self.frameGeometry()
        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center)
        self.move(geometry.topLeft())
