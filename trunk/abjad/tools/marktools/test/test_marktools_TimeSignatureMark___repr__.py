# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.marktools import TimeSignatureMark


def test_marktools_TimeSignatureMark___repr___01():
    r'''Time signature mark returns nonempty string repr.
    '''

    time_signature_repr = marktools.TimeSignatureMark((3, 8)).__repr__()
    assert isinstance(time_signature_repr, str) and 0 < len(time_signature_repr)


def test_marktools_TimeSignatureMark___repr___02():
    r'''Repr is evaluable.
    '''

    time_signature_1 = marktools.TimeSignatureMark((3, 8), partial=Duration(1, 8))
    time_signature_2 = eval(repr(time_signature_1))

    assert time_signature_1 == time_signature_2
