__author__ = 'Tillsten'

from PySide.QtGui import *

from base import SchemaView, Schema, NodeView


class ToolBar(QGraphicsView):
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
        rep = NodeView(node(None))
        self.scene.addItem(rep)
        rep.setPos(0., self._bottom)
        rep.setFlag(rep.ItemIsMovable, False)
        rect = (rep.childrenBoundingRect()|rep.boundingRect())
        self._bottom += rect.height() + 5

class ChartWindow(QWidget):
    def __init__(self, schema=None, parent=None):
        super(ChartWindow, self).__init__(parent)
        lay = QHBoxLayout()
        self.setLayout(lay)
        self.tb = ToolBar(self)
        self.gv = QGraphicsView(self)
        self.schema = schema or Schema()
        self.sv = SchemaView(self.schema)
        self.gv.setScene(self.sv)
        lay.addWidget(self.tb)
        lay.addWidget(self.gv)



if __name__ == '__main__':
    from exampleNodes import *

    app = QApplication([])
    cw = ChartWindow()
    cw.tb.add_node(FilterNode)
    cw.tb.add_node(DataGenNode)
    cw.tb.add_node(PlotNode)
    cw.show()
    app.exec_()





