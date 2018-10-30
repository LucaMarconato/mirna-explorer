from edge import Edge
from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QGradient, QPainterPath, QPen
from PySide2.QtWidgets import QGraphicsItem, QGraphicsScene, QStyle


class Node(QGraphicsItem):

    def __init__(self, graph_widget):
        super(Node, self).__init__()

        self.edges = []
        self.__graph = graph_widget
        self.__newpos = 0
        self.Type = QGraphicsItem.UserType + 1

        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)

    def type(self):
        return self.Type

    def add_edge(self, edge):
        self.edges.append(edge)
        edge.adjust()

    def calculate_forces(self):
        if not QGraphicsScene() or QGraphicsScene.mouseGrabberItem() == self:
            self.__new_pos = self.pos()

        # Sum up all forces pushing this item away
        xvel, yvel = 0, 0
        for item in QGraphicsScene.items():
            node = self.qgraphicsitem_cast(item)
            if not node:
                continue

            vec = QGraphicsItem.mapFromItem(node, 0., 0.)
            dx = vec.x()
            dy = vec.y()
            force = 2.0*(dx*dx + dy*dy)
            if force > 0:
                xvel += (dx*150.0)/force
                yvel += (dy*150.0)/force

        # Now subtract all forces pulling items together
        weight = (len(self.edges) + 1)*10
        for edge in self.edges:
            if edge.source_node == self:
                vec = QGraphicsItem.mapFromItem(edge.dest_node, 0, 0)
            else:
                vec = QGraphicsItem.mapFromItem(edge.source_node, 0, 0)

            xvel -= vec.x()/weight
            yvel -= vec.y()/weight

        if abs(xvel) < 0.1 and abs(yvel) < 0.1:
            xvel = 0
            yvel = 0

        scene_rect = QGraphicsScene().sceneRect()
        self.__newpos = self.pos()
        self.__newpos.setX(min(max(self.__newpos.x(), scene_rect.left() + 10),
                               scene_rect.right() - 10))
        self.__newpos.setY(min(max(self.__newpos.y(), scene_rect.top() + 10),
                               scene_rect.bottom() - 10))

    def advance_position(self):
        if self.__newpos == self.pos():
            return False

        self.setPos(self.__newpos)
        return True

    def boundingRect(self):
        adjust = 2
        return QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.darkGray)
        painter.addEllipse(-7, -7, 20, 20)

        gradient = QGradient(-3, -3, 10)
        if option.state & QStyle.State_Sunken:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QColor(Qt.yellow).light(120))
            gradient.setColorAt(0, QColor(Qt.darkYellow).light(120))
        else:
            gradient.setColorAt(0, Qt.yellow)
            gradient.setColorAt(1, Qt.darkYellow)

        painter.setBrush(gradient)
        painter.setPen(QPen(Qt.black), 0)
        painter.drawEllipse(-10, -10, 20, 20)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()
            self.graph.itemMoved()

        return QGraphicsItem.itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        self.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        self.mouseReleaseEvent(event)
