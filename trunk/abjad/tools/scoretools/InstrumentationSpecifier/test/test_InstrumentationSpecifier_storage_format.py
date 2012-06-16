from abjad import *


def test_InstrumentationSpecifier_storage_format_01():

    flute = scoretools.Performer('Flute')
    flute.instruments.append(instrumenttools.Flute())
    flute.instruments.append(instrumenttools.AltoFlute())
    guitar = scoretools.Performer('Guitar')
    guitar.instruments.append(instrumenttools.Guitar())
    specifier = scoretools.InstrumentationSpecifier([flute, guitar])
    
    r'''
    scoretools.InstrumentationSpecifier(
        performers=scoretools.PerformerInventory([
            scoretools.Performer(
                name='Flute',
                instruments=instrumenttools.InstrumentInventory([
                    instrumenttools.Flute(),
                    instrumenttools.AltoFlute()
                    ])
                ),
            scoretools.Performer(
                name='Guitar',
                instruments=instrumenttools.InstrumentInventory([
                    instrumenttools.Guitar()
                    ])
                )
            ])
        )
    '''

    assert specifier.storage_format == "scoretools.InstrumentationSpecifier(\n\tperformers=scoretools.PerformerInventory([\n\t\tscoretools.Performer(\n\t\t\tname='Flute',\n\t\t\tinstruments=instrumenttools.InstrumentInventory([\n\t\t\t\tinstrumenttools.Flute(),\n\t\t\t\tinstrumenttools.AltoFlute()\n\t\t\t\t])\n\t\t\t),\n\t\tscoretools.Performer(\n\t\t\tname='Guitar',\n\t\t\tinstruments=instrumenttools.InstrumentInventory([\n\t\t\t\tinstrumenttools.Guitar()\n\t\t\t\t])\n\t\t\t)\n\t\t])\n\t)"
