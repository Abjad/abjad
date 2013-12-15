# -*- encoding: utf-8 -*-
'''Abjad ``scoretools`` package.

    Dependencies:

    The ``scoretools`` package may import the ``scoretools``
    and ``componenttool`` packages at top level.

    The ``scoretools`` package should not import sibling
    or cousing packages like ``scoretools`` at top level.

    The ``scoretools`` package should not import ``instrumenttools`` 
    at top level.
    
'''
from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'core'
