# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_TaleaRhythmMaker___call___01():

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=[-1, 4, -2, 3], 
        talea_denominator=16, 
        prolation_addenda=[3, 4],
        )

    divisions = [(2, 8), (5, 8)]
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


def test_rhythmmakertools_TaleaRhythmMaker___call___02():

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=[-1, 4, -2, 3], 
        talea_denominator=16, 
        prolation_addenda=[3, 4], 
        secondary_divisions=[6],
        )

    divisions = [(2, 8), (5, 8)]
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
