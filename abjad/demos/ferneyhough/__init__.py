# -*- coding: utf-8 -*-
import abjad


abjad.systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )

_documentation_section = 'demos'

del(main)
