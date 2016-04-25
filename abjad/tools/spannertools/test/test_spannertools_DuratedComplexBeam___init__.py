# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_DuratedComplexBeam___init___01():
    r'''Initialize empty durated complex beam spanner.
    '''

    beam = spannertools.DuratedComplexBeam()
    assert isinstance(beam, spannertools.DuratedComplexBeam)
