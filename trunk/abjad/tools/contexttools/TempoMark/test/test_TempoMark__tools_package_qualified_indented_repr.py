from abjad import *


def test_TempoMark__tools_package_qualified_indented_repr_01():

    tempo_mark = contexttools.TempoMark('Allegro', (1, 4), 84)

    r'''
    contexttools.TempoMark(
        'Allegro',
        durationtools.Duration(1, 4),
        84
        )
    '''

    assert tempo_mark._tools_package_qualified_indented_repr == \
        "contexttools.TempoMark(\n\t'Allegro',\n\tdurationtools.Duration(1, 4),\n\t84\n\t)"
