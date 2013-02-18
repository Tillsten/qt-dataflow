# -*- coding: utf-8 -*-
"""
Simple example. Has random generating Node, a filter node and a plotting node.
"""
from __future__ import print_function

try:
    from PyQt4.QtGui import *
except ImportError:
    from PySide.QtGui import *


from model import Node, Schema

import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
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

    def get(self):
        num = np.random.random(self.num_points) * (self.max - self.min) + self.min
        return num

    def show_widget(self):
        int, ok = QInputDialog.getInteger(None, 'Input Dialog',
                                          'Number of Points', self.num_points)
        if ok:
            self.num_points = int


class FilterNode(Node):
    """
    Applies a simple on the data filter.
    """
    def __init__(self):
        super(FilterNode, self).__init__()
        self.accepts_input = True
        self.generates_output = True
        self.node_type = 'Filter'
        self.icon_path = 'icons/onebit_31.png'
        self.rel = 1.

    def get(self):
        data = self.in_conn[0].get()
        m = data.mean()
        s = data.std()
        return np.where(np.abs(data - m) > self.rel * s, m, data)

    def show_widget(self):
        int, ok = QInputDialog.getDouble(None, 'Input Dialog',
                                          'Number of Points', self.rel)
        if ok:
            self.sel = int



class PlotNode(Node):
    """
    A test node to plot output from Datagen Node.
    """
    def __init__(self):
        super(PlotNode, self).__init__()
        self.accepts_input = True
        self.node_type = 'Plotter'
        self.icon_path = 'icons/onebit_16.png'

    def show_widget(self):
        data = [i.get() for i in self.in_conn]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for d in data:
            ax.plot(d)
        fig.show()

if __name__ == '__main__':
    from view import *
    from gui import ChartWindow
    app = QApplication([])
    cw = ChartWindow()
    cw.tb.add_node(FilterNode)
    cw.tb.add_node(DataGenNode)
    cw.tb.add_node(PlotNode)
    f = FilterNode()
    d = DataGenNode()
    # cw.schema.add_node(f)
    # cw.schema.add_node(d)
    # cw.schema.connect_nodes(d, f)
    cw.show()
    app.exec_()

