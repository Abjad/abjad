from abjad import *


def test_Performer__tools_package_qualified_indented_repr_01():

    performer = scoretools.Performer('Flute')
    performer.instruments.append(instrumenttools.Flute())
    performer.instruments.append(instrumenttools.AltoFlute())

    r'''
    scoretools.Performer(
        name='Flute',
        instruments=instrumenttools.InstrumentInventory([
            instrumenttools.Flute(),
            instrumenttools.AltoFlute()
            ])
        )
    '''

    assert performer._storage_format == "scoretools.Performer(\n\tname='Flute',\n\tinstruments=instrumenttools.InstrumentInventory([\n\t\tinstrumenttools.Flute(),\n\t\tinstrumenttools.AltoFlute()\n\t\t])\n\t)"
