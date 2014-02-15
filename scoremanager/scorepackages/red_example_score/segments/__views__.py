# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedOrderedDict(
    [
        (
            'forward',
            iotools.View(
                ['segment 01', 'segment 02', 'segment 03'],
                custom_identifier='forward',
                ),
            ),
        (
            'backward',
            iotools.View(
                ['segment 03', 'segment 02', 'segment 01'],
                custom_identifier='backward',
                ),
            ),
        ],
    item_class=iotools.View,
    )