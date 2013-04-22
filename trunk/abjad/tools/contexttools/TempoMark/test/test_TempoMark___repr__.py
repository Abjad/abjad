from abjad import *


def test_TempoMark___repr___01():
    '''Tempo mark returns nonempty string repr.
    '''

    repr = contexttools.TempoMark((1, 8), 48).__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
