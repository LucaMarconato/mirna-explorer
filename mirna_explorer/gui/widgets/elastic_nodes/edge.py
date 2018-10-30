import math
from PySide2.QtGui import QPolygonF, QPen
from PySide2.QtCore import Qt, QLineF, QPointF, QRectF, QSizeF
from PySide2.QtWidgets import QGraphicsItem


class Edge(QGraphicsItem):

    def __init__(self, source_node, dest_node):
        super(Edge, self).__init__()

        self.arrow_size = 10
        self.Type = QGraphicsItem.UserType + 2
        self.setAcceptedMouseButtons(0)
        self.source_node = source_node
        self.dest_node = dest_node
        self.source_node.add_edge(self)
        self.dest_node.add_edge(self)
        self.adjust()

    def adjust(self):
        if not self.source_node or not self.dest_node:
            return None

        line = QLineF(self.mapFromItem(self.source_node, 0., 0.),
                     self.mapFromItem(self.dest_node, 0., 0.))
        length = line.length()

        self.prepareGeometryChange()

        if length > 20.0:
            edge_offset = QPointF((line.dx()*10/length,
                                      (line.dy()*10)/length))
            self.sourcePoint = line.p1() + edge_offset
            self.destPoint = line.p2() - edge_offset
        else:
            self.sourcePoint = line.p1()
            self.destPoint = line.p1()

    def boundingRect(self):
        if not self.source_node or not self.dest_node:
            return QRectF()

        pen_width = 1
        extra = (pen_width + self.arrow_size) / 2.0

        x = self.destPoint.x() - self.sourcePoint.x()
        y = self.destPoint.y() - self.sourcePoint.y()

        rect = QRectF(self.sourcePoint, QSizeF(x, y))
        return rect.normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source_node or not self.dest_node:
            return None

        line = QLineF(self.sourcePoint, self.destPoint)
        if math.isclose(line.length(), 0.0, rel_tol=1e-5):
            return None

        # Draw the line itself
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine,
                                Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(line)

        # Draw the arrows
        angle = math.atan2(-line.dy(), line.dx())

        plus, minus = angle + math.pi, angle - math.pi

        p1 = QPointF(math.sin(plus/3)*self.arrow_size,
                     math.cos(plus/3)*self.arrow_size)

        p2 = QPointF(math.sin(plus - math.pi/3)*self.arrow_size,
                     math.cos(plus - math.pi/3)*self.arrow_size)

        p3 = QPointF(math.sin(minus/3)*self.arrow_size,
                     math.cos(minus/3)*self.arrow_size)

        p4 = QPointF(math.sin(minus + math.pi/3)*self.arrow_size,
                     math.cos(minus + math.pi/3)*self.arrow_size)

        source_arrow_p1 = self.sourcePoint + p1
        source_arrow_p2 = self.sourcePoint + p2
        source_arrow_p3 = self.sourcePoint + p3
        source_arrow_p4 = self.sourcePoint + p4

        painter.setBrush(Qt.black)

        polygon = QPolygonF()
        polygon << source_arrow_p1 << source_arrow_p2
        polygon << source_arrow_p3 << source_arrow_p4
        painter.drawPolygon(polygon)
