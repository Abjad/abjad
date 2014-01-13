# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_DivisionIncisedNoteRhythmMaker___call___01():

    maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
        prefix_talea=(-8,), 
        prefix_lengths=(0, 1), 
        suffix_talea=(-1,), 
        suffix_lengths=(1,), 
        talea_denominator=32,
        )

    divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(leaves)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/8
                c'2 ~
                c'16.
                r32
            }
            {
                r4
                c'4 ~
                c'16.
                r32
            }
            {
                c'2 ~
                c'16.
                r32
            }
            {
                r4
                c'4 ~
                c'16.
                r32
            }
        }
        '''
        )


def test_rhythmmakertools_DivisionIncisedNoteRhythmMaker___call___02():

    maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
        prefix_talea=(-8,), 
        prefix_lengths=(1, 2, 3, 4), 
        suffix_talea=(-1,), 
        suffix_lengths=(1,), 
        talea_denominator=32,
        )

    divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(leaves)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/8
                r4
                c'4 ~
                c'16.
                r32
            }
            {
                r4
                r4
                c'16.
                r32
            }
            {
                r4
                r4
                r8
            }
            {
                r4
                r4
                r8
            }
        }
        '''
        )


def test_rhythmmakertools_DivisionIncisedNoteRhythmMaker___call___03():

    maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
        prefix_talea=(-1,), 
        prefix_lengths=(1,), 
        suffix_talea=(-8,), 
        suffix_lengths=(1, 2, 3), 
        talea_denominator=32,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(leaves)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/8
                r32
                c'4 ~
                c'16.
                r4
            }
            {
                r32
                c'16.
                r4
                r4
            }
            {
                r32
                r4
                r4
                r16.
            }
        }
        '''
        )


def test_rhythmmakertools_DivisionIncisedNoteRhythmMaker___call___04():

    maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
        prefix_talea=(), 
        prefix_lengths=(0,), 
        suffix_talea=(), 
        suffix_lengths=(0,), 
        talea_denominator=8,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 5/8
                c'2 ~
                c'8
            }
            {
                c'2 ~
                c'8
            }
            {
                c'2 ~
                c'8
            }
        }
        '''
        )


def test_rhythmmakertools_DivisionIncisedNoteRhythmMaker___call___05():

    maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
        prefix_talea=(-1,), 
        prefix_lengths=(1,), 
        suffix_talea=(-1,), 
        suffix_lengths=(1,), 
        talea_denominator=8,
        prolation_addenda=(1, 0, 3),
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 4/8
                \times 4/5 {
                    r8
                    c'4.
                    r8
                }
            }
            {
                {
                    r8
                    c'4
                    r8
                }
            }
            {
                \times 4/7 {
                    r8
                    c'2 ~
                    c'8
                    r8
                }
            }
        }
        '''
        )


def test_rhythmmakertools_DivisionIncisedNoteRhythmMaker___call___06():

    maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
        prefix_talea=(-1,),
        prefix_lengths=(1,),
        suffix_talea=(),
        suffix_lengths=(0,),
        talea_denominator=32,
        prolation_addenda=(2, 0),
        secondary_divisions=(20,),
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 4/8
                \times 8/9 {
                    r32
                    c'2 ~
                    c'32
                }
            }
            {
                {
                    r32
                    c'16.
                }
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 6/7 {
                    r32
                    c'4. ~
                    c'32
                }
            }
            {
                {
                    r32
                    c'8..
                }
                \times 4/5 {
                    r32
                    c'4 ~
                    c'32
                }
            }
        }
        '''
        )
