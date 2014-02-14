# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedList(
    [
        iotools.View(
            ['segment 03', 'segment 02', 'segment 01'],
            custom_identifier='backward',
            ),
        iotools.View(
            ['segment 01', 'segment 02', 'segment 03'],
            custom_identifier='forward',
            ),
        iotools.View(
            ['segment 02', 'segment 03', 'segment 01'],
            custom_identifier='two-three-one',
            ),
        ]
    )
