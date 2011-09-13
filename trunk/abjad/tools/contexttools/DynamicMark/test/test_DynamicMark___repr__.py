from abjad import *


def test_DynamicMark___repr___01():
    '''Dynamic mark returns nonempty string repr.
    '''

    repr = contexttools.DynamicMark('f').__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
