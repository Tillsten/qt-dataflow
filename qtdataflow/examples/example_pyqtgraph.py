import pyqtgraph

__author__ = 'Tillsten'


from pyqtgraph import PlotItem
from qtdataflow.model import Node, Schema
from qtdataflow.view import PixmapNodeView, NodeView
from qtdataflow.qtpy import QtCore, QtGui

class PlotOnCanvasItem(NodeView, PlotItem):
    def __init__(self, Node):
        PlotItem.__init__(self)
        self.setMinimumSize(300, 300)
        NodeView.__init__(self, Node)


class PlotOnCanvasNode(Node):
    def __init__(self):
        super(PlotOnCanvasNode, self).__init__()
        self.node_type = 'pyqtgraph-Plotter'
        self.accepts_input = True

    def get_view(self):
        p = PlotOnCanvasItem(self)
        self.plot = p.plot()
        self.plot.setPen(pyqtgraph.mkPen('r', lw=3))
        return p

    def get_toolbar_view(self):
        self.icon_path = 'icons/onebit_16.png'
        p = PixmapNodeView(self)
        return p

    def show_widget(self):
        pass

    def update(self):
        self.plot.setData(self.in_conn[0].get())

    def new_connection_out(self, node):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50.)


if __name__ == '__main__':
    from example import DataGenNode
    from qtdataflow.gui import ChartWindow
    from qtdataflow.qtpy.QtGui import  QApplication
    app = QApplication([])
    cw = ChartWindow()
    cw.tb.add_node(PlotOnCanvasNode)
    cw.tb.add_node(DataGenNode)
    cw.show()
    app.exec_()
