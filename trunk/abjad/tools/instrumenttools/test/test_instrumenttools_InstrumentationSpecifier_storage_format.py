# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_InstrumentationSpecifier_storage_format_01():

    flute = instrumenttools.Performer('Flute')
    flute.instruments.append(instrumenttools.Flute())
    flute.instruments.append(instrumenttools.AltoFlute())
    guitar = instrumenttools.Performer('Guitar')
    guitar.instruments.append(instrumenttools.Guitar())
    specifier = instrumenttools.InstrumentationSpecifier([flute, guitar])

    assert testtools.compare(
        specifier.storage_format,
        r'''
        instrumenttools.InstrumentationSpecifier(
            performers=instrumenttools.PerformerInventory([
                instrumenttools.Performer(
                    name='Flute',
                    instruments=instrumenttools.InstrumentInventory([
                        instrumenttools.Flute(),
                        instrumenttools.AltoFlute()
                        ])
                    ),
                instrumenttools.Performer(
                    name='Guitar',
                    instruments=instrumenttools.InstrumentInventory([
                        instrumenttools.Guitar()
                        ])
                    )
                ])
            )
        ''',
        )
