from abjad import *


def testContextMark___repr___01():
    '''Context mark returns a nonempty string repr.
    '''

    repr = contexttools.ContextMark().__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
