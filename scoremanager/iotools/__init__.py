# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
import sys
if sys.version_info[0] == 2:
    import getters
else:
    from scoremanager.iotools import getters
del sys


systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'score manager'
