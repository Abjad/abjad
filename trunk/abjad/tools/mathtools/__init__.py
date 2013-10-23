# -*- encoding: utf-8 -*-
'''Abjad ``mathtools`` package.

    Dependencies:

    The ``mathtools`` package imports no other Abjad modules.
    Do not add modules to mathtools with intrapackage imports.

'''
from abjad.tools import importtools


importtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	package_root_name='abjad',
    )

_documentation_section = 'core'
