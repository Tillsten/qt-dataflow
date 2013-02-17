qt-dataflow
===========
This package tries to provide components for building your own
visual programming environment. The authors aim is to make his
data analysis programmes available to his colleagues who don't
know programming or Python.
Because a standard gui is not very flexible, this projects tries
to make visual canvas on which the dataflow is defined. Extensibility
is given through simply adding or modifying Nodes.
This project is inspired by Orange - where i did not see an easy way to just
use the canvas part (also: license differences).

Requirements
------------
It is made with Python 2.7. Not tested for lower versions or
Python 3 (patches welcome). It should work with PySide and PyQt,
but at the moment, the imports need to be manually changed.

The example has additional requirements:
   * numpy
   * guidata
   * matplotlib

Usage
-----
See exampleNodes.py for an easy example.

![My image](example.png)


Todo
----
* Toolbar to allow inserting nodes
* modifying and deleting existing connections.
* deleting nodes
* persistence
* make an example with less requirements.
* checking the connection type.
* ...

License
-------
3-BSD, see license.txt
