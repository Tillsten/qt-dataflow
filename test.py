__author__ = 'Tillsten'
from nose.tools import raises, assert_raises
from base import Schema, Node

def test_schema():
    schema = Schema()
    n1 = Node()
    n2 = Node()
    n3 = Node()
    schema.add_node(n1)
    schema.add_node(n2)
    schema.add_node(n3)
    assert(n1 in schema.nodes)
    assert(n2 in schema.nodes)
    schema.delete_node(n1)
    assert(n1 not in schema.nodes)


@raises(ValueError)
def test_schema_exception():
    schema = Schema()
    n1 = Node()
    schema.add_node(n1)
    schema.add_node(n1)

def test_schema_connections():
    schema = Schema()
    n1 = Node()
    n2 = Node()
    n3 = Node()
    schema.add_node(n1)
    schema.add_node(n2)
    assert_raises(ValueError, schema.connect_nodes, n1, n1)
    schema.connect_nodes(n1, n2)
    assert((n1, n2) in schema.connections)
    assert(n1.out_conn[0] is n2)
    assert(n2.in_conn[0] is n1)
    assert_raises(ValueError, schema.disconnect_nodes, n2, n1)
    schema.connect_nodes(n3, n2)
    schema.disconnect_nodes(n1, n2)
    assert(schema.connections == [(n3, n2)])
    assert(n1.out_conn == [])
    assert(n2.in_conn == [n3])