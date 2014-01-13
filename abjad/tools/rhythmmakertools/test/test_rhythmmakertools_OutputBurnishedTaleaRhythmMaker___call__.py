# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_OutputBurnishedTaleaRhythmMaker___call___01():

    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea=(1,), 
        talea_denominator=16, 
        prolation_addenda=(2,),
        lefts=(0,), 
        middles=(-1,), 
        rights=(0,), 
        left_lengths=(1,), 
        right_lengths=(1,),
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

    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea=(1,), 
        talea_denominator=4, 
        prolation_addenda=(2,),
        lefts=(-1,), 
        middles=(0,), 
        rights=(-1,), 
        left_lengths=(1,), 
        right_lengths=(1,),
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

    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea=(1, 2, 3), 
        talea_denominator=16, 
        prolation_addenda=(0, 2),
        lefts=(-1,), 
        middles=(0,), 
        rights=(-1,), 
        left_lengths=(1,), 
        right_lengths=(1,), 
        secondary_divisions=(9,),
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

    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        talea=(1,), 
        talea_denominator=8, 
        prolation_addenda=(),
        lefts=(-1,), 
        middles=(0,), 
        rights=(-1,),
        left_lengths=(1,), 
        right_lengths=(2,),
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
