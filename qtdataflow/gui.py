__author__ = 'Tillsten'
# try:
#     from PyQt4.QtGui import *
#     from PyQt4.QtCore import pyqtSignal
#     Signal = pyqtSignal
#except ImportError:
from PySide.QtGui import *
from PySide.QtCore import Signal

from view import SchemaView,  NodeView, PixmapNodeView
from model import Schema


class ToolBar(QGraphicsView):
    """
    Toolbar which show the availeble nodes.
    """
    node_clicked = Signal(object)

    def __init__(self, parent):
        super(ToolBar, self).__init__(parent)
        self.nodes = []
        self.scene = QGraphicsScene()
        self.setRenderHint(QPainter.Antialiasing)
        self.setScene(self.scene)
        self.setStyleSheet("background: transparent")
        self._bottom = 0
        self.setLayout(QHBoxLayout())
        size_pol = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_pol)

    def add_node(self, node):
        rep = PixmapNodeView(node())
        self.scene.addItem(rep)
        rep.setPos(0., self._bottom)
        rep.setFlag(rep.ItemIsMovable, False)
        rep.setFlag(rep.ItemIsSelectable, False)
        rep.setHandlesChildEvents(True)
        rect = (rep.childrenBoundingRect() | rep.boundingRect())
        self._bottom += rect.height() + 5
        self.setSceneRect(self.scene.itemsBoundingRect().adjusted(-3, 0, 0, 0))

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
        self.setWindowTitle("qt-flowgraph")
        self.setLayout(lay)
        self.setMinimumSize(500, 300)
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



class SchemaApp(QMainWindow):
    def __init__(self):
        super(SchemaApp, self).__init__()
        cw = ChartWindow(self)
        self.setCentralWidget(cw)
        tb = self.addToolBar()
        save_action = QAction('Save')






class SaveAction(QAction):
    def __init__(self):

        super(SaveAction, self).__init__()
        self.setIconText(QStyle.SP_DialogSaveButton)
        self.iconText('Save Schema')
