# -*- encoding: utf-8 -*-
from abjad import *


def test_TimeSignatureMark___init___01():
    r'''Initialize time signature mark from integer pair.
    '''

    time_signature = TimeSignatureMark((9, 32))
    assert isinstance(time_signature, TimeSignatureMark)
    assert format(time_signature, 'lilypond') == '\\time 9/32'


def test_TimeSignatureMark___init___02():
    r'''Initialize time signature mark from other time signature instance.
    '''

    time_signature_1 = TimeSignatureMark((9, 32))
    time_signature_2 = TimeSignatureMark(time_signature_1)

    assert isinstance(time_signature_1, TimeSignatureMark)
    assert isinstance(time_signature_2, TimeSignatureMark)
    assert format(time_signature_1, 'lilypond') == '\\time 9/32'
    assert format(time_signature_2, 'lilypond') == '\\time 9/32'
    assert time_signature_1 is not time_signature_2


def test_TimeSignatureMark___init___03():
    r'''Initialize time signature mark from other time signature 
    instance with partial.
    '''

    time_signature_1 = TimeSignatureMark(
        (9, 32), 
        partial=Duration(1, 32),
        )
    time_signature_2 = TimeSignatureMark(time_signature_1)

    assert time_signature_1 == time_signature_2
    assert not time_signature_1 is time_signature_2
