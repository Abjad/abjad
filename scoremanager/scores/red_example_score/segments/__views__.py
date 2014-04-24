# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedOrderedDict(
    [
        (
            'backward',
            iotools.View(
                [
                    'segment 03 (Red Example Score)',
                    'segment 02 (Red Example Score)',
                    'segment 01 (Red Example Score)',
                    ]
                ),
            ),
        ]
    )