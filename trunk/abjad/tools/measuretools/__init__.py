'''Abjad ``measuretools`` package.

    Import regime:
    
    The ``measuretools`` package may import all leaf packages at top level.

    The ``measuretools`` package may import all parent component packages
    at top level. These are ``containertools`` and ``componenttools``.

    The ``measuretools`` package should not import sibling- or cousin-related
    container packages at top level. This includes ``tuplettools`` and other
    packages.

    The ``measuretools`` package must not import ``contexttools`` at top level
    even though measures and time signatures are closely related. This allows
    ``contexttools`` to import the component packages freely at top-level.      

    The ``measuretools`` package must not import ``timesignaturetools`` at top
    level in order to handle ``timesignaturetools`` in parallel to ``contexttools``.

'''
from abjad.tools import importtools

importtools.import_structured_package(__path__[0], globals())

_documentation_section = 'core'
