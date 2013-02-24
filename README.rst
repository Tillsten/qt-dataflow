===========
qt-dataflow
===========
This package tries to provide components for building your own
visual programming environment. The authors aim is to make his
data analysis tool available to his colleagues who don't
know programming or Python.

Because a standard gui is not very flexible, this projects tries
to make visual canvas on which the dataflow can be defined and modified.
Extensibility is given through simply adding or modifying Nodes.


This project is inspired by Orange - where i did not see an easy way to just
use the canvas part (also: license differences). Also the design tries
to be more flexible.


Requirements
------------
It is made with Python 2.7. Not tested for lower versions or
Python 3 (patches welcome). It should work with PySide and PyQt,
but at the moment, the imports need to be manually changed.

The examples have additional requirements:
   * numpy
   * matplotlib
   * pyqtgraph for the pyqtgraph example

Examples
--------
See example.py for an simple example using icons whic react to double click.
Hold the mousebutton to connect node Termials (only out-> in is allowed).

.. image:: https://github.com/Tillsten/qt-dataflow/raw/master/example.png

example_widget uses widgets on the canvas directly, it also show how to make

example_pyqtgraph need also the pyqtgraph package. It plot directly on the
canvas.

example_matplotlib_on_canvas does the same, but uses matplotlib via
a temporary file.

Code Example
------------
To make custom nodes you need to subclass Node. It must return
a NodeView via its 'get_view' method. The following example
implements a Node which make a random number.


    class RandomNumber(Node):
        """
        A test node which outputs a random number. Widget allow to set the number.
        """
        def __init__(self):
            super(DataGenNode, self).__init__()
            #Node type/name
            self.node_type = 'Random Array'
            #Icon_path is needed for the PixmapNodeView
            self.icon_path = 'icons/onebit_11.png'
            #The makes the node have an output terminal.
            self.generates_output = True

        def get_view(self):
            return PixmapNodeView(self)

        def get(self):
            #Method which can be called by other nodes. The name is just
            #a convention.
            num = [random.random() for i in range(self.num_points)]
            return num

        def show_widget(self):
            #Method called by double clicking on the icon.
            int, ok = Qt.QtGui.QInputDialog.getInteger(None, 'Input Dialog',
                                              'Number of Points', self.num_points)
            if ok:
                self.num_points = int




Structure
---------
The logic is as follow: A schema contains all nodes and connections between nodes.
Nodes can accept inputs and/or provide an output.

The rendering and the gui interaction is handled by the
corresponding SchemaView and NodeView classes. The interaction is almost
exclusively handled by by SchemaView.

The gui module contains some basic usage widgets.

Todo
----
* add different icons (simple)
* nicer toolbar (drag-n-drop would be nice)
* persistence
* make an example with less requirements.
* checking and introducing a connection type.
* checking and improving compatibility with different Python versions.
* automate detection of qt-toolkit.
* signaling changes in nodes (optional?)
* ...

Coding Style
------------
This projects tries to follow PEP8.

License
-------
Example icons are from http://www.icojam.com/blog/?p=177 (Public Domain).

BSD - 3 clauses, see license.txt.
