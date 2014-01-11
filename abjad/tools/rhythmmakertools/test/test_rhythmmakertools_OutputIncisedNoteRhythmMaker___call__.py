# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_OutputIncisedNoteRhythmMaker___call___01():

    prefix_talea, prefix_lengths = [-8], [2]
    suffix_talea, suffix_lengths = [-3], [4]
    talea_denominator = 32
    maker = rhythmmakertools.OutputIncisedNoteRhythmMaker(
        prefix_talea, 
        prefix_lengths, 
        suffix_talea, 
        suffix_lengths, 
        talea_denominator,
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
                r4
                r4
                c'8
            }
            {
                c'2 ~
                c'8
            }
            {
                c'4
                r16.
                r16.
                r16.
                r16.
            }
        }
        '''
        )


def test_rhythmmakertools_OutputIncisedNoteRhythmMaker___call___02():

    prefix_talea, prefix_lengths = [-1], [20]
    suffix_talea, suffix_lengths = [-1], [2]
    talea_denominator = 4
    maker = rhythmmakertools.OutputIncisedNoteRhythmMaker(
        prefix_talea, 
        prefix_lengths, 
        suffix_talea, 
        suffix_lengths, 
        talea_denominator,
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
                r4
                r4
                r8
            }
            {
                c'2 ~
                c'8
            }
            {
                c'8
                r4
                r4
            }
        }
        '''
        )


def test_rhythmmakertools_OutputIncisedNoteRhythmMaker___call___03():

    prefix_talea, prefix_lengths = [], [0]
    suffix_talea, suffix_lengths = [], [0]
    talea_denominator = 4
    maker = rhythmmakertools.OutputIncisedNoteRhythmMaker(
        prefix_talea, 
        prefix_lengths, 
        suffix_talea, 
        suffix_lengths, 
        talea_denominator,
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


def test_rhythmmakertools_OutputIncisedNoteRhythmMaker___call___04():

    prefix_talea, prefix_lengths = [-1], [1]
    suffix_talea, suffix_lengths = [-1], [1]
    talea_denominator = 8
    prolation_addenda = [1, 0, 3]
    maker = rhythmmakertools.OutputIncisedNoteRhythmMaker(
        prefix_talea, 
        prefix_lengths, 
        suffix_talea, 
        suffix_lengths, 
        talea_denominator,
        prolation_addenda=prolation_addenda,
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
                    c'2
                }
            }
            {
                {
                    c'2
                }
            }
            {
                \times 4/7 {
                    c'2.
                    r8
                }
            }
        }
        '''
        )


def test_rhythmmakertools_OutputIncisedNoteRhythmMaker___call___05():

    prefix_talea, prefix_lengths = [-1], [1]
    suffix_talea, suffix_lengths = [-1], [1]
    talea_denominator = 8
    prolation_addenda =    [1, 0, 0, 0, 2]
    secondary_divisions = [3, 1, 4, 1, 3]
    maker = rhythmmakertools.OutputIncisedNoteRhythmMaker(
        prefix_talea, 
        prefix_lengths, 
        suffix_talea, 
        suffix_lengths, 
        talea_denominator,
        prolation_addenda=prolation_addenda, 
        secondary_divisions=secondary_divisions,
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
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    r8
                    c'4.
                }
                {
                    c'8
                }
            }
            {
                {
                    c'2
                }
            }
            {
                {
                    c'8
                }
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'2
                    r8
                }
            }
        }
        '''
        )
