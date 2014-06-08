# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=iotools.ViewInventory(
    [
        (
            'autoeditable',
            iotools.View(
                ['md:use_autoeditor']
                ),
            ),
        (
            'inventories',
            iotools.View(
                ["'inventory' in :ds:"]
                ),
            ),
        (
            'magic',
            iotools.View(
                ["'magic_' in :path:"]
                ),
            ),
        ]
    )