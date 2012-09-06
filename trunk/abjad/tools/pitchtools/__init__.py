'''Abjad ``pitchtools`` package.

    Dependencies:

    The ``pitchtools`` package may import ``sequencetools`` at top level.

    The ``pitchtools`` package should not import any component packages 
    at top level.

'''
from abjad.tools import importtools

importtools.import_structured_package(__path__[0], globals())

_documentation_section = 'core'
