# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_DivisionBurnishedTaleaRhythmMaker___call___01():

    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
        talea=(1, 1, 2, 4), 
        talea_denominator=32, 
        prolation_addenda=(0,),
        lefts=(-1,), 
        middles=(0,), 
        rights=(-1,), 
        left_lengths=(2,), 
        right_lengths=(1,),
        )

    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(music)

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

    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
        talea=(1, 1, 2, 4), 
        talea_denominator=32, 
        prolation_addenda=(0,),
        lefts=(0,), 
        middles=(-1,), 
        rights=(0,), 
        left_lengths=(2,), 
        right_lengths=(1,),
        )

    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(music)

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

    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
        talea=(1, 1, 2, 4,), 
        talea_denominator=32, 
        prolation_addenda=(3,),
        lefts=(0,), 
        middles=(-1,), 
        rights=(0,), 
        left_lengths=(2,), 
        right_lengths=(1,),
        )

    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(music)

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

    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
        talea=(1, 1, 2, 4), 
        talea_denominator=32, 
        prolation_addenda=(0, 3),
        lefts=(-1,), 
        middles=(0,), 
        rights=(-1,), 
        left_lengths=(1,), 
        right_lengths=(1,),
        )

    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(music)

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

    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
        talea=(1, 1, 2, 4), 
        talea_denominator=32, 
        prolation_addenda=(0, 3),
        lefts=(-1,), 
        middles=(0,), 
        rights=(-1,), 
        left_lengths=(1,), 
        right_lengths=(1,), 
        secondary_divisions=(14,),
        )

    divisions = [(5, 16), (6, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(music)

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
