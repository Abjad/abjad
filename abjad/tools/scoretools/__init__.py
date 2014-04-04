# -*- encoding: utf-8 -*-
'''Dependencies:

The ``scoretools`` package should not import ``instrumenttools``
at top level.
'''
from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'core'