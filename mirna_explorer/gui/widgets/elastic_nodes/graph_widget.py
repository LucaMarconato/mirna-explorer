import math
from edge import Edge
from node import Node
from PySide2.QtGui import QPainter, QLinearGradient, QBrush
from PySide2.QtCore import Qt, QRectF, qrand
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene


class GraphWidget(QGraphicsView):

    def __init__(self, parent=None):
        super(GraphWidget, self).__init__()

        self.timer_id = 0

        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.setSceneRect(-200, -200, 400, 400)
        self.setScene(scene)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Elastic Nodes")

        node1 = Node(self)
        node2 = Node(self)
        node3 = Node(self)
        node4 = Node(self)
        self.center_node = Node(self)
        node6 = Node(self)
        node7 = Node(self)
        node8 = Node(self)
        node9 = Node(self)

        scene.addItem(node1)
        scene.addItem(node2)
        scene.addItem(node3)
        scene.addItem(node4)
        scene.addItem(self.center_node)
        scene.addItem(node6)
        scene.addItem(node7)
        scene.addItem(node8)
        scene.addItem(node9)
        scene.addItem(Edge(node1, node2))
        scene.addItem(Edge(node2, node3))
        scene.addItem(Edge(node2, self.center_node))
        scene.addItem(Edge(node3, node6))
        scene.addItem(Edge(node4, node1))
        scene.addItem(Edge(node4, self.center_node))
        scene.addItem(Edge(self.center_node, node6))
        scene.addItem(Edge(self.center_node, node8))
        scene.addItem(Edge(node6, node9))
        scene.addItem(Edge(node7, node4))
        scene.addItem(Edge(node8, node7))
        scene.addItem(Edge(node9, node8))

        node1.setPos(-50, -50)
        node2.setPos(0, -50)
        node3.setPos(50, -50)
        node4.setPos(-50, 0)
        self.center_node.setPos(0, 0)
        node6.setPos(50, 0)
        node7.setPos(-50, 50)
        node8.setPos(0, 50)
        node9.setPos(50, 50)

    def itemMoved(self):
        if not self.timer_id:
            self.timer_id = self.startTimer(1000/25)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.center_node.moveBy(0, -20)
        elif key == Qt.Key_Down:
            self.center_node.moveBy(0, 20)
        elif key == Qt.Key_Left:
            self.center_node.moveBy(-20, 0)
        elif key == Qt.Key_Right:
            self.center_node.moveBy(20, 0)
        elif key == Qt.Key_Plus:
            self.zoomIn()
        elif key == Qt.Key_Minus:
            self.zoomOut()
        elif key == Qt.Key_Space or key == Qt.Enter:
            self.shuffle()
        else:
            super(GraphWidget, self).keyPressEvent(event)

    def timerEvent(self, event):
        nodes = [item for item in self.scene().items() if isinstance(item, Node)]
        for node in nodes:
            node.calculate_forces()

        items_moved = False
        for node in nodes:
            if node.advance():
                items_moved = True

        if not items_moved:
            self.killTimer(self.timer_id)
            self.timer_id = 0

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta()/240.0))

    def drawBackground(self, painter, rect):
        scene_rect = self.sceneRect()

        # Shadow
        right_shadow = QRectF(scene_rect.right(), scene_rect.top() + 5, 5, scene_rect.height())
        bottom_shadow = QRectF(scene_rect.left() + 5, scene_rect.bottom(), scene_rect.width(), 5)

        if right_shadow.intersects(rect) or right_shadow.contains(rect):
            painter.fillRect(right_shadow, Qt.darkGray)
        if bottom_shadow.intersects(rect) or bottom_shadow.contains(rect):
            painter.fillRect(bottom_shadow, Qt.darkGray)

        # Fill
        gradient = QLinearGradient(scene_rect.topLeft(), scene_rect.bottomRight())
        gradient.setColorAt(0, Qt.white)
        gradient.setColorAt(1, Qt.lightGray)
        painter.fillRect(rect.intersected(scene_rect), QBrush(gradient))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(scene_rect)

        # Text
        text_rect = QRectF(scene_rect.left() + 4, scene_rect.top() + 4,
                           scene_rect.width() - 4, scene_rect.height() - 4)
        message = ("Click and drag the nodes around, and zoom with the "
                   "mouse wheel or the '+' and '-' keys")

        font = painter.font()
        font.setBold(True)
        font.setPointSize(14)
        painter.setFont(font)
        painter.setPen(Qt.lightGray)
        painter.drawText(text_rect.translated(2, 2), message)
        painter.setPen(Qt.black)
        painter.drawText(text_rect, message)

    def scaleView(self, scale_factor):
        factor = self.transform().scale(scale_factor, scale_factor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return

        self.scale(scale_factor, scale_factor)

    def shuffle(self):
        for item in self.scene().items():
            if isinstance(item, Node):
                item.setPos(-150 + qrand() % 300, -150 + qrand() % 300)

    def zoomIn(self):
        self.scaleView(1.2)

    def zoomOut(self):
        self.scaleView(1/1.2)
