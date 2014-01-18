# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_TaleaRhythmMaker_burnish_divisions_01():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        lefts=(-1,), 
        middles=(0,), 
        rights=(-1,), 
        left_lengths=(2,), 
        right_lengths=(1,),
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=(1, 1, 2, 4), 
        talea_denominator=32, 
        burnish_specifier=burnish_specifier,
        prolation_addenda=(0,),
        burnish_divisions=True,
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


def test_rhythmmakertools_TaleaRhythmMaker_burnish_divisions_02():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        lefts=(0,), 
        middles=(-1,), 
        rights=(0,), 
        left_lengths=(2,), 
        right_lengths=(1,),
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=(1, 1, 2, 4), 
        talea_denominator=32, 
        prolation_addenda=(0,),
        burnish_specifier=burnish_specifier,
        burnish_divisions=True,
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


def test_rhythmmakertools_TaleaRhythmMaker_burnish_divisions_03():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        lefts=(0,), 
        middles=(-1,), 
        rights=(0,), 
        left_lengths=(2,), 
        right_lengths=(1,),
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=(1, 1, 2, 4,), 
        talea_denominator=32, 
        prolation_addenda=(3,),
        burnish_specifier=burnish_specifier,
        burnish_divisions=True,
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


def test_rhythmmakertools_TaleaRhythmMaker_burnish_divisions_04():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        lefts=(-1,), 
        middles=(0,), 
        rights=(-1,), 
        left_lengths=(1,), 
        right_lengths=(1,),
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=(1, 1, 2, 4), 
        talea_denominator=32, 
        prolation_addenda=(0, 3),
        burnish_specifier=burnish_specifier,
        burnish_divisions=True,
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


def test_rhythmmakertools_TaleaRhythmMaker_burnish_divisions_05():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        lefts=(-1,), 
        middles=(0,), 
        rights=(-1,), 
        left_lengths=(1,), 
        right_lengths=(1,), 
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=(1, 1, 2, 4), 
        talea_denominator=32, 
        prolation_addenda=(0, 3),
        burnish_specifier=burnish_specifier,
        secondary_divisions=(14,),
        burnish_divisions=True,
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
