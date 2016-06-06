# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_FixedDurationTuplet_force_fraction_01():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    tuplet.force_fraction = True

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )
