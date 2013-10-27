# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_MeasuredComplexBeamSpanner___init___01():
    r'''Init empty measured complex beam spanner.
    '''

    beam = spannertools.MeasuredComplexBeamSpanner()
    assert isinstance(beam, spannertools.MeasuredComplexBeamSpanner)
