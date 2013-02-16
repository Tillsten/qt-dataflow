from PySide.QtGui import *
from PySide.QtCore import *

try:
    pyqtSignal = Signal
except NameError:
    pass


class SchemaIcon(QGraphicsPixmapItem):
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
        if self.node.accepts_input:
            term = QGraphicsEllipseItem(self)
            term.setRect(0, 0, 10, 10)
            pos = _get_left(self.boundingRect())
            pos += QPoint(-10, 0)
            term.setPos(pos)
            term.setAcceptedMouseButtons(1)
            print term.isActive()
            self.term_in = term

        if self.node.generates_output:
            term = QGraphicsEllipseItem(self)
            term.setRect(0, 0, 10, 10)
            pos = _get_right(self.boundingRect())
            pos += QPoint(0, 0)
            term.setPos(pos)
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
    def __init__(self, from_node, to_node):
        super(LinkLine, self).__init__()
        self.from_node = from_node
        self.to_node = to_node
        pen = QPen()
        pen.setWidth(3)

        self.setPen(pen)

    def paint(self, *args):
        start_pos = _get_right(self.from_node.sceneBoundingRect())
        end_pos = _get_left(self.to_node.sceneBoundingRect())
        path_rect = QRectF(start_pos, end_pos)
        path = QPainterPath(path_rect.topLeft())
        path.cubicTo(path_rect.topRight(),
                     path_rect.bottomLeft(),
                     path_rect.bottomRight())
        self.setPath(path)
        super(LinkLine, self).paint(*args)

def _get_right(rect):
    return QPoint(rect.right() + 5, rect.bottom() - rect.height() / 2.)

def _get_left(rect):
    return QPoint(rect.left() - 5, rect.bottom() - rect.height() / 2.)

def _get_bot(rect):
    return QPoint(rect.left() + rect.width() / 2., rect.bottom())

class SchemaNode(object):
    def __init__(self, schema):
        self.schema = schema
        self.node_type = 'BaseNode'
        self.accepts_input = False
        self.generates_output = False
        self.out_conn = []
        self.in_conn = []


class Schema(QObject):
    node_created = pyqtSignal(SchemaNode)
    node_deleted = pyqtSignal(SchemaNode)
    node_connected = pyqtSignal(SchemaNode)
    node_disconnected = pyqtSignal(SchemaNode)

    def __init__(self):
        super(Schema, self).__init__()
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)
        #Schema.node_connected()


class SchemaView(QGraphicsScene):
    def __init__(self, schema, *args):
        super(SchemaView, self).__init__(*args)
        self.schema = schema
        self.drawn_icons = []

    def draw_schema(self):
        for n in self.schema.nodes:
            if n not in self.drawn_icons:
                it = SchemaIcon(n)
                self.addItem(it)
                self.drawn_icons.append(it)

    def mousePressEvent(self, ev):
        super(SchemaView, self).mousePressEvent(ev)
        print self.itemAt(ev.scenePos())

    def mouseMoveEvent(self, ev):
        super(SchemaView, self).mouseMoveEvent(ev)
        print self.itemAt(ev.scenePos())

if __name__ == '__main__':

    app = QApplication([])
    sch = Schema()
    from nodes import DataGenNode, PlotNode
    d = DataGenNode(sch)
    p = PlotNode(sch)
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
