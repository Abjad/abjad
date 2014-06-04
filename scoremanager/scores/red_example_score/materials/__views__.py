# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedOrderedDict(
    [
        (
            'autoeditable',
            iotools.View(
                ['md:use_autoeditor']
                ),
            ),
        ]
    )