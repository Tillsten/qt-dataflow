__author__ = 'Tillsten'

from qtdataflow.Qt import QtGui
from qtdataflow.Qt import QtCore


from view import SchemaView,  NodeView, PixmapNodeView
from model import Schema


class ToolBar(QtGui.QGraphicsView):
    """
    Toolbar which show the availeble nodes.
    """
    node_clicked = QtCore.Signal(object)

    def __init__(self, parent):
        super(ToolBar, self).__init__(parent)
        self.nodes = []
        self.scene = QtGui.QGraphicsScene()
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setScene(self.scene)
        self.setStyleSheet("background: transparent")
        self._bottom = 0
        self.setLayout(QtGui.QHBoxLayout())
        size_pol = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                     QtGui.QSizePolicy.Minimum)
        self.setSizePolicy(size_pol)

    def add_node(self, node):
        rep = node().get_toolbar_view()
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


class ChartWindow(QtGui.QWidget):
    def __init__(self, schema=None, parent=None):
        super(ChartWindow, self).__init__(parent)
        lay = QtGui.QHBoxLayout()
        self.setWindowTitle("qt-flowgraph")
        self.setLayout(lay)
        self.setMinimumSize(500, 300)
        self.tb = ToolBar(self)
        self.view = QtGui.QGraphicsView(self)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        self.schema = schema or Schema()
        self.sv = SchemaView(self.schema)
        self.view.setScene(self.sv)

        lay.addWidget(self.tb)
        lay.addWidget(self.view)

        self.tb.node_clicked.connect(self.schema.add_node)



class SchemaApp(QtGui.QMainWindow):
    def __init__(self):
        super(SchemaApp, self).__init__()
        cw = ChartWindow(self)
        self.setCentralWidget(cw)
        tb = self.addToolBar()
        save_action = QtGui.QAction('Save')






class SaveAction(QtGui.QAction):
    def __init__(self):

        super(SaveAction, self).__init__()
        self.setIconText(QtGui.QStyle.SP_DialogSaveButton)
        self.iconText('Save Schema')
