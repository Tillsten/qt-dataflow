try:
    from PyQt4.QtCore import QObject, pyqtSignal
    Signal = pyqtSignal
except ImportError:
    from PySide.QtCore import QObject, Signal

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
    node_created = Signal(Node)
    node_deleted = Signal(Node)
    nodes_connected = Signal(list)
    nodes_disconnected = Signal(list)

    def __init__(self):
        super(Schema, self).__init__()
        self.nodes = []
        self.connections = []

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            self.node_created.emit(node)
        else:
            raise ValueError('Node already in Schema.')

    def delete_node(self, node):
        to_delete = [(o, i) for (o, i) in self.connections
                     if o == node or i == node]

        for o, i in to_delete:
            self.disconnect_nodes(o, i)

        self.nodes.remove(node)
        self.node_deleted.emit(node)

    def connect_nodes(self, out_node, in_node):
        if out_node is in_node:
            raise ValueError("Node can't connect to itself")
        out_node.out_conn.append(in_node)
        in_node.in_conn.append(out_node)
        self.connections.append((out_node, in_node))
        self.nodes_connected.emit([out_node, in_node])

    def disconnect_nodes(self, out_node, in_node):
        if (out_node, in_node) not in self.connections:
            raise ValueError("Nodes are not connected")
        self.nodes_disconnected.emit([out_node, in_node])
        out_node.out_conn.remove(in_node)
        in_node.in_conn.remove(out_node)
        self.connections.remove((out_node, in_node))

    def to_disk(self, file):
        import pickle

        to_pickle = (self.nodes, self.connections)
        return pickle.dump(to_pickle, file)

    def from_disk(self, file):
        import pickle

        nodes, connections = pickle.load(file)
        for n in nodes:
            self.add_node(n)
        for c in connections:
            self.connect_nodes(*c)
