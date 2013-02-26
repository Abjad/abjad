from abjad import *


def test_InstrumentInventory_storage_format_01():

    inventory = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Violin()])

    r'''
    instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Violin()
        ])
    '''

    assert inventory.storage_format == 'instrumenttools.InstrumentInventory([\n\tinstrumenttools.Flute(),\n\tinstrumenttools.Violin()\n\t])'
