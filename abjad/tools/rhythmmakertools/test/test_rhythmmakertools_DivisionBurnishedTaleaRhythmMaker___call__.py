# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools
from abjad.tools import rhythmmakertools


def test_rhythmmakertools_DivisionBurnishedTaleaRhythmMaker___call___01():

    talea, talea_denominator, prolation_addenda = [1, 1, 2, 4], 32, [0]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [2], [1]
    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(talea, talea_denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)

    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips(divisions))
    scoretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            {
                r32
                r32
                c'16
                c'8
                c'32
                r32
            }
        }
        {
            \time 6/16
            {
                r16
                r8
                c'32
                c'32
                c'16
                r16
            }
        }
    }
    '''

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/16
                {
                    r32
                    r32
                    c'16
                    c'8
                    c'32
                    r32
                }
            }
            {
                \time 6/16
                {
                    r16
                    r8
                    c'32
                    c'32
                    c'16
                    r16
                }
            }
        }
        '''
        )


def test_rhythmmakertools_DivisionBurnishedTaleaRhythmMaker___call___02():

    talea, talea_denominator, prolation_addenda = [1, 1, 2, 4], 32, [0]
    lefts, middles, rights = [0], [-1], [0]
    left_lengths, right_lengths = [2], [1]
    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(talea, talea_denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)
    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips(divisions))
    scoretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            {
                c'32
                c'32
                r16
                r8
                r32
                c'32
            }
        }
        {
            \time 6/16
            {
                c'16
                c'8
                r32
                r32
                r16
                c'16
            }
        }
    }
    '''

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/16
                {
                    c'32
                    c'32
                    r16
                    r8
                    r32
                    c'32
                }
            }
            {
                \time 6/16
                {
                    c'16
                    c'8
                    r32
                    r32
                    r16
                    c'16
                }
            }
        }
        '''
        )


def test_rhythmmakertools_DivisionBurnishedTaleaRhythmMaker___call___03():

    talea, talea_denominator, prolation_addenda = [1, 1, 2, 4], 32, [3]
    lefts, middles, rights = [0], [-1], [0]
    left_lengths, right_lengths = [2], [1]
    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(talea, talea_denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)
    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips(divisions))
    scoretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 10/13 {
                c'32
                c'32
                r16
                r8
                r32
                r32
                r16
                c'32
            }
        }
        {
            \time 6/16
            \times 4/5 {
                c'16.
                c'32
                r32
                r16
                r8
                r32
                r32
                c'16
            }
        }
    }
    '''

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/16
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 10/13 {
                    c'32
                    c'32
                    r16
                    r8
                    r32
                    r32
                    r16
                    c'32
                }
            }
            {
                \time 6/16
                \times 4/5 {
                    c'16.
                    c'32
                    r32
                    r16
                    r8
                    r32
                    r32
                    c'16
                }
            }
        }
        '''
        )


def test_rhythmmakertools_DivisionBurnishedTaleaRhythmMaker___call___04():

    talea, talea_denominator, prolation_addenda = [1, 1, 2, 4], 32, [0, 3]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [1]
    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(talea, talea_denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)
    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips(divisions))
    scoretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            {
                r32
                c'32
                c'16
                c'8
                c'32
                r32
            }
        }
        {
            \time 6/16
            \times 4/5 {
                r16
                c'8
                c'32
                c'32
                c'16
                c'8
                r32
            }
        }
    }
    '''

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/16
                {
                    r32
                    c'32
                    c'16
                    c'8
                    c'32
                    r32
                }
            }
            {
                \time 6/16
                \times 4/5 {
                    r16
                    c'8
                    c'32
                    c'32
                    c'16
                    c'8
                    r32
                }
            }
        }
        '''
        )


def test_rhythmmakertools_DivisionBurnishedTaleaRhythmMaker___call___05():

    talea, talea_denominator, prolation_addenda = [1, 1, 2, 4], 32, [0, 3]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [1]
    secondary_divisions = [14]
    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(talea, talea_denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths, secondary_divisions)

    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips(divisions))
    scoretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 5/16
            {
                r32
                c'32
                c'16
                c'8
                c'32
                r32
            }
        }
        {
            \time 6/16
            \times 4/7 {
                r16
                c'8
                r32
            }
            {
                r32
                c'16
                c'8
                r32
            }
        }
    }
    '''

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/16
                {
                    r32
                    c'32
                    c'16
                    c'8
                    c'32
                    r32
                }
            }
            {
                \time 6/16
                \times 4/7 {
                    r16
                    c'8
                    r32
                }
                {
                    r32
                    c'16
                    c'8
                    r32
                }
            }
        }
        '''
        )
