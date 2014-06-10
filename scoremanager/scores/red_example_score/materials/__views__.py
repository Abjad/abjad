# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import idetools


view_inventory=idetools.ViewInventory(
    [
        (
            'autoeditable',
            idetools.View(
                ['md:use_autoeditor']
                ),
            ),
        (
            'inventories',
            idetools.View(
                ["'inventory' in :ds:"]
                ),
            ),
        (
            'magic',
            idetools.View(
                ["'magic_' in :path:"]
                ),
            ),
        ]
    )