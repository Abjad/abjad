# -*- coding: utf-8 -*-
import abjad
from abjad import *


def test_spannertools_MeasuredComplexBeam___init___01():
    r'''Initialize empty measured complex beam spanner.
    '''

    beam = spannertools.MeasuredComplexBeam()
    assert isinstance(beam, spannertools.MeasuredComplexBeam)
