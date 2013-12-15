# -*- encoding: utf-8 -*-
'''Page layout tools.

   This package depends on the following:

      * rational numbers
'''

from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'core'
