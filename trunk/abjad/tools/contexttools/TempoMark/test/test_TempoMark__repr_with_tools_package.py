from abjad import *


def test_TempoMark__fully_qualified_repr_01():

    assert contexttools.TempoMark('Allegro', (1, 4), 84)._fully_qualified_repr == \
        "contexttools.TempoMark('Allegro', durationtools.Duration(1, 4), 84)"
