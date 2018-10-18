import sys
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets
from gui.main import MirnaExplorer
from assets.assets_mapper import AssetsMapper


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MirnaExplorer()
    window.setWindowIcon(QtGui.QIcon(AssetsMapper.APP_ICON.value))
    window.show()

    sys.exit(app.exec_())
