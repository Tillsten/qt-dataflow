from PySide.QtGui import *
from PySide.QtCore import *

try:
    pyqtSignal = Signal
except NameError:
    pass

class TerminalItem(QGraphicsEllipseItem):
    pass


class NodeView(QGraphicsPixmapItem):
    """
    Class responsible for drawing and interaction of a Node.
    """
    def __init__(self, node, *args):
        super(NodeView, self).__init__(*args)
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
            term = TerminalItem(self)
            term.setRect(0, 0, 10, 10)
            pos = _get_left(self.boundingRect())
            pos += QPointF(-15., 0.)
            term.setPos(pos)
            term._con = 'in'
            self.term_in = term

        if self.node.generates_output:
            term = TerminalItem(self)
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
    Like Link line, but only one pos is a node.
    """
    def __init__(self):
        super(LinkLine, self).__init__()
        self.pen = QPen()
        self.pen.setWidth(3)
        self.setPen(self.pen)

    def paint(self, *args):
        start_pos = self.end_pos
        end_pos = self.start_pos
        path_rect = QRectF(start_pos, end_pos)
        path = QPainterPath(path_rect.topLeft())
        path.cubicTo(path_rect.topRight(),
                     path_rect.bottomLeft(),
                     path_rect.bottomRight())
        self.setPath(path)
        super(LinkLine, self).paint(*args)


class LinkNodesLine(LinkLine):
    """
    Visual representation for a connection between nodes.
    """
    def __init__(self, from_node, to_node):
        super(LinkNodesLine, self).__init__()
        self.from_node = from_node
        self.to_node = to_node
        self.setFlag(self.ItemIsSelectable)


    def paint(self, *args):
        self.start_pos = self.from_node.sceneBoundingRect().center()
        self.end_pos = self.to_node.sceneBoundingRect().center()
        super(LinkNodesLine, self).paint(*args)


class TempLinkLine(LinkLine):
    """
    Line from node to end_pos
    """
    def __init__(self, from_node, pos):
        super(TempLinkLine, self).__init__()
        self.from_node = from_node
        self.end_pos = pos

    def paint(self, *args):
        self.start_pos = self.from_node.sceneBoundingRect().center()
        super(TempLinkLine, self).paint(*args)


# Simple helper funcs to get points of a QRectF
def _get_right(rect):
    return QPointF(rect.right(), rect.bottom() - rect.height() / 2.)


def _get_left(rect):
    return QPointF(rect.left(), rect.bottom() - rect.height() / 2.)


def _get_bot(rect):
    return QPointF(rect.left() + rect.width() / 2., rect.bottom())


class Node(object):
    """
    Logical Representation of a node.
    """
    def __init__(self):
        #self.schema = schema
        self.node_type = 'BaseNode'
        self.accepts_input = False
        self.generates_output = False
        self.out_conn = []
        self.in_conn = []

    def accept_type(self, node):
        return True


class Schema(QObject):
    """
    Model a Schema, which includes all Nodes and connections.
    """
    node_created = pyqtSignal(Node)
    node_deleted = pyqtSignal(Node)
    nodes_connected = pyqtSignal(list)
    nodes_disconnected = pyqtSignal(list)

    def __init__(self):
        super(Schema, self).__init__()
        self.nodes = []
        self.connections = []

    def add_node(self, node):
        self.nodes.append(node)
        self.node_created.emit(Node)

    def delete_node(self, node):
        to_delete = [(o, i) for (o, i) in self.connections
                     if o == node or i == node]

        for o, i in to_delete:
            self.disconnect_nodes(o, i)

        self.nodes.remove(node)
        self.node_deleted.emit(node)

    def connect_nodes(self, out_node, in_node):
        out_node.out_conn.append(in_node)
        in_node.in_conn.append(out_node)
        self.connections.append((out_node, in_node))
        self.nodes_connected.emit([out_node, in_node])

    def disconnect_nodes(self, out_node, in_node):
        self.nodes_disconnected.emit([out_node, in_node])
        out_node.out_conn.remove(in_node)
        in_node.in_conn.remove(out_node)
        self.connections.remove((out_node, in_node))


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
        self.connections_drawn = {}
        self.connect_to_schema_sig()

    def connect_to_schema_sig(self):
        self.schema.node_created.connect(self.draw_schema)
        self.schema.nodes_connected.connect(self.add_link)
        self.schema.node_deleted.connect(self.remove_node)
        self.schema.nodes_disconnected.connect(self.remove_link)

    def draw_schema(self):
        """
        Draw Nodes
        """
        i = 0
        for n in self.schema.nodes:
            if n not in self.nodes_drawn:
                it = NodeView(n)
                self.addItem(it)
                self.nodes_drawn[n] = it
                it.setPos(it.pos()+ i * QPointF(100., 0.))
                i += 1

    def add_link(self, nodes):
        """
        Adds connection between nodes.
        """
        out_node, in_node = nodes
        in_it = self.nodes_drawn[in_node]
        out_it = self.nodes_drawn[out_node]

        ll = LinkNodesLine(out_it.term_out, in_it.term_in)
        self.addItem(ll)
        self.connections_drawn[(out_it.node, in_it.node)] = ll

    def remove_link(self, nodes):
        """Remove connection from view"""
        node_out, node_in = nodes
        ll = self.connections_drawn.pop((node_out, node_in))
        self.removeItem(ll)

    def remove_node(self, node):
        """Remove node from view"""
        self.removeItem(self.nodes_drawn[node])
        self.nodes_drawn[node] = None

    def mousePressEvent(self, ev):
        super(SchemaView, self).mousePressEvent(ev)
        it = self.itemAt(ev.scenePos())
        #Check if connection is started
        if hasattr(it, '_con'):
            self.temp_ll = TempLinkLine(it, ev.scenePos())
            self.addItem(self.temp_ll)
            self._pressed = True
            self._start_con = it._con
            self._start_node = it.parentItem().node

    def mouseMoveEvent(self, ev):
        #While connectiong, draw temp line
        super(SchemaView, self).mouseMoveEvent(ev)
        if self._pressed:
            self.temp_ll.end_pos = ev.scenePos()
            self.temp_ll.update()

    def mouseReleaseEvent(self, ev):
        super(SchemaView, self).mouseReleaseEvent(ev)
        #If connecting, check if endpoint is ok and add connection.
        if self._pressed:
            it = self.items(ev.scenePos())
            it = [i for i in it if hasattr(i, '_con')][0]
            if hasattr(it, '_con'):
                if it._con != self._start_con:
                    if it._con == 'in':
                        in_node = it.parentItem().node
                        self.schema.connect_nodes(self._start_node, in_node)
                    else:
                        out_node = it.parentItem().node
                        self.schema.connect_nodes(out_node, self._start_node)
            self.removeItem(self.temp_ll)
        self._pressed = False
        self._start_node = None

    def keyPressEvent(self, ev):
        super(SchemaView, self).keyPressEvent(ev)
        # Delte canvas item
        if ev.key() == Qt.Key_Delete and self.selectedItems() != []:
            for it in self.selectedItems():
                #Delete connections
                if it in self.connections_drawn.values():
                    self.schema.disconnect_nodes(it.from_node.parentItem().node,
                                                 it.to_node.parentItem().node)
                #Delete Nodes
                if it in self.nodes_drawn.values():
                    self.schema.delete_node(it.node)

