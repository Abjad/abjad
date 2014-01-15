# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_IncisedRhythmMaker___call___01():
    r'''Division-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(-8,), 
        prefix_lengths=(0, 1), 
        suffix_talea=(-1,), 
        suffix_lengths=(1,), 
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=True,
        incise_divisions=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___02():
    r'''Division-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(-8,), 
        prefix_lengths=(1, 2, 3, 4), 
        suffix_talea=(-1,), 
        suffix_lengths=(1,), 
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=True,
        incise_divisions=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___03():
    r'''Division-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(-1,), 
        prefix_lengths=(1,), 
        suffix_talea=(-8,), 
        suffix_lengths=(1, 2, 3), 
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=True,
        incise_divisions=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___04():
    r'''Division-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(), 
        prefix_lengths=(0,), 
        suffix_talea=(), 
        suffix_lengths=(0,), 
        talea_denominator=8,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=True,
        incise_divisions=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___05():
    r'''Division-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(-1,), 
        prefix_lengths=(1,), 
        suffix_talea=(-1,), 
        suffix_lengths=(1,), 
        talea_denominator=8,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        prolation_addenda=(1, 0, 3),
        fill_with_notes=True,
        incise_divisions=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___06():
    r'''Division-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(-1,),
        prefix_lengths=(1,),
        suffix_talea=(),
        suffix_lengths=(0,),
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        prolation_addenda=(2, 0),
        secondary_divisions=(20,),
        fill_with_notes=True,
        incise_divisions=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___07():
    r'''Division-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(8,), 
        prefix_lengths=(0, 1), 
        suffix_talea=(1,), 
        suffix_lengths=(1,), 
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=False,
        incise_divisions=True,
        )

    divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
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
    r'''Division-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(8,), 
        prefix_lengths=(1, 2, 3, 4), 
        suffix_talea=(1,), 
        suffix_lengths=(1,), 
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=False,
        incise_divisions=True,
        )

    divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
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
    r'''Division-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(1,), 
        prefix_lengths=(1,), 
        suffix_talea=(8,), 
        suffix_lengths=(1, 2, 3), 
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=False,
        incise_divisions=True,
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
    r'''Division-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(), 
        prefix_lengths=(0,), 
        suffix_talea=(), 
        suffix_lengths=(0,), 
        talea_denominator=8,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=False,
        incise_divisions=True,
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
    r'''Division-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(1,), 
        prefix_lengths=(1,), 
        suffix_talea=(1,), 
        suffix_lengths=(1,), 
        talea_denominator=8,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        prolation_addenda=(1, 0, 3),
        fill_with_notes=False,
        incise_divisions=True,
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
    r'''Division-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(1,),
        prefix_lengths=(1,),
        suffix_talea=(),
        suffix_lengths=(0,),
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        prolation_addenda=(2, 0),
        secondary_divisions=(20,),
        fill_with_notes=False,
        incise_divisions=True,
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
                \tweak #'text #tuplet-number::calc-fraction-text
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
    r'''Output-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(-8,), 
        prefix_lengths=(2,), 
        suffix_talea=(-3,), 
        suffix_lengths=(4,), 
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=True,
        incise_output=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___14():
    r'''Output-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(-1,), 
        prefix_lengths=(20,), 
        suffix_talea=(-1,), 
        suffix_lengths=(2,), 
        talea_denominator=4,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=True,
        incise_output=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___15():
    r'''Output-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(), 
        prefix_lengths=(0,), 
        suffix_talea=(), 
        suffix_lengths=(0,), 
        talea_denominator=4,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=True,
        incise_output=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___16():
    r'''Output-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(-1,), 
        prefix_lengths=(1,), 
        suffix_talea=(-1,), 
        suffix_lengths=(1,), 
        talea_denominator=8,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        prolation_addenda=(1, 0, 3),
        fill_with_notes=True,
        incise_output=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___17():
    r'''Output-incised notes.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(-1,), 
        prefix_lengths=(1,), 
        suffix_talea=(-1,), 
        suffix_lengths=(1,), 
        talea_denominator=8,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        prolation_addenda=(1, 0, 0, 0, 2), 
        secondary_divisions=(3, 1, 4, 1, 3),
        fill_with_notes=True,
        incise_output=True,
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


def test_rhythmmakertools_IncisedRhythmMaker___call___18():
    r'''Output-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(8,), 
        prefix_lengths=(2,), 
        suffix_talea=(3,), 
        suffix_lengths=(4,), 
        talea_denominator=32,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=False,
        incise_output=True,
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
                c'16.
                c'16.
                c'16.
                c'16.
            }
        }
        '''
        )


def test_rhythmmakertools_IncisedRhythmMaker___call___19():
    r'''Output-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(1,), 
        prefix_lengths=(20,), 
        suffix_talea=(1,), 
        suffix_lengths=(2,), 
        talea_denominator=4,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=False,
        incise_output=True,
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
    r'''Output-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(), 
        prefix_lengths=(0,), 
        suffix_talea=(), 
        suffix_lengths=(0,), 
        talea_denominator=4,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        fill_with_notes=False,
        incise_output=True,
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
    r'''Output-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(1,), 
        prefix_lengths=(1,), 
        suffix_talea=(1,), 
        suffix_lengths=(1,), 
        talea_denominator=8,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        prolation_addenda=(1, 0, 3),
        fill_with_notes=False,
        incise_output=True,
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
    r'''Output-incised rests.
    '''

    incise_specifier = rhythmmakertools.InciseSpecifier(
        prefix_talea=(1,), 
        prefix_lengths=(1,), 
        suffix_talea=(1,), 
        suffix_lengths=(1,), 
        talea_denominator=8,
        )

    maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=incise_specifier,
        prolation_addenda=(1, 0, 0, 0, 2), 
        secondary_divisions=(3, 1, 4, 1, 3),
        fill_with_notes=False,
        incise_output=True,
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
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    r2
                    c'8
                }
            }
        }
        '''
        )
