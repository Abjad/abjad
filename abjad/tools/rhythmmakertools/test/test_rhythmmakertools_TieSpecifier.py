# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_TieSpecifier_01():

    divisions = [(3, 8), (5, 16), (1, 4), (5, 16)]
    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        burnish_specifier=rhythmmakertools.BurnishSpecifier(
            left_classes=(Rest, Note),
            left_counts=(1,),
            ),
        extra_counts_per_division=(0, 1, 1),
        talea=rhythmmakertools.Talea(
            counts=(1, 2, 3),
            denominator=16,
            ),
        tie_specifier=rhythmmakertools.TieSpecifier(
            tie_across_divisions=True,
            ),
        )
    selections = rhythm_maker(divisions)
    staff = Staff(selections)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                r16
                c'8 [
                c'8. ~ ]
            }
            \tweak text #tuplet-number::calc-fraction-text
            \times 5/6 {
                c'16 [
                c'8
                c'8. ]
            }
            \times 4/5 {
                r16
                c'8 [
                c'8 ~ ]
            }
            {
                c'16 [
                c'16
                c'8
                c'16 ]
            }
        }
        '''
        )
