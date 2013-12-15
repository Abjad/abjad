# -*- encoding: utf-8 -*-
'''Abjad ``pitchtools`` package.

    Dependencies:

    The ``pitchtools`` package may import ``sequencetools`` at top level.

    The ``pitchtools`` package should not import any component packages 
    at top level.

    The ``pitchtools`` package should not import ``indicatortools`` at
    top level, and vice versa.

'''
from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'core'
