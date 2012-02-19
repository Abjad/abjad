from abjad import *


def test_Articulation_direction_01():

    t = Note("c'4")
    a = marktools.Articulation('staccato')(t)

    assert a.direction is None

    a.direction = '^'

    assert a.direction == '^'
