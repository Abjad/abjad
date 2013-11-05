# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Performer_storage_format_01():

    performer = instrumenttools.Performer('Flute')
    performer.instruments.append(instrumenttools.Flute())
    performer.instruments.append(instrumenttools.AltoFlute())

    assert testtools.compare(
        performer.storage_format,
        r'''
        instrumenttools.Performer(
            name='Flute',
            instruments=instrumenttools.InstrumentInventory([
                instrumenttools.Flute(),
                instrumenttools.AltoFlute(),
                ])
            )
        ''',
        )
