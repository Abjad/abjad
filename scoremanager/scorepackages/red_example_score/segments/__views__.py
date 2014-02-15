# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedOrderedDict(
    [
        (
            'forward',
            iotools.View(
                ['segment 01', 'segment 02', 'segment 03'],
                ),
            ),
        (
            'backward',
            iotools.View(
                ['segment 03', 'segment 02', 'segment 01'],
                ),
            ),
        ],
    item_class=iotools.View,
    )
