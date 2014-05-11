# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedOrderedDict(
    [
        (
            'backward',
            iotools.View(
                ['segment 03', 'segment 02', 'segment 01']
                ),
            ),
        ]
    )