from abjad import *


def test_TimeSignatureMark___init___01():
    '''Initialize time signature mark from integer pair.
    '''

    time_signature = contexttools.TimeSignatureMark((9, 32))
    assert isinstance(time_signature, contexttools.TimeSignatureMark)
    assert time_signature.lilypond_format == '\\time 9/32'


def test_TimeSignatureMark___init___02():
    '''Initialize time signature mark from other time signature instance.
    '''

    time_signature_1 = contexttools.TimeSignatureMark((9, 32))
    time_signature_2 = contexttools.TimeSignatureMark(time_signature_1)

    assert isinstance(time_signature_1, contexttools.TimeSignatureMark)
    assert isinstance(time_signature_2, contexttools.TimeSignatureMark)
    assert time_signature_1.lilypond_format == '\\time 9/32'
    assert time_signature_2.lilypond_format == '\\time 9/32'
    assert time_signature_1 is not time_signature_2


def test_TimeSignatureMark___init___03():
    '''Initialize time signature mark from other time signature instance with partial.
    '''

    time_signature_1 = contexttools.TimeSignatureMark((9, 32), partial=Duration(1, 32))
    time_signature_2 = contexttools.TimeSignatureMark(time_signature_1)

    assert time_signature_1 == time_signature_2
    assert not time_signature_1 is time_signature_2
