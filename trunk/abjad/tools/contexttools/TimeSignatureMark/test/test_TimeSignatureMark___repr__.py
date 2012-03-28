from abjad import *
from abjad.tools.contexttools import TimeSignatureMark


def test_TimeSignatureMark___repr___01():
    '''Time signature mark returns nonempty string repr.
    '''

    time_signature_repr = contexttools.TimeSignatureMark((3, 8)).__repr__()
    assert isinstance(time_signature_repr, str) and 0 < len(time_signature_repr)


def test_TimeSignatureMark___repr___02():
    '''Repr is evaluable.
    '''
    
    time_signature_1 = contexttools.TimeSignatureMark((3, 8), partial=Duration(1, 8))
    time_signature_2 = eval(repr(time_signature_1))

    assert time_signature_1 == time_signature_2
