# -*- encoding: utf-8 -*-
'''Time signature manipulation tools.

   Modules in this package depend on, may freely import from, the following:

      from abjad.tools import durationtools
      from abjad.tools import mathtools
'''

from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'core'
