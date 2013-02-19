__author__ = 'Tillsten'


from pyqtgraph import PlotItem
from qtdataflow.model import Node, Schema
from qtdataflow.view import PixmapNodeView, NodeView
import numpy as np
import matplotlib

matplotlib.use('Qt4Agg')
import matplotlib.pylab as plt

class PlotOnCanvasItem(NodeView, PlotItem):
    def __init__(self, Node):
        PlotItem.__init__(self)
        NodeView.__init__(self, Node)


class PlotOnCanvasNode(Node):
    def __init__(self):
        super(PlotOnCanvasNode, self).__init__()


    def get_view(self):
        return PlotOnCanvasItem(self)




if __name__ == '__main__':
    from qtdataflow.gui import ChartWindow
    from PySide.QtGui import  QApplication
    app = QApplication([])
    cw = ChartWindow()
    cw.tb.add_node(PlotOnCanvasNode)
    cw.show()
    app.exec_()
