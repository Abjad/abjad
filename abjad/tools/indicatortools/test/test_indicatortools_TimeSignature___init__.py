# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_TimeSignature___init___01():
    r'''Initializes time signature from integer pair.
    '''

    time_signature = TimeSignature((9, 32))
    assert isinstance(time_signature, TimeSignature)
    assert format(time_signature, 'lilypond') == '\\time 9/32'
