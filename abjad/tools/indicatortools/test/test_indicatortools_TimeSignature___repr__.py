# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_TimeSignature___repr___01():
    r'''Time signature returns nonempty string repr.
    '''

    time_signature_repr = TimeSignature((3, 8)).__repr__()
    assert isinstance(time_signature_repr, str) and \
        0 < len(time_signature_repr)


def test_indicatortools_TimeSignature___repr___02():
    r'''Repr is evaluable.
    '''

    time_signature_1 = TimeSignature((3, 8), partial=Duration(1, 8))
    time_signature_2 = eval(repr(time_signature_1))

    assert time_signature_1 == time_signature_2
