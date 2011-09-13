from abjad import *


def test_TimeSignatureMark___repr___01():
    '''Time signature mark returns nonempty string repr.
    '''

    repr = contexttools.TimeSignatureMark((3, 8)).__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
