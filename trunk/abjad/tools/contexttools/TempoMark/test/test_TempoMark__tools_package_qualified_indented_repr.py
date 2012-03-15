from abjad import *


def test_TempoMark__tools_package_qualified_indented_repr_01():

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

    assert tempo_mark._tools_package_qualified_indented_repr == "contexttools.TempoMark(\n\t'Allegro',\n\tdurationtools.Duration(\n\t\t1,\n\t\t4\n\t\t),\n\t84\n\t)"
