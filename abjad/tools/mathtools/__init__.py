# -*- coding: utf-8 -*-
'''Abjad ``mathtools`` package.

    Dependencies:

    The ``mathtools`` package imports no other Abjad modules.
    Do not add modules to mathtools with intrapackage imports.

'''
from abjad.tools import systemtools


systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )

_documentation_section = 'core'
