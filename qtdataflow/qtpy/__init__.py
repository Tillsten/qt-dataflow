"""Abstraction for different Python Qt bindings.

Supported Python Qt bindings are PyQt4 and PySide.
The Qt modules can be imported like this:

from qtpy.QtCore import QObject
from qtpy import QtGui, loadUi

All available modules are listed in QT_BINDING_MODULES.

"""

import sys

try:
    from binding_helper import loadUi, QT_BINDING, QT_BINDING_MODULES, QT_BINDING_VERSION # @UnusedImport

    # register all binding modules as sub modules of this package (qtools.qtpy) for easy importing
    for module_name, module in QT_BINDING_MODULES.items():
        sys.modules[__name__ + '.' + module_name] = module
        setattr(sys.modules[__name__], module_name, module)
        del module_name
        del module

    del sys


except ImportError:
    QtCore = QtGui = None
