from PySide2.QtCore import Qt, QRectF, QPointF, QLineF, qAbs
from PySide2.QtGui import QRadialGradient, QPainterPath, QPen, QColor, QBrush
from PySide2.QtWidgets import QGraphicsItem, QStyle


class Node(QGraphicsItem):

    def __init__(self, graph_widget):
        super(Node, self).__init__()

        self.Type = QGraphicsItem.UserType + 1
        self.edges = []
        self.__graph = graph_widget
        self.__newpos = QPointF()

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(-1)

    def type(self):
        return self.Type

    def add_edge(self, edge):
        self.edges.append(edge)
        edge.adjust()

    def calculate_forces(self):
        if not self.scene() or self.scene().mouseGrabberItem() is self:
            self.__newpos = self.pos()
            return

        # Sum up all forces pushing this item away.
        xvel = 0.0
        yvel = 0.0
        for item in self.scene().items():
            if not isinstance(item, Node):
                continue

            line = QLineF(self.mapFromItem(item, 0, 0), QPointF(0, 0))
            dx = line.dx()
            dy = line.dy()
            force = 2.0 * (dx * dx + dy * dy)
            if force > 0:
                xvel += (dx * 150.0)/force
                yvel += (dy * 150.0)/force

        # Now subtract all forces pulling items together.
        weight = (len(self.edges) + 1) * 10.0
        for edge in self.edges:
            if edge.source_node is self:
                pos = self.mapFromItem(edge.dest_node, 0, 0)
            else:
                pos = self.mapFromItem(edge.source_node, 0, 0)
            xvel += pos.x() / weight
            yvel += pos.y() / weight

        if qAbs(xvel) < 0.1 and qAbs(yvel) < 0.1:
            xvel = yvel = 0.0

        sceneRect = self.scene().sceneRect()
        self.__newpos = self.pos() + QPointF(xvel, yvel)
        self.__newpos.setX(min(max(self.__newpos.x(), sceneRect.left() + 10), sceneRect.right() - 10))
        self.__newpos.setY(min(max(self.__newpos.y(), sceneRect.top() + 10), sceneRect.bottom() - 10))

    def advance(self):
        if self.__newpos == self.pos():
            return False

        self.setPos(self.__newpos)
        return True

    def boundingRect(self):
        adjust = 2.
        return QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.darkGray)
        painter.drawEllipse(-7, -7, 20, 20)

        gradient = QRadialGradient(-3, -3, 10)
        if option.state & QStyle.State_Sunken:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QColor(Qt.yellow).light(120))
            gradient.setColorAt(0, QColor(Qt.darkYellow).light(120))
        else:
            gradient.setColorAt(0, Qt.yellow)
            gradient.setColorAt(1, Qt.darkYellow)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()
            self.__graph.itemMoved()

        return super(Node, self).itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(Node, self).mouseReleaseEvent(event)
