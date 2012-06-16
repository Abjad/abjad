from abjad import *


def test_TempoMark_storage_format_01():

    tempo_mark = contexttools.TempoMark('Allegro', (1, 4), 84)

    r'''
    contexttools.TempoMark(
        'Allegro',
        durationtools.Duration(1, 4),
        84
        )
    '''

    assert tempo_mark.storage_format == "contexttools.TempoMark(\n\t'Allegro',\n\tdurationtools.Duration(1, 4),\n\t84\n\t)"
