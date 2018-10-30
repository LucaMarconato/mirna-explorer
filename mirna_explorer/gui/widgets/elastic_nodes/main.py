import sys
from PySide2.QtCore import qsrand, QTime
from PySide2.QtWidgets import QApplication, QMainWindow
from graph_widget import GraphWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))

    widget = GraphWidget()
    window = QMainWindow()
    window.setCentralWidget(widget)
    window.show()

    sys.exit(app.exec_())
