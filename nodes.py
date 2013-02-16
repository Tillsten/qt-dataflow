# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 00:40:58 2013

@author: UlMi
"""
from __future__ import print_function
from PyQt4.QtGui import *
from base import SchemaNode

import numpy as np
import matplotlib.pylab as plt
import guidata.dataset.datatypes as dt
import guidata.dataset.dataitems as di

class DataGenNode(SchemaNode):
    """
    A test node which outputs a random number. Widget allow to set the number.
    """
    def __init__(self, schema):
        super(DataGenNode, self).__init__(schema)
        self.node_type = 'DataGen'
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


class PlotNode(SchemaNode):
    """
    A test node to plot output from Datagen Node.
    """
    def __init__(self, schema):
        super(PlotNode, self).__init__(schema)
        self.accepts_input = True
        self.node_type = 'PlotNode'

    def show_widget(self):
        if len(self.in_conn)!= 1:
            print('Wrong number of inputs')
            return

        data = self.in_conn[0].get()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(data)
        fig.show()



if __name__ == '__main__':
    app = QApplication([])
    w = DataW()

    app.exec_()