# -*- coding: utf-8 -*-
import abjad


def test_spannertools_MeasuredComplexBeam___init___01():
    r'''Initialize empty measured complex beam spanner.
    '''

    beam = abjad.MeasuredComplexBeam()
    assert isinstance(beam, abjad.MeasuredComplexBeam)
