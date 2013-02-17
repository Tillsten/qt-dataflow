# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 00:40:58 2013

@author: UlMi
"""
from __future__ import print_function
from PySide.QtGui import *
from base import Node

import numpy as np
import matplotlib.pylab as plt
import guidata.dataset.datatypes as dt
import guidata.dataset.dataitems as di

class DataGenNode(Node):
    """
    A test node which outputs a random number. Widget allow to set the number.
    """
    def __init__(self):
        super(DataGenNode, self).__init__()
        self.node_type = 'Random Array'
        self.min = 0
        self.max = 1
        self.size = 100
        self.generates_output = True

    def get(self):
        num = np.random.random(self.size) * (self.max - self.min) + self.min
        return num

    def show_widget(self):
        w = DataW()
        w.edit()
        self.min = w.mini
        self.max = w.maxi
        self.size = w.size


class FilterNode(Node):
    """
    Applies a simple on the data filter.
    """
    def __init__(self):
        super(FilterNode, self).__init__()
        self.accepts_input = True
        self.generates_output = True
        self.node_type = 'Filter'

    def get(self):
        data = self.in_conn[0].get()
        m = data.mean()
        s = data.std()
        return np.where(np.abs(data - m) > s, m, data)

    def show_widget(selfs):
        pass




#class DataGenWidget(QWidget):
#    """
#    Widget for DataGenNode
#    """
#    def __init__(self):
#        super(DataGenWidget, self).__init__()
#        lay = QVBoxLayout()
#        self.setLayout(lay)
#        tb_min = QSpinBox()
#        tb_max = QSpinBox()
#        tb_size = QLineEdit('Size')
#        for i in [tb_min, tb_max, tb_size]:
#            lay.addWidget(i)


class DataW(dt.DataSet):
    mini = di.FloatItem('Min', 0.)
    maxi = di.FloatItem('Max.', 1.)
    size = di.IntItem('Size', 50.)


class PlotNode(Node):
    """
    A test node to plot output from Datagen Node.
    """
    def __init__(self):
        super(PlotNode, self).__init__()
        self.accepts_input = True
        self.node_type = 'Plotter'

    def show_widget(self):
        data = [i.get() for i in self.in_conn]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for d in data:
            ax.plot(d)
        fig.show()



if __name__ == '__main__':
    from base import *
    from gui import ChartWindow
    app = QApplication([])
    app.setStyle('macos')
    cw = ChartWindow()
    cw.tb.add_node(FilterNode)
    cw.tb.add_node(DataGenNode)
    cw.tb.add_node(PlotNode)
    f = FilterNode()
    d = DataGenNode()
    cw.schema.add_node(f)
    cw.schema.add_node(d)
    cw.schema.connect_nodes(d, f)
    cw.show()
    app.exec_()

