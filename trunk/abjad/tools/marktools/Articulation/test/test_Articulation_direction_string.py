from abjad import *


def test_Articulation_direction_string_01():

    t = Note("c'4")
    a = marktools.Articulation('staccato')(t)

    assert a.direction_string is None

    a.direction_string = '^'

    assert a.direction_string == '^'
