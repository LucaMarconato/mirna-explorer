import sys
from PySide2 import QtWidgets
from graph_widget import GraphWidget


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    widget = GraphWidget()

    window = QtWidgets.QMainWindow()
    window.setCentralWidget(widget)
    window.show()

    sys.exit(app.exec_())
