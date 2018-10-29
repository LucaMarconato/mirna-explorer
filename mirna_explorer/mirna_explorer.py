import sys
from PySide2 import QtGui, QtWidgets
from gui.main import MirnaExplorer
from assets.assets_mapper import AssetsMapper


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MirnaExplorer()
    window.setWindowIcon(QtGui.QIcon(AssetsMapper.APP_ICON.value))
    window.show()

    sys.exit(app.exec_())
