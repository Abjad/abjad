from abjad import *


def test_TimeSignatureMark___init___01():
    '''Initialize time signature mark from integer pair.
    '''

    time_signature = contexttools.TimeSignatureMark((9, 32))
    assert isinstance(time_signature, contexttools.TimeSignatureMark)
    assert time_signature.format == '\\time 9/32'


def test_TimeSignatureMark___init___02():
    '''Initialize time signature mark from other time signature instance.
    '''

    time_signature_1 = contexttools.TimeSignatureMark((9, 32))
    time_signature_2 = contexttools.TimeSignatureMark(time_signature_1)
    assert isinstance(time_signature_1, contexttools.TimeSignatureMark)
    assert isinstance(time_signature_2, contexttools.TimeSignatureMark)
    assert time_signature_1.format == '\\time 9/32'
    assert time_signature_2.format == '\\time 9/32'
    assert time_signature_1 is not time_signature_2
