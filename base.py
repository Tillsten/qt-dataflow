from PyQt4.QtGui import *
from PyQt4.QtCore import *

try:
    pyqtSignal = Signal
except NameError:
    pass




class SchemaIcon(QGraphicsPixmapItem):
    """
    Class responisble for drawing and interaction of a Node.
    """
    def __init__(self, node, *args):
        super(SchemaIcon, self).__init__(*args)
        self.setAcceptHoverEvents(True)
        pixmap = QPixmap('flop.png')
        flags = [QGraphicsItem.ItemIsMovable,
                 QGraphicsItem.ItemIsSelectable]
        for f in flags:
            self.setFlag(f)


        self.node = node
        self.setPixmap(pixmap)
        self.setScale(1.)
        self.setGraphicsEffect(None)
        self.add_label(node.node_type)
        self.add_terminals()

    def add_terminals(self):
        """
        Adds terminals to the item.
        """
        if self.node.accepts_input:
            term = QGraphicsEllipseItem(self)
            term.setRect(0, 0, 10, 10)
            pos = _get_left(self.boundingRect())
            pos += QPointF(-15., 0.)
            term.setPos(pos)
            term._con = 'in'
            self.term_in = term

        if self.node.generates_output:
            term = QGraphicsEllipseItem(self)
            term.setRect(0, 0, 10, 10)
            pos = _get_right(self.boundingRect())
            pos += QPointF(5., 0.)
            term.setPos(pos)
            term._con = 'out'
            self.term_out = term

    def add_label(self, text):
        t = QGraphicsSimpleTextItem(text, self)
        t.setPos(self.boundingRect().bottomLeft())

    def hoverEnterEvent(self, ev):
        self.setGraphicsEffect(QGraphicsColorizeEffect())
        self.update()

    def hoverLeaveEvent(self, ev):
        self.setGraphicsEffect(None)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.node.show_widget()


class LinkLine(QGraphicsPathItem):
    """
    Visual representation for a connection between nodes.
    """
    def __init__(self, from_node, to_node):
        super(LinkLine, self).__init__()
        self.from_node = from_node
        self.to_node = to_node
        pen = QPen()
        pen.setWidth(3)
        self.setPen(pen)

    def paint(self, *args):
        start_pos = self.from_node.sceneBoundingRect().center()
        end_pos = self.to_node.sceneBoundingRect().center()
        path_rect = QRectF(start_pos, end_pos)
        path = QPainterPath(path_rect.topLeft())
        path.cubicTo(path_rect.topRight(),
                     path_rect.bottomLeft(),
                     path_rect.bottomRight())
        self.setPath(path)
        super(LinkLine, self).paint(*args)

# Simple helper funcs to get points of a QRectF
def _get_right(rect):
    return QPointF(rect.right(), rect.bottom() - rect.height() / 2.)

def _get_left(rect):
    return QPointF(rect.left(), rect.bottom() - rect.height() / 2.)

def _get_bot(rect):
    return QPointF(rect.left() + rect.width() / 2., rect.bottom())


class SchemaNode(object):
    """
    Logical Representation of a node.
    """
    def __init__(self, schema):
        self.schema = schema
        self.node_type = 'BaseNode'
        self.accepts_input = False
        self.generates_output = False
        self.out_conn = []
        self.in_conn = []


class Schema(QObject):
    """
    Model a Schema, which includes all Nodes and connections.
    """
    node_created = pyqtSignal(SchemaNode)
    node_deleted = pyqtSignal(SchemaNode)
    nodes_connected = pyqtSignal(list)
    node_disconnected = pyqtSignal(SchemaNode)

    def __init__(self):
        super(Schema, self).__init__()
        self.nodes = []
        self.connections = []

    def add_node(self, node):
        self.nodes.append(node)
        #Schema.node_connected()

    def connect_nodes(self, out_node, in_node):
        out_node.out_conn.append(in_node)
        in_node.in_conn.append(out_node)
        self.connections.append((out_node, in_node))
        self.nodes_connected.emit([out_node, in_node])

class SchemaView(QGraphicsScene):
    """
    The view of a Schema, manges GUI interaction.
    """
    def __init__(self, schema, *args):
        super(SchemaView, self).__init__(*args)
        self.schema = schema
        self.drawn_icons = []
        self._pressed = None
        self.nodes_drawn = {}
        self.schema.nodes_connected.connect(self.add_link)

    def draw_schema(self):
        for n in self.schema.nodes:
            if n not in self.nodes_drawn:
                it = SchemaIcon(n)
                self.addItem(it)
                self.nodes_drawn[n] = it


    def add_link(self, l):
        out_node, in_node = l
        in_it = self.nodes_drawn[in_node]
        out_it = self.nodes_drawn[out_node]

        ll = LinkLine(in_it.term_in, out_it.term_out)
        self.addItem(ll)

    def mousePressEvent(self, ev):
        super(SchemaView, self).mousePressEvent(ev)
        it = self.itemAt(ev.scenePos())

        if hasattr(it, '_con'):
            self._pressed = True
            self._start_con = it._con
            self._start_node = it.parentItem().node

    def mouseReleaseEvent(self, ev):
        super(SchemaView, self).mouseReleaseEvent(ev)
        if self._pressed:
            it = self.itemAt(ev.scenePos())
            if hasattr(it, '_con'):
                if it._con != self._start_con:
                    if it._con == 'in':
                        in_node = it.parentItem().node
                        self.schema.connect_nodes(self._start_node, in_node)
                    else:
                        out_node = it.parentItem().node
                        self.schema.connect_nodes(out_node, self._start_node)
        self._pressed = False
        self._start_node = None


    def mouseMoveEvent(self, ev):
        super(SchemaView, self).mouseMoveEvent(ev)

        #print self.itemAt(ev.scenePos())

if __name__ == '__main__':

    app = QApplication([])
    sch = Schema()
    from nodes import DataGenNode, PlotNode, FilterNode
    d = DataGenNode(sch)
    p = PlotNode(sch)
    f = FilterNode(sch)
    sch.add_node(f)
    sch.add_node(d)
    sch.add_node(p)
    sv = SchemaView(sch)
    vi = QGraphicsView()
    vi.setScene(sv)
    vi.setRenderHint(QPainter.Antialiasing)
    vi.setRenderHint(QPainter.HighQualityAntialiasing)
    sv.draw_schema()
    # it = SchemaIcon()
    # it.setPos(0., 200.)
    # it2 = SchemaIcon()
    # sv.addItem(it)
    # sv.addItem(it2)
    # p = LinkLine(it, it2)
    # sv.addItem(p)
    #
    vi.show()
    app.exec_()
