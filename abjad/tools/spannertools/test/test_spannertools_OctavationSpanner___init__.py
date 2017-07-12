# -*- coding: utf-8 -*-
import abjad


def test_spannertools_OctavationSpanner___init___01():
    r'''Initialize empty octavation spanner.
    '''

    octavation = abjad.OctavationSpanner()
    assert isinstance(octavation, abjad.OctavationSpanner)
