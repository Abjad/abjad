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
            \tweak #'text #tuplet-number::calc-fraction-text
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


def test_rhythmmakertools_TieSpecifier_02():

    pattern = patterntools.select_every(indices=[1], period=2)
    divisions = [(3, 8), (4, 4), (5, 16), (7, 8)]
    rhythm_maker = rhythmmakertools.EvenRunRhythmMaker(
        tie_specifier=rhythmmakertools.TieSpecifier(
            tie_consecutive_notes=pattern,
            ),
        )
    assert divisions[0] == (3, 8)
    selections = rhythm_maker(divisions)
    print(selections[0])
    staff = Staff(selections)
    f(staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                c'8 ~ [
                c'8
                c'8 ~ ]
            }
            {
                c'4
                c'4 ~
                c'4
                c'4 ~
            }
            {
                c'16 [
                c'16 ~
                c'16
                c'16 ~
                c'16 ]
            }
            {
                c'8 ~ [
                c'8
                c'8 ~
                c'8
                c'8 ~
                c'8
                c'8 ]
            }
        }
        '''
        )

def test_rhythmmakertools_TieSpecifier_03():
    divisions = [(3, 8), (4, 4), (5, 16), (7, 8)]
    rhythm_maker = rhythmmakertools.EvenRunRhythmMaker(
        tie_specifier=rhythmmakertools.TieSpecifier(
            tie_consecutive_notes=True,
            ),
        )
    assert divisions[0] == (3, 8)
    selections = rhythm_maker(divisions)
    staff = Staff(selections)
    f(staff)
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                c'8 ~ [
                c'8 ~
                c'8 ~ ]
            }
            {
                c'4 ~
                c'4 ~
                c'4 ~
                c'4 ~
            }
            {
                c'16 ~ [
                c'16 ~
                c'16 ~
                c'16 ~
                c'16 ~ ]
            }
            {
                c'8 ~ [
                c'8 ~
                c'8 ~
                c'8 ~
                c'8 ~
                c'8 ~
                c'8 ]
            }
        }
        '''
        )

def test_rhythmmakertools_TieSpecifier_04():
    divisions = [(3, 8), (4, 4), (5, 16), (7, 8)]
    talea = rhythmmakertools.Talea(
        counts=[1,2,3,4,5],
        denominator=16
    )
    pattern = patterntools.select_every(indices=[2], period=3)
    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        tie_specifier=rhythmmakertools.TieSpecifier(
            tie_consecutive_notes=pattern,
            ),
        )
    selections = rhythm_maker(divisions)
    staff = Staff(selections)
    f(staff)
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'16 [
            c'8 ~
            c'8. ]
            c'4
            c'4 ~
            c'16 [
            c'16
            c'8 ~
            c'8.
            c'16 ]
            c'8. ~ [
            c'8 ]
            c'8. [
            c'16 ~
            c'8
            c'8. ]
            c'4 ~
            c'16
        }
        '''
        )
