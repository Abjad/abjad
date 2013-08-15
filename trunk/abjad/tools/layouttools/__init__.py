# -*- encoding: utf-8 -*-
'''Page layout tools.

   This package depends on the following:

      * rational numbers
'''

from abjad.tools import importtools

importtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	package_root_name='abjad')

_documentation_section = 'core'
