from PySide2.QtWidgets import QGraphicsItem, QGraphicsScene
from PySide2.QtWidgets import ItemIsMovable, ItemSendsGeometryChanges
from PySide2.QtWidgets import DeviceCoordinateCache


class Node(QGraphicsItem):

    def __init__(self, graph_widget):
        super(Node, self).__init__()

        self.edges = []
        self.__graph = graph_widget
        self.__new_pos = 0
        self.Type = QGraphicsItem.UserType + 1

        self.setFlag(ItemIsMovable)
        self.setFlag(ItemSendsGeometryChanges)
        self.setCacheMode(DeviceCoordinateCache)
        self.setZValue(-1)

    def type(self):
        return self.Type

    def add_edge(self, edge):
        self.edges.append(edge)
        edge.adjust()

    def calculate_forces(self):
        if not QGraphicsScene() or QGraphicsScene.mouseGrabberItem() == self:
            self.__new_pos = self.pos()

    def advance_position(self):
        pass

    def boundingRect(self):
        pass

    def shape(self):
        pass

    def paint(self, painter, option, widget):
        pass

    def itemChange(self, change, value):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass
