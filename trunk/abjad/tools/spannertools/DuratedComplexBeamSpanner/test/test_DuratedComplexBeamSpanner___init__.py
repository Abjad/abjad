# -*- encoding: utf-8 -*-
from abjad import *


def test_DuratedComplexBeamSpanner___init___01():
    r'''Init empty durated complex beam spanner.
    '''

    beam = spannertools.DuratedComplexBeamSpanner()
    assert isinstance(beam, spannertools.DuratedComplexBeamSpanner)
