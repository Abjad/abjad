from abjad import *


def test_TempoMark_storage_format_01():

    tempo_mark = contexttools.TempoMark('Allegro', (1, 4), 84)

    r'''
    contexttools.TempoMark(
        'Allegro',
        durationtools.Duration(
            1,
            4
            ),
        84
    )
    '''

    assert tempo_mark.storage_format == "contexttools.TempoMark(\n\t'Allegro',\n\tdurationtools.Duration(\n\t\t1,\n\t\t4\n\t\t),\n\t84\n\t)"
