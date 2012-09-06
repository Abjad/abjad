'''Abjad ``scoretools`` package.

    Dependencies:

    The ``scoretools`` package may import the ``containertools``
    and ``componenttool`` packages at top level.

    The ``scoretools`` package should not import sibling
    or cousing packages like ``stafftools`` at top level.

    The ``scoretools`` package should not import ``instrumenttools`` 
    at top level.
    
'''
from abjad.tools import importtools

importtools.import_structured_package(__path__[0], globals())

_documentation_section = 'core'
