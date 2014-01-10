# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_OutputBurnishedTaleaRhythmMaker___call___01():

    talea, talea_denominator, prolation_addenda = [1], 16, [2]
    lefts, middles, rights = [0], [-1], [0]
    left_lengths, right_lengths = [1], [1]
    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea, 
        talea_denominator, 
        prolation_addenda,
        lefts, 
        middles, 
        rights, 
        left_lengths, 
        right_lengths,
        )

    divisions = [(3, 16), (3, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(music)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/16
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'16
                    r16
                    r16
                    r16
                    r16
                }
            }
            {
                \time 3/8
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    r16
                    r16
                    r16
                    r16
                    r16
                    r16
                    r16
                    c'16
                }
            }
        }
        '''
        )


def test_rhythmmakertools_OutputBurnishedTaleaRhythmMaker___call___02():

    talea, talea_denominator, prolation_addenda = [1], 4, [2]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [1]
    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea, talea_denominator, prolation_addenda,
        lefts, middles, rights, left_lengths, right_lengths)

    divisions = [(3, 16), (3, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(music)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/16
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    r4
                    c'16
                }
            }
            {
                \time 3/8
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    c'8.
                    c'4
                    r16
                }
            }
        }
        '''
        )


def test_rhythmmakertools_OutputBurnishedTaleaRhythmMaker___call___03():

    talea, talea_denominator, prolation_addenda = [1, 2, 3], 16, [0, 2]
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [1]
    secondary_divisions = [9]
    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea, 
        talea_denominator, 
        prolation_addenda,
        lefts, 
        middles, 
        rights, 
        left_lengths, 
        right_lengths, 
        secondary_divisions,
        )

    divisions = [(3, 8), (4, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(music)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/8
                {
                    r16
                    c'8
                    c'8.
                }
            }
            {
                \time 4/8
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'16
                    c'8
                    c'8
                }
                {
                    c'16
                    c'16
                    c'8
                    r16
                }
            }
        }
        '''
        )


def test_rhythmmakertools_OutputBurnishedTaleaRhythmMaker___call___04():

    talea, talea_denominator, prolation_addenda  = [1], 8, []
    lefts, middles, rights = [-1], [0], [-1]
    left_lengths, right_lengths = [1], [2]
    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea, 
        talea_denominator, 
        prolation_addenda,
        lefts, 
        middles, 
        rights,
        left_lengths, 
        right_lengths,
        )

    divisions = [(8, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(music)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 8/8
                r8
                c'8
                c'8
                c'8
                c'8
                c'8
                r8
                r8
            }
        }
        '''
        )
