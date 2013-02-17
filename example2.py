__author__ = 'Tillsten'

from matplotlib.backend_bases import FigureCanvasBase
from view import *
from model import Node, Schema
from PyQt4.QtGui  import *

class SpinBoxNode(Node):
    def __init__(self):
        super(SpinBoxNode, self).__init__()
        self.node_type = 'SpinBoxNode'
        self.generates_output = True
        self.sb = QSpinBox()
        self.sb.setGeometry(0,0,50,25)
        self.sb.changeEvent = self.signal_change()

    def get_widget(self):
        return self.sb

    def get(self):
        return self.sb.value()

    def signal_change(self):
        for n in self.out_conn:
            n.update()


class SumLabelNode(Node):
    def __init__(self):
        super(SumLabelNode, self).__init__()
        self.node_type = 'Sum Label'
        self.accepts_input = True
        self.lbl = QLabel()

    def get_widget(self):
        return self.lbl

    def update(self):
        s = sum((n.get() for n in self.in_conn))
        self.lbl.setText(str(s))

if __name__ == '__main__':
    app = QApplication([])
    sch = Schema()
    sv = SchemaView(sch)
    sv.myNodeView = WidgetNodeView
    n = SpinBoxNode()
    #n2 = SumLabelNode()
    sch.add_node(n)
    #sch.add_node(n2)
    gv = QGraphicsView(sv)
    gv.show()

    app.exec_()