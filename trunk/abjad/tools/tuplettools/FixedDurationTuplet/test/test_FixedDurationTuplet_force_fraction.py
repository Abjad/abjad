# -*- encoding: utf-8 -*-
from abjad import *


def test_FixedDurationTuplet_force_fraction_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    tuplet.force_fraction = True

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )
