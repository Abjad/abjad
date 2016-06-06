# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_IncisedRhythmMaker___call___01():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-8],
        prefix_counts=[0, 1],
        suffix_talea=[-1],
        suffix_counts=[1],
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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


def test_rhythmmakertools_IncisedRhythmMaker___call___02():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-8],
        prefix_counts=[1, 2, 3, 4],
        suffix_talea=[-1],
        suffix_counts=[1],
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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


def test_rhythmmakertools_IncisedRhythmMaker___call___03():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-1],
        prefix_counts=[1],
        suffix_talea=[-8],
        suffix_counts=[1, 2, 3],
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    staff = Staff(scoretools.make_spacer_skip_measures(divisions))
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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


def test_rhythmmakertools_IncisedRhythmMaker___call___04():

    incise_specifier = rhythmmakertools.InciseSpecifier()

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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


def test_rhythmmakertools_IncisedRhythmMaker___call___05():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-1],
        prefix_counts=[1],
        suffix_talea=[-1],
        suffix_counts=[1],
        talea_denominator=8,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        extra_counts_per_division=[1, 0, 3],
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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


def test_rhythmmakertools_IncisedRhythmMaker___call___06():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-1],
        prefix_counts=[1],
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        extra_counts_per_division=[2, 0],
        split_divisions_by_counts=[20],
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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
                \tweak text #tuplet-number::calc-fraction-text
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


def test_rhythmmakertools_IncisedRhythmMaker___call___07():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[8],
        prefix_counts=[0, 1],
        suffix_talea=[1],
        suffix_counts=[1],
        talea_denominator=32,
        fill_with_notes=False,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 5/8
                r2
                r16.
                c'32
            }
            {
                c'4
                r4
                r16.
                c'32
            }
            {
                r2
                r16.
                c'32
            }
            {
                c'4
                r4
                r16.
                c'32
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___08():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[8],
        prefix_counts=[1, 2, 3, 4],
        suffix_talea=[1],
        suffix_counts=[1],
        talea_denominator=32,
        fill_with_notes=False,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 5/8
                c'4
                r4
                r16.
                c'32
            }
            {
                c'4
                c'4
                r16.
                c'32
            }
            {
                c'4
                c'4
                c'8
            }
            {
                c'4
                c'4
                c'8
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___09():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[1],
        prefix_counts=[1],
        suffix_talea=[8],
        suffix_counts=[1, 2, 3],
        talea_denominator=32,
        fill_with_notes=False,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 5/8
                c'32
                r4
                r16.
                c'4
            }
            {
                c'32
                r16.
                c'4
                c'4
            }
            {
                c'32
                c'4
                c'4
                c'16.
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___10():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        fill_with_notes=False,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 5/8
                r2
                r8
            }
            {
                r2
                r8
            }
            {
                r2
                r8
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___11():

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[1],
        prefix_counts=[1],
        suffix_talea=[1],
        suffix_counts=[1],
        talea_denominator=8,
        fill_with_notes=False,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        extra_counts_per_division=[1, 0, 3],
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 4/8
                \times 4/5 {
                    c'8
                    r4.
                    c'8
                }
            }
            {
                {
                    c'8
                    r4
                    c'8
                }
            }
            {
                \times 4/7 {
                    c'8
                    r2
                    r8
                    c'8
                }
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___12():
    r'''Adds 32nd note to beginning of every division.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[1],
        prefix_counts=[1],
        talea_denominator=32,
        fill_with_notes=False,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        extra_counts_per_division=[2, 0],
        split_divisions_by_counts=[20],
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 4/8
                \times 8/9 {
                    c'32
                    r2
                    r32
                }
            }
            {
                {
                    c'32
                    r16.
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/7 {
                    c'32
                    r4.
                    r32
                }
            }
            {
                {
                    c'32
                    r8..
                }
                \times 4/5 {
                    c'32
                    r4
                    r32
                }
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___13():
    r'''Incises outer divisions only.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-8],
        prefix_counts=[2],
        suffix_talea=[-3],
        suffix_counts=[4],
        talea_denominator=32,
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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


def test_rhythmmakertools_IncisedRhythmMaker___call___14():
    r'''Incises outer divisions only.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-1],
        prefix_counts=[20],
        suffix_talea=[-1],
        suffix_counts=[2],
        talea_denominator=4,
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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


def test_rhythmmakertools_IncisedRhythmMaker___call___15():
    r'''Unincised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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


def test_rhythmmakertools_IncisedRhythmMaker___call___16():
    r'''Incises outer divisions only.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-1],
        prefix_counts=[1],
        suffix_talea=[-1],
        suffix_counts=[1],
        talea_denominator=8,
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        extra_counts_per_division=[1, 0, 3],
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
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


def test_rhythmmakertools_IncisedRhythmMaker___call___17():
    r'''Incises outer divisions only.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[-1],
        prefix_counts=[1],
        suffix_talea=[-1],
        suffix_counts=[1],
        talea_denominator=8,
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        extra_counts_per_division=[1, 0, 0, 0, 2],
        split_divisions_by_counts=[3, 1, 4, 1, 3],
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 4/8
                \tweak text #tuplet-number::calc-fraction-text
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
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'2
                    r8
                }
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___18():
    r'''Incises outer divisions only. Fills with rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[8],
        prefix_counts=[2],
        suffix_talea=[3],
        suffix_counts=[4],
        talea_denominator=32,
        fill_with_notes=False,
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 5/8
                c'4
                c'4
                r8
            }
            {
                r2
                r8
            }
            {
                r4
                c'16. [
                c'16.
                c'16.
                c'16. ]
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___19():
    r'''Incises outer divisions only. Fills with rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[1],
        prefix_counts=[20],
        suffix_talea=[1],
        suffix_counts=[2],
        talea_denominator=4,
        fill_with_notes=False,
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 5/8
                c'4
                c'4
                c'8
            }
            {
                r2
                r8
            }
            {
                r8
                c'4
                c'4
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___20():
    r'''Unincised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        fill_with_notes=False,
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        )

    divisions = [(5, 8), (5, 8), (5, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 5/8
                r2
                r8
            }
            {
                r2
                r8
            }
            {
                r2
                r8
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___21():
    r'''Incises outer divisions only. Fills with rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[1],
        prefix_counts=[1],
        suffix_talea=[1],
        suffix_counts=[1],
        talea_denominator=8,
        fill_with_notes=False,
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        extra_counts_per_division=[1, 0, 3],
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 4/8
                \times 4/5 {
                    c'8
                    r2
                }
            }
            {
                {
                    r2
                }
            }
            {
                \times 4/7 {
                    r2.
                    c'8
                }
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___22():
    r'''Incises outer divisions only. Fills with rests:
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=[1],
        prefix_counts=[1],
        suffix_talea=[1],
        suffix_counts=[1],
        talea_denominator=8,
        fill_with_notes=False,
        outer_divisions_only=True,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        extra_counts_per_division=[1, 0, 0, 0, 2],
        split_divisions_by_counts=[3, 1, 4, 1, 3],
        )

    divisions = [(4, 8), (4, 8), (4, 8)]
    leaf_lists = maker(divisions)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 4/8
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    c'8
                    r4.
                }
                {
                    r8
                }
            }
            {
                {
                    r2
                }
            }
            {
                {
                    r8
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    r2
                    c'8
                }
            }
        }
        '''
        )
