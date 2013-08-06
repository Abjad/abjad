# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools
from abjad.tools import rhythmmakertools


def test_TaleaRhythmMaker___call___01():

    talea, talea_denominator, prolation_addenda = [-1, 4, -2, 3], 16, [3, 4]
    maker = rhythmmakertools.TaleaRhythmMaker(talea, talea_denominator, prolation_addenda)

    divisions = [(2, 8), (5, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 2/8
            \times 4/7 {
                r16
                c'4
                r8
            }
        }
        {
            \time 5/8
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 5/7 {
                c'8.
                r16
                c'4
                r8
                c'8.
                r16
            }
        }
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            {
                \time 2/8
                \times 4/7 {
                    r16
                    c'4
                    r8
                }
            }
            {
                \time 5/8
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 5/7 {
                    c'8.
                    r16
                    c'4
                    r8
                    c'8.
                    r16
                }
            }
        }
        '''
        )


def test_TaleaRhythmMaker___call___02():

    talea, talea_denominator, prolation_addenda = [-1, 4, -2, 3], 16, [3, 4]
    secondary_divisions = [6]
    maker = rhythmmakertools.TaleaRhythmMaker(talea, talea_denominator, prolation_addenda, secondary_divisions)

    divisions = [(2, 8), (5, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
    measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 2/8
            \times 4/7 {
                r16
                c'4
                r8
            }
        }
        {
            \time 5/8
            {
                c'8
            }
            \times 2/3 {
                c'16
                r16
                c'4
                r8
                c'16
            }
            {
                c'8
            }
        }
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            {
                \time 2/8
                \times 4/7 {
                    r16
                    c'4
                    r8
                }
            }
            {
                \time 5/8
                {
                    c'8
                }
                \times 2/3 {
                    c'16
                    r16
                    c'4
                    r8
                    c'16
                }
                {
                    c'8
                }
            }
        }
        '''
        )
