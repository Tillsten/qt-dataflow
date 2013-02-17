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
   * matplotlib

Usage
-----
See example.py for an easy example using icons whic react to double click.
Hold the mousebutton to connect node Termials (only out-> in is allowed).

.. image:: https://github.com/Tillsten/qt-dataflow/raw/master/example.png

Example2 uses widgets directly, also uses callback to propagate changes.
Warning, there is no circular detection yet.


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
This projects trys to follow PEP8.

License
-------
Example icons are from http://www.icojam.com/blog/?p=177 (Public Domain).

BSD - 3 clauses, see license.txt.
