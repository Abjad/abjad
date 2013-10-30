# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Performer_storage_format_01():

    performer = instrumenttools.Performer('Flute')
    performer.instruments.append(instrumenttools.Flute())
    performer.instruments.append(instrumenttools.AltoFlute())

    r'''
    instrumenttools.Performer(
        name='Flute',
        instruments=instrumenttools.InstrumentInventory([
            instrumenttools.Flute(),
            instrumenttools.AltoFlute()
            ])
        )
    '''

    assert performer.storage_format == "instrumenttools.Performer(\n\tname='Flute',\n\tinstruments=instrumenttools.InstrumentInventory([\n\t\tinstrumenttools.Flute(),\n\t\tinstrumenttools.AltoFlute()\n\t\t])\n\t)"
