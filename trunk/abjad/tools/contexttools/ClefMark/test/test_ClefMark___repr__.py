from abjad import *


def test_ClefMark___repr___01():
    '''Clef returns a nonempty repr string.
    '''

    repr = contexttools.ClefMark('treble').__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
