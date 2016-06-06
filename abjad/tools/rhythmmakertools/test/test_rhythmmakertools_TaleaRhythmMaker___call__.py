# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_TaleaRhythmMaker___call___01():

    talea = rhythmmakertools.Talea(
        counts=(-1, 4, -2, 3),
        denominator=16,
        )
    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=(3, 4),
        )

    divisions = [(2, 8), (5, 8)]
    selections = rhythm_maker(divisions)

    selections = sequencetools.flatten_sequence(selections)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(selections)

    assert format(staff) == stringtools.normalize(
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
                \tweak text #tuplet-number::calc-fraction-text
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

    talea = rhythmmakertools.Talea(
        counts=(-1, 4, -2, 3),
        denominator=16,
        )
    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=(3, 4),
        split_divisions_by_counts=(6,),
        )

    divisions = [(2, 8), (5, 8)]
    selections = rhythm_maker(divisions)

    selections = sequencetools.flatten_sequence(selections)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(selections)

    assert format(staff) == stringtools.normalize(
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
                    c'8 ~
                }
                \times 2/3 {
                    c'16
                    r16
                    c'4
                    r8
                    c'16 ~
                }
                {
                    c'8
                }
            }
        }
        '''
        )