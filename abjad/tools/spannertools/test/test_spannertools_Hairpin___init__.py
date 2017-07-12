# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Hairpin___init___01():
    r'''Initialize empty hairpin spanner.
    '''

    hairpin = abjad.Hairpin()
    assert isinstance(hairpin, abjad.Hairpin)
