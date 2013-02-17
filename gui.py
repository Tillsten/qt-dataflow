__author__ = 'Tillsten'

from PySide.QtGui import *
from PySide.QtCore import Signal
from base import SchemaView, Schema, NodeView


class ToolBar(QGraphicsView):
    """
    Toolbar which show the availeble nodes.
    """
    node_clicked = Signal(object)
    def __init__(self, parent):
        super(ToolBar, self).__init__(parent)
        self.nodes = []
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self._bottom = 0
        self.setLayout(QHBoxLayout())
        size_pol = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_pol)

    def add_node(self, node):
        rep = NodeView(node())
        self.scene.addItem(rep)
        rep.setPos(0., self._bottom)
        rep.setFlag(rep.ItemIsMovable, False)
        rep.setFlag(rep.ItemIsSelectable, False)
        rep.setHandlesChildEvents(True)
        rect = (rep.childrenBoundingRect() | rep.boundingRect())
        self._bottom += rect.height() + 5

    def mousePressEvent(self, ev):
        super(ToolBar, self).mouseReleaseEvent(ev)
        item = self.itemAt(ev.pos())
        if item is not None:
            if not hasattr(item, 'node'):
                item = item.parentItem()
            t = type(item.node)
            self.node_clicked.emit(t())


class ChartWindow(QWidget):
    def __init__(self, schema=None, parent=None):
        super(ChartWindow, self).__init__(parent)
        lay = QHBoxLayout()
        self.setLayout(lay)
        self.tb = ToolBar(self)
        self.view = QGraphicsView(self)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.HighQualityAntialiasing)
        self.schema = schema or Schema()
        self.sv = SchemaView(self.schema)
        self.view.setScene(self.sv)

        lay.addWidget(self.tb)
        lay.addWidget(self.view)
        self.tb.node_clicked.connect(self.schema.add_node)






