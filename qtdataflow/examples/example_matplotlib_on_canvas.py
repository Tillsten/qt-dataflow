from __future__ import print_function
from qtdataflow.model import Node, Schema
from qtdataflow.view import PixmapNodeView
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pylab as plt


class DataGenNode(Node):
    """
    A test node which outputs a random number. Widget allow to set the number.
    """
    def __init__(self):
        super(DataGenNode, self).__init__()
        self.node_type = 'Random Array'
        self.icon_path = 'icons/onebit_11.png'
        self.min = 0
        self.max = 1
        self.num_points = 100
        self.generates_output = True

    def get_view(self):
        return PixmapNodeView(self)

    def get(self):
        num = np.random.random(self.num_points) * (self.max - self.min) + self.min
        return num

    def show_widget(self):
        int, ok = Qt.QtGui.QInputDialog.getInteger(None, 'Input Dialog',
                                          'Number of Points', self.num_points)
        if ok:
            self.num_points = int


def make_plot(y):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.set_size_inches(4, 4)
    ax.plot(y)
    fig.savefig('tmp.png', dpi=75)

class MatplotlibNodeView(PixmapNodeView):
    def __init__(self, node):
        super(MatplotlibNodeView, self).__init__(node)
        make_plot([0])
        self.update_view()

    def update_view(self):
        self.setPixmap('tmp.png')
        self.layout_nodes()
        import os
        os.remove('tmp.png')
        self.update()

class MatplotlibNode(Node):
    def __init__(self):
        super(MatplotlibNode, self).__init__()
        self.node_type = 'Matplotlib Image'
        self.accepts_input = True
        self.generates_output = False
        self.icon_path = 'icons/onebit_16.png'

    def get_view(self):
        self.view = MatplotlibNodeView(self)
        return self.view

    def get_toolbar_view(self):
        return PixmapNodeView(self)

    def show_widget(self):
        a = self.in_conn[0].get()
        make_plot(a)
        self.view.update_view()


if __name__ == '__main__':
    from qtdataflow.gui import ChartWindow
    from qtdataflow import qtpy as Qt
    app = Qt.QtGui.QApplication([])
    cw = ChartWindow()
    cw.tb.add_node(DataGenNode)
    cw.tb.add_node(MatplotlibNode)
    cw.show()
    app.exec_()