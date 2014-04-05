# -*- encoding: utf-8 -*-
'''Abjad ``labeltools`` package.

Dependencies:

The ``labeltools`` package is a high-level labeling package.
The package may import essentially all of the core packages
at top level.
'''
from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'core'