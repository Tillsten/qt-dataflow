__author__ = 'Tillsten'
import numpy as np
from example import DataGenNode


class VarDataGenNode(DataGenNode):

    def __init__(self):
        super(VarDataGenNode, self).__init__()
        self.accepts_input = True

    def get(self):
        if len(self.in_conn) == 1:
            m = self.in_conn[0].get()
        else:
            m = 1
        return np.random.randn(self.num_points) * m


if __name__ == '__main__':
    from qtdataflow.gui import ChartWindow
    from qtdataflow.Qt import QtGui

    from example_matplotlib_on_canvas import MatplotlibNode
    from example_widget import SpinBoxNode
    from example_pyqtgraph import PlotOnCanvasNode

    app = QtGui.QApplication([])
    cw = ChartWindow()
    cw.tb.add_node(PlotOnCanvasNode)
    cw.tb.add_node(VarDataGenNode)
    cw.tb.add_node(MatplotlibNode)
    cw.tb.add_node(SpinBoxNode)
    cw.show()
    app.exec_()
