from __future__ import print_function
from qtdataflow.Qt import QtCore, QtGui
QRectF = QtCore.QRectF
QPointF = QtCore.QPointF

class TerminalItem(QtGui.QGraphicsEllipseItem):

    def __init__(self):
        super(TerminalItem).__init__(self)

    def add_label(self, text):
        self.label = QtGui.QGraphicsSimpleTextItem(text, self)
        #self.label.align
        #TODO make text left align for in, etc for out.
        self.label.setPos(self.boundingRect().top())



#TODO if multiterm node is finnished, it should be the baseclass
class NodeView(object):
    """
    Class responsible for drawing and interaction of a Node. Note that
    your subclass has to be a subtype of QGraphicsItem. (only one qt
    parent is allowed)
    """
    def __init__(self, node, *args):
        #super(NodeView, self).__init__(*args)
        self.node = node
        self.setAcceptHoverEvents(True)
        flags = [QtGui.QGraphicsItem.ItemIsMovable,
                 QtGui.QGraphicsItem.ItemIsSelectable]
        for f in flags:
            self.setFlag(f)

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
            term._con = 'in'
            self.term_in = term

        if self.node.generates_output:
            term = TerminalItem(self)
            term.setRect(0, 0, 10, 10)
            term._con = 'out'
            self.term_out = term

        self.layout_nodes()

    def layout_nodes(self):
        if hasattr(self, 'term_in'):
            pos = _get_left(self.boundingRect())
            pos += QtCore.QPointF(-15., 0.)
            self.term_in.setPos(pos)

        if hasattr(self, 'term_out'):
            pos = _get_right(self.boundingRect())
            pos += QtCore.QPointF(5., 0.)
            self.term_out.setPos(pos)

        if hasattr(self, 'label'):
            self.label.setPos(self.boundingRect().bottomLeft())

    def add_label(self, text):
        self.label = QtGui.QGraphicsSimpleTextItem(text, self)
        self.label.setPos(self.boundingRect().bottomLeft())

    def hoverEnterEvent(self, ev):
        self.setGraphicsEffect(QtGui.QGraphicsColorizeEffect())

    def hoverLeaveEvent(self, ev):
        self.setGraphicsEffect(None)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.node.show_widget()


class MultiTermNodeView(NodeView):
    def add_terminals(self):
        if self.node.accepts_input:
            term = TerminalItem(self)
            term.setRect(0, 0, 10, 10)
            term._con = 'in'
            self.term_in = term

        if self.node.generates_output:
            term = TerminalItem(self)
            term.setRect(0, 0, 10, 10)
            term._con = 'out'
            self.term_out = term

    def add_terminal(self, name, io_type):
        """
        Adds a single terminal to the view.
        """
        if io_type == 'out':
            term = TerminalItem(self)
            term.setRect(0, 0, 10, 10)
            term._con = 'out'
            self.terms_out.append((name, term))

        elif io_type == 'in':
            term = TerminalItem(self)
            term.setRect(0, 0, 10, 10)
            term._con = 'in'
            self.terms_in.append((name, term))



    def layout_nodes(self):
        n_out = len(self.terms_out)
        coords = _get_n_side(self.rect(), n_out, 'right')

        for name, t in self.terms_out:

            pass





class PixmapNodeView(NodeView, QtGui.QGraphicsPixmapItem):
    """
    Node using a pixmap (icon).
    """

    def __init__(self, node, *args):
        QtGui.QGraphicsPixmapItem.__init__(self)
        pixmap = QtGui.QPixmap(node.icon_path)
        self.setPixmap(pixmap)
        self.setScale(1.)
        NodeView.__init__(self, node, *args)


class WidgetNodeView(NodeView, QtGui.QGraphicsRectItem):
    """
    Node using a full fledged widget.
    """
    def __init__(self, node):
        QtGui.QGraphicsRectItem.__init__(self, 0., 0., 70., 50.)
        proxy = QtGui.QGraphicsProxyWidget(self)
        proxy.setWidget(node.get_widget())
        proxy.setPos(15., 15.)
        NodeView.__init__(self, node)


class LinkLine(QtGui.QGraphicsPathItem):
    """
    Like Link line, but only one pos is a node.
    """
    def __init__(self):
        super(LinkLine, self).__init__()
        self.pen = QtGui.QPen()
        self.pen.setWidth(3)
        self.setPen(self.pen)

    def paint(self, *args):
        start_pos = self.end_pos
        end_pos = self.start_pos
        path_rect = QRectF(start_pos, end_pos)
        path = QtGui.QPainterPath(path_rect.topLeft())
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


def _get_n_side(rect, n, side):
    if side == 'left':
        x = rect.left()
    elif side == 'right':
        x = rect.right()
    part_h = rect.height() / (n + 1.)
    points = []
    for i in range(1, n + 1.):
        p = QPointF(x, rect.bottom() - part_h * i)
        points.append(p)
    return points


def _get_bot(rect):
    return QPointF(rect.left() + rect.width() / 2., rect.bottom())


class SchemaView(QtGui.QGraphicsScene):
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
                it = n.get_view()
                self.addItem(it)
                self.nodes_drawn[n] = it
                offset = QPointF(100., 0.)
                offset.setX(i * 100)
                it.setPos(it.pos() + offset)
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

    #--------------------- Eventhandling after here -----------------

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
            it = [i for i in it if hasattr(i, '_con')]
            it = it[0] if len(it) > 0  else  None
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
        if ev.key() == QtCore.Qt.Key_Delete and self.selectedItems() != []:
            for it in self.selectedItems():
                #Delete connections
                if it in self.connections_drawn.values():
                    self.schema.disconnect_nodes(it.from_node.parentItem().node,
                                                 it.to_node.parentItem().node)
                #Delete Nodes
                if it in self.nodes_drawn.values():
                    self.schema.delete_node(it.node)



