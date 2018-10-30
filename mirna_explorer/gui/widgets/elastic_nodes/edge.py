import math
from PySide2.QtGui import QPolygonF, QPen
from PySide2.QtCore import Qt, QLineF, QPointF, QRectF, QSizeF
from PySide2.QtWidgets import QGraphicsItem


class Edge(QGraphicsItem):

    def __init__(self, source_node, dest_node):
        super(Edge, self).__init__()

        self.Type = QGraphicsItem.UserType + 2
        self.setAcceptedMouseButtons(Qt.NoButton)

        self.arrow_size = 10.0
        self.source_pt = QPointF()
        self.dest_pt = QPointF()

        self.source_node = source_node
        self.dest_node = dest_node
        self.source_node.add_edge(self)
        self.dest_node.add_edge(self)
        self.adjust()

    def type(self):
        return self.Type

    def adjust(self):
        if not self.source_node or not self.dest_node:
            return

        line = QLineF(self.mapFromItem(self.source_node, 0., 0.),
                      self.mapFromItem(self.dest_node, 0., 0.))
        length = line.length()

        self.prepareGeometryChange()

        if length > 20.0:
            edge_offset = QPointF(line.dx()*10/length, (line.dy()*10)/length)
            self.source_pt = line.p1() + edge_offset
            self.dest_pt = line.p2() - edge_offset
        else:
            self.source_pt = line.p1()
            self.dest_pt = line.p1()

    def boundingRect(self):
        if not self.source_node or not self.dest_node:
            return QRectF()

        pen_width = 1.0
        extra = (pen_width + self.arrow_size) / 2.0

        x = self.dest_pt.x() - self.source_pt.x()
        y = self.dest_pt.y() - self.source_pt.y()
        rect = QRectF(self.source_pt, QSizeF(x, y))

        return rect.normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source_node or not self.dest_node:
            return

        line = QLineF(self.source_pt, self.dest_pt)
        if math.isclose(line.length(), 0.0, rel_tol=1e-1):
            return

        # Draw the line itself
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(line)

        # Draw the arrows
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = math.pi*2 - angle

        sourceArrowP1 = self.source_pt + QPointF(math.sin(angle + math.pi/3) * self.arrow_size,
                                                 math.cos(angle + math.pi/3) * self.arrow_size)
        sourceArrowP2 = self.source_pt + QPointF(math.sin(angle + math.pi - math.pi/3) * self.arrow_size,
                                                 math.cos(angle + math.pi - math.pi/3) * self.arrow_size)
        destArrowP1 = self.dest_pt + QPointF(math.sin(angle - math.pi/3) * self.arrow_size,
                                             math.cos(angle - math.pi/3) * self.arrow_size)
        destArrowP2 = self.dest_pt + QPointF(math.sin(angle - math.pi + math.pi/3) * self.arrow_size,
                                             math.cos(angle - math.pi + math.pi/3) * self.arrow_size)

        painter.setBrush(Qt.black)
        painter.drawPolygon(QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        painter.drawPolygon(QPolygonF([line.p2(), destArrowP1, destArrowP2]))
