from abjad import *


def test_InstrumentInventory__tools_package_qualified_indented_repr_01():

    inventory = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Violin()])

    r'''
    instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Violin()
        ])
    '''

    assert inventory._tools_package_qualified_indented_repr == 'instrumenttools.InstrumentInventory([\n\tinstrumenttools.Flute(),\n\tinstrumenttools.Violin()\n\t])'
