from abjad import *


def test_Voice___len___01():
    '''Voice length returns the number of elements in voice.'''

    t = Voice()
    assert len(t) == 0


def test_Voice___len___02():
    '''Voice length returns the number of elements in voice.'''

    t = Voice("c'8 d'8 e'8 f'8")
    assert len(t) == 4
