# -*- encoding: utf-8 -*-
from abjad import *


def test_indicatortools_TimeSignature___init___01():
    r'''Initialize time signature from integer pair.
    '''

    time_signature = TimeSignature((9, 32))
    assert isinstance(time_signature, TimeSignature)
    assert format(time_signature, 'lilypond') == '\\time 9/32'


def test_indicatortools_TimeSignature___init___02():
    r'''Initialize time signature from other time signature instance.
    '''

    time_signature_1 = TimeSignature((9, 32))
    time_signature_2 = TimeSignature(time_signature_1)

    assert isinstance(time_signature_1, TimeSignature)
    assert isinstance(time_signature_2, TimeSignature)
    assert format(time_signature_1, 'lilypond') == '\\time 9/32'
    assert format(time_signature_2, 'lilypond') == '\\time 9/32'
    assert time_signature_1 is not time_signature_2


def test_indicatortools_TimeSignature___init___03():
    r'''Initialize time signature from other time signature 
    instance with partial.
    '''

    time_signature_1 = TimeSignature(
        (9, 32), 
        partial=Duration(1, 32),
        )
    time_signature_2 = TimeSignature(time_signature_1)

    assert time_signature_1 == time_signature_2
    assert not time_signature_1 is time_signature_2
