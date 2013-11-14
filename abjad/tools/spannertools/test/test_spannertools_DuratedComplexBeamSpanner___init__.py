# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_DuratedComplexBeamSpanner___init___01():
    r'''Initialize empty durated complex beam spanner.
    '''

    beam = spannertools.DuratedComplexBeamSpanner()
    assert isinstance(beam, spannertools.DuratedComplexBeamSpanner)
