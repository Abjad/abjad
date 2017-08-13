from __future__ import absolute_import
from abjad import *


systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    delete_systemtools=False,
    )
