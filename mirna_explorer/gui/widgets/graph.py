from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QWidget, QGridLayout
from PySide2.QtCharts import QtCharts


class GraphWidget(QWidget):

    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        grid.addWidget(self.create_dummy_chart(), 0, 0)
        self.setLayout(grid)

    def create_dummy_chart(self):
        set0 = QtCharts.QBarSet('Jane')
        set1 = QtCharts.QBarSet('John')
        set2 = QtCharts.QBarSet('Axel')
        set3 = QtCharts.QBarSet('Mary')
        set4 = QtCharts.QBarSet('Samantha')

        set0.append([1, 2, 3, 4, 5, 6])
        set1.append([5, 0, 0, 4, 0, 7])
        set2.append([3, 5, 8, 13, 8, 5])
        set3.append([5, 6, 7, 3, 4, 5])
        set4.append([9, 7, 5, 3, 1, 2])

        bar_series = QtCharts.QBarSeries()
        bar_series.append(set0)
        bar_series.append(set1)
        bar_series.append(set2)
        bar_series.append(set3)
        bar_series.append(set4)

        line_series = QtCharts.QLineSeries()
        line_series.setName('trend')
        line_series.append(QtCore.QPoint(0, 4))
        line_series.append(QtCore.QPoint(1, 15))
        line_series.append(QtCore.QPoint(2, 20))
        line_series.append(QtCore.QPoint(3, 4))
        line_series.append(QtCore.QPoint(4, 12))
        line_series.append(QtCore.QPoint(5, 17))

        chart = QtCharts.QChart()
        chart.addSeries(bar_series)
        chart.addSeries(line_series)
        chart.setTitle('Simple example')

        categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        axis_x = QtCharts.QBarCategoryAxis()
        axis_x.append(categories)
        chart.setAxisX(axis_x, line_series)
        chart.setAxisX(axis_x, bar_series)
        axis_x.setRange('Jan', 'Jun')

        axis_y = QtCharts.QValueAxis()
        chart.setAxisY(axis_y, line_series)
        chart.setAxisY(axis_y, bar_series)
        axis_y.setRange(0, 20)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignBottom)

        chart_view = QtCharts.QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

        return chart_view
