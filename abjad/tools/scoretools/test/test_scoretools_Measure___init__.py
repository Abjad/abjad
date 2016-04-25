# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Measure___init___01():
    r'''Initializes measure from empty input.
    '''

    measure = Measure()

    assert measure.time_signature == TimeSignature((4, 4))
    assert not len(measure)
