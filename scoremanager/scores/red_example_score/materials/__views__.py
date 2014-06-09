# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import ide


view_inventory=ide.ViewInventory(
    [
        (
            'autoeditable',
            ide.View(
                ['md:use_autoeditor']
                ),
            ),
        (
            'inventories',
            ide.View(
                ["'inventory' in :ds:"]
                ),
            ),
        (
            'magic',
            ide.View(
                ["'magic_' in :path:"]
                ),
            ),
        ]
    )