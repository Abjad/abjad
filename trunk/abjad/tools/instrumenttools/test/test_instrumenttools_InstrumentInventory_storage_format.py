# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_InstrumentInventory_storage_format_01():

    inventory = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Violin()])

    assert testtools.compare(
        inventory.storage_format,
        r'''
        instrumenttools.InstrumentInventory([
            instrumenttools.Flute(),
            instrumenttools.Violin(),
            ])
        ''',
        )
