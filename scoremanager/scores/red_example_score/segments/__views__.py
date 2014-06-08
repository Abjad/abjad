# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=iotools.ViewInventory(
    [
        (
            'backward',
            iotools.View(
                ['C', 'B', 'A']
                ),
            ),
        ]
    )