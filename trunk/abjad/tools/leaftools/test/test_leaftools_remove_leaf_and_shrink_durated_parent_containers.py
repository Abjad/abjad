# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_01():
    r'''Excise leaf from tuplet and measure.
    '''

    measure = Measure((4, 4), tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(measure)

    r'''
    {
        \time 4/4
        \times 2/3 {
            c'4
            d'4
            e'4
        }
        \times 2/3 {
            f'4
            g'4
            a'4
        }
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(measure.select_leaves()[0])

    r'''
    {
        \time 5/6
        \scaleDurations #'(2 . 3) {
            {
                d'4
                e'4
            }
            {
                f'4
                g'4
                a'4
            }
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 5/6
            \scaleDurations #'(2 . 3) {
                {
                    d'4
                    e'4
                }
                {
                    f'4
                    g'4
                    a'4
                }
            }
        }
        '''
        )


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_02():
    r'''Excise leaf from tuplet and measure.
    '''

    measure = Measure((4, 4), tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 5) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(measure)

    r'''
    {
        \time 4/4
        \times 4/5 {
            c'8
            d'8
            e'8
            f'8
            g'8
        }
        \times 4/5 {
            a'8
            b'8
            c''8
            d''8
            e''8
        }
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(measure.select_leaves()[0])

    r'''
    {
        \time 9/10
        \scaleDurations #'(4 . 5) {
            {
                d'8
                e'8
                f'8
                g'8
            }
            {
                a'8
                b'8
                c''8
                d''8
                e''8
            }
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 9/10
            \scaleDurations #'(4 . 5) {
                {
                    d'8
                    e'8
                    f'8
                    g'8
                }
                {
                    a'8
                    b'8
                    c''8
                    d''8
                    e''8
                }
            }
        }
        '''
        )


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_03():
    r'''Excise leaf from tuplet and measure.
    '''

    measure = Measure((5, 6), [
        tuplettools.FixedDurationTuplet(Duration(3, 4), Note("c'4") * 5),
        tuplettools.FixedDurationTuplet(Duration(4, 8), Note(0, (1, 8)) * 7),
        ])

    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(measure)

    r'''
    {
        \time 5/6
        \scaleDurations #'(2 . 3) {
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/5 {
                c'4
                d'4
                e'4
                f'4
                g'4
            }
            \times 4/7 {
                a'8
                b'8
                c''8
                d''8
                e''8
                f''8
                g''8
            }
        }
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(measure.select_leaves()[0])

    r'''
    {
        \time 11/15
        \scaleDurations #'(8 . 15) {
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/4 {
                d'4
                e'4
                f'4
                g'4
            }
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 5/7 {
                a'8
                b'8
                c''8
                d''8
                e''8
                f''8
                g''8
            }
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 11/15
            \scaleDurations #'(8 . 15) {
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    d'4
                    e'4
                    f'4
                    g'4
                }
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 5/7 {
                    a'8
                    b'8
                    c''8
                    d''8
                    e''8
                    f''8
                    g''8
                }
            }
        }
        '''
        )


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_04():
    r'''Excise leaf that conflicts with time signature duration;
    change time signature denominator and reset tuplet target durations.
    '''

    measure = Measure((5, 6), [
        tuplettools.FixedDurationTuplet(Duration(3, 4), Note("c'4") * 5),
        tuplettools.FixedDurationTuplet(Duration(4, 8), Note(0, (1, 8)) * 7),
        ])

    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(measure)

    r'''
    \time 5/6
        \compressMusic #'(2 . 3) {
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/5 {
                c'4
                cs'4
                d'4
                ef'4
                e'4
            }
            \times 4/7 {
                f'8
                fs'8
                g'8
                af'8
                a'8
                bf'8
                b'8
            }
        }
        '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(measure.select_leaves()[-1])

    r'''
    \time 11/14
        \compressMusic #'(4 . 7) {
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 7/10 {
                c'4
                cs'4
                d'4
                ef'4
                e'4
            }
            \times 2/3 {
                f'8
                fs'8
                g'8
                af'8
                a'8
                bf'8
            }
        }
        '''

    assert isinstance(measure, Measure)
    assert measure.time_signature == contexttools.TimeSignatureMark((11, 14))
    assert len(measure) == 2
    tuplet = measure[0]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 5
    assert tuplet.target_duration == Duration(7, 8)
    assert inspect(tuplet).get_duration() == Duration(2, 4)
    note = measure[0][0]
    assert note.written_duration == Duration(1, 4)
    assert inspect(note).get_duration() == Duration(1, 10)
    tuplet = measure[1]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 6
    assert tuplet.target_duration == Duration(4, 8)
    assert inspect(tuplet).get_duration() == Duration(2, 7)
    note = measure[1][0]
    assert note.written_duration == Duration(1, 8)
    assert inspect(note).get_duration() == Duration(1, 21)
    assert select(measure).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_05():
    r'''Excise leaf that conflicts with time signature duration;
    trigger tuplet insertion.
    '''

    measure = Measure((5, 6),
        [tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(7))] +
            notetools.make_repeated_notes(3, (1, 4)))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(measure)

    r'''
    \time 5/6
        \compressMusic #'(2 . 3) {
            \times 4/7 {
                c'8
                cs'8
                d'8
                ef'8
                e'8
                f'8
                fs'8
            }
            g'4
            af'4
            a'4
        }
        '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(measure.select_leaves()[0])

    r'''
    \time 11/14
        \compressMusic #'(4 . 7) {
            \times 2/3 {
                cs'8
                d'8
                ef'8
                e'8
                f'8
                fs'8
            }
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 7/6 {
                g'4
            }
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 7/6 {
                af'4
            }
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 7/6 {
                a'4
            }
        }
        '''

    assert isinstance(measure, Measure)
    assert measure.time_signature == contexttools.TimeSignatureMark((11, 14))
    assert len(measure) == 4
    tuplet = measure[0]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 6
    assert tuplet.target_duration == Duration(2, 4)
    assert inspect(tuplet).get_duration() == Duration(2, 7)
    note = measure[0][0]
    assert note.written_duration == Duration(1, 8)
    assert inspect(note).get_duration() == Duration(1, 21)
    tuplet = measure[1]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 1
    assert tuplet.target_duration == Duration(7, 24)
    assert inspect(tuplet).get_duration() == Duration(1, 6)
    note = measure[1][0]
    assert note.written_duration == Duration(1, 4)
    assert inspect(note).get_duration() == Duration(1, 6)
    assert select(measure).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_06():
    r'''Excise leaf that matches time signature duration;
    does not trigger trivial 1:1 tuplet insertion.
    '''

    measure = Measure((5, 6),
        [tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(7))] +
            notetools.make_repeated_notes(3, (1, 4)))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(measure)

    r'''
    \time 5/6
        \compressMusic #'(2 . 3) {
            \times 4/7 {
                c'8
                cs'8
                d'8
                ef'8
                e'8
                f'8
                fs'8
            }
            g'4
            af'4
            a'4
        }
        '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(measure.select_leaves()[-1])

    r'''
    \time 4/6
        \scaleDurations #'(2 . 3) {
            \times 4/7 {
                c'8
                cs'8
                d'8
                ef'8
                e'8
                f'8
                fs'8
            }
            g'4
            af'4
        }
        '''

    assert isinstance(measure, Measure)
    assert measure.time_signature == contexttools.TimeSignatureMark((4, 6))
    assert len(measure) == 3
    tuplet = measure[0]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 7
    assert tuplet.target_duration == Duration(2, 4)
    assert inspect(tuplet).get_duration() == Duration(2, 6)
    note = measure[0][0]
    assert note.written_duration == Duration(1, 8)
    assert inspect(note).get_duration() == Duration(1, 21)
    note = measure[1]
    assert note.written_duration == Duration(1, 4)
    assert inspect(note).get_duration() == Duration(1, 6)
    assert select(measure).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_07():
    r'''Nested fixed-duration tuplet.
    '''

    measure = Measure((4, 4), [
        tuplettools.FixedDurationTuplet(Duration(2, 2), [Note(0, (1, 2)), Note(1, (1, 2)),
        tuplettools.FixedDurationTuplet(Duration(2, 4), [Note(i, (1, 4)) for i in range(2, 5)])])])

    r'''
    \time 4/4
        \times 2/3 {
            c'2
            cs'2
            \times 2/3 {
                            d'4
                            ef'4
                            e'4
            }
        }
        '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(measure.select_leaves()[-1])
    measure = measure
    assert isinstance(measure, Measure)
    assert measure.time_signature == contexttools.TimeSignatureMark((8, 9))
    assert len(measure) == 1
    tuplet = measure[0]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 3
    assert tuplet.target_duration == Duration(1)
    assert inspect(tuplet).get_duration() == Duration(8, 9)
    assert tuplet.multiplier == Duration(3, 4)
    note = measure[0][0]
    assert isinstance(note, Note)
    assert note.written_duration == Duration(1, 2)
    assert inspect(note).get_duration() == Duration(1, 3)
    tuplet = measure[0][-1]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 2
    assert tuplet.target_duration == Duration(1, 3)
    assert inspect(tuplet).get_duration() == Duration(2, 9)
    assert tuplet.multiplier == Duration(2, 3)
    note = measure[0][-1][0]
    assert isinstance(note, Note)
    assert note.written_duration == Duration(1, 4)
    assert inspect(note).get_duration() == Duration(1, 9)

    r'''
    \time 8/9
        \compressMusic #'(8 . 9) {
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'2
                cs'2
                \times 2/3 {
                    d'4
                    ef'4
                }
            }
        }
    '''


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_08():
    r'''Exicse plain vanilla container.
    '''

    container = Container(Note("c'4") * 6)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(container.select_leaves()[0])
    assert isinstance(container, Container)
    assert len(container) == 5
    assert container._preprolated_duration == Duration(5, 4)
    assert inspect(container).get_duration() == Duration(5, 4)
    assert isinstance(container[0], Note)
    assert container[0].written_duration == Duration(1, 4)
    assert inspect(container[0]).get_duration() == Duration(1, 4)
    assert select(container).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_09():
    r'''Container container.
    '''

    container = Container(Note("c'4") * 6)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(container.select_leaves()[0])
    assert isinstance(container, Container)
    assert len(container) == 5
    assert container._preprolated_duration == Duration(5, 4)
    assert inspect(container).get_duration() == Duration(5, 4)
    assert isinstance(container[0], Note)
    assert container[0].written_duration == Duration(1, 4)
    assert inspect(container[0]).get_duration() == Duration(1, 4)
    assert select(container).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_10():
    r'''Excise voice.
    '''

    voice = Voice(Note("c'4") * 6)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(voice.select_leaves()[0])
    assert isinstance(voice, Voice)
    assert len(voice) == 5
    assert voice._preprolated_duration == Duration(5, 4)
    assert inspect(voice).get_duration() == Duration(5, 4)
    assert isinstance(voice[0], Note)
    assert voice[0].written_duration == Duration(1, 4)
    assert inspect(voice[0]).get_duration() == Duration(1, 4)
    assert select(voice).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_11():
    r'''Staff.
    '''

    staff = Staff(Note("c'4") * 6)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(staff.select_leaves()[0])
    assert isinstance(staff, Staff)
    assert len(staff) == 5
    assert staff._preprolated_duration == Duration(5, 4)
    assert inspect(staff).get_duration() == Duration(5, 4)
    assert isinstance(staff[0], Note)
    assert staff[0].written_duration == Duration(1, 4)
    assert inspect(staff[0]).get_duration() == Duration(1, 4)
    assert select(staff).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_12():
    r'''Container.
    '''

    container = Container(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(container[0])
    assert isinstance(container, Container)
    assert len(container) == 1
    assert container._preprolated_duration == Duration(2, 4)
    assert inspect(container).get_duration() == Duration(2, 4)
    assert isinstance(container[0], tuplettools.FixedDurationTuplet)
    assert container[0].target_duration == Duration(2, 4)
    assert inspect(container[0]).get_duration() == Duration(2, 4)
    assert isinstance(container[0][0], Note)
    assert container[0][0].written_duration == Duration(1, 4)
    assert inspect(container[0][0]).get_duration() == Duration(1, 6)
    assert select(container).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_13():
    r'''Container.
    '''

    container = Container(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(container[0])
    assert isinstance(container, Container)
    assert len(container) == 1
    assert container._preprolated_duration == Duration(2, 4)
    assert inspect(container).get_duration() == Duration(2, 4)
    assert isinstance(container[0], tuplettools.FixedDurationTuplet)
    assert container[0].target_duration == Duration(2, 4)
    assert inspect(container[0]).get_duration() == Duration(2, 4)
    assert isinstance(container[0][0], Note)
    assert container[0][0].written_duration == Duration(1, 4)
    assert inspect(container[0][0]).get_duration() == Duration(1, 6)
    assert select(container).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_14():
    r'''Excise voice.
    '''

    voice = Voice(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(voice[0])
    assert isinstance(voice, Voice)
    assert len(voice) == 1
    assert voice._preprolated_duration == Duration(2, 4)
    assert inspect(voice).get_duration() == Duration(2, 4)
    assert isinstance(voice[0], tuplettools.FixedDurationTuplet)
    assert voice[0].target_duration == Duration(2, 4)
    assert inspect(voice[0]).get_duration() == Duration(2, 4)
    assert isinstance(voice[0][0], Note)
    assert voice[0][0].written_duration == Duration(1, 4)
    assert inspect(voice[0][0]).get_duration() == Duration(1, 6)
    assert select(voice).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_15():
    r'''Excise staff.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(staff[0])
    assert isinstance(staff, Staff)
    assert len(staff) == 1
    assert staff._preprolated_duration == Duration(2, 4)
    assert inspect(staff).get_duration() == Duration(2, 4)
    assert isinstance(staff[0], tuplettools.FixedDurationTuplet)
    assert staff[0].target_duration == Duration(2, 4)
    assert inspect(staff[0]).get_duration() == Duration(2, 4)
    assert isinstance(staff[0][0], Note)
    assert staff[0][0].written_duration == Duration(1, 4)
    assert inspect(staff[0][0]).get_duration() == Duration(1, 6)
    assert select(staff).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_16():
    r'''Excise container.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(staff.select_leaves()[0])
    assert isinstance(staff, Staff)
    assert len(staff) == 2
    assert staff._preprolated_duration == Duration(5, 6)
    assert inspect(staff).get_duration() == Duration(5, 6)
    assert isinstance(staff[0], tuplettools.FixedDurationTuplet)
    assert staff[0].target_duration == Duration(2, 6)
    assert inspect(staff[0]).get_duration() == Duration(2, 6)
    assert isinstance(staff[0][0], Note)
    assert staff[0][0].written_duration == Duration(1, 4)
    assert inspect(staff[0][0]).get_duration() == Duration(1, 6)
    assert select(staff).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_17():
    r'''Excise container.
    '''

    container = Container(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(container.select_leaves()[0])
    assert isinstance(container, Container)
    assert len(container) == 2
    assert container._preprolated_duration == Duration(5, 6)
    assert inspect(container).get_duration() == Duration(5, 6)
    assert isinstance(container[0], tuplettools.FixedDurationTuplet)
    assert container[0].target_duration == Duration(2, 6)
    assert inspect(container[0]).get_duration() == Duration(2, 6)
    assert isinstance(container[0][0], Note)
    assert container[0][0].written_duration == Duration(1, 4)
    assert inspect(container[0][0]).get_duration() == Duration(1, 6)
    assert select(container).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_18():
    r'''Excise voice.
    '''

    voice = Voice(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(voice.select_leaves()[0])
    assert isinstance(voice, Voice)
    assert len(voice) == 2
    assert voice._preprolated_duration == Duration(5, 6)
    assert inspect(voice).get_duration() == Duration(5, 6)
    assert isinstance(voice[0], tuplettools.FixedDurationTuplet)
    assert voice[0].target_duration == Duration(2, 6)
    assert inspect(voice[0]).get_duration() == Duration(2, 6)
    assert isinstance(voice[0][0], Note)
    assert voice[0][0].written_duration == Duration(1, 4)
    assert inspect(voice[0][0]).get_duration() == Duration(1, 6)
    assert select(voice).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_19():
    r'''Excise staff.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(staff.select_leaves()[0])
    assert isinstance(staff, Staff)
    assert len(staff) == 2
    assert staff._preprolated_duration == Duration(5, 6)
    assert inspect(staff).get_duration() == Duration(5, 6)
    assert isinstance(staff[0], tuplettools.FixedDurationTuplet)
    assert staff[0].target_duration == Duration(2, 6)
    assert inspect(staff[0]).get_duration() == Duration(2, 6)
    assert isinstance(staff[0][0], Note)
    assert staff[0][0].written_duration == Duration(1, 4)
    assert inspect(staff[0][0]).get_duration() == Duration(1, 6)
    assert select(staff).is_well_formed()


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_20():
    r'''Excise singly-nested singleton.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        Note("c'4"),
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(1, 4), [Note("c'4")])])
    leaftools.remove_leaf_and_shrink_durated_parent_containers(tuplet.select_leaves()[-1])
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 2
    assert tuplet.target_duration == Duration(2, 6)
    assert tuplet.multiplier == Duration(2, 3)
    assert inspect(tuplet).get_duration() == Duration(2, 6)
    assert isinstance(tuplet[0], Note)
    assert tuplet[0].written_duration == Duration(1, 4)
    assert inspect(tuplet[0]).get_duration() == Duration(1, 6)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_21():
    r'''Excise doubly-nested singleton.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        Note("c'4"),
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(1, 4), [
            tuplettools.FixedDurationTuplet(Duration(1, 4), [Note("c'4")])])])

    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(tuplet)

    r'''
    \times 2/3 {
        c'4
        d'4
        {
            {
                e'4
            }
        }
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(tuplet.select_leaves()[-1])

    r'''
    \times 2/3 {
        c'4
        d'4
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'4
            d'4
        }
        '''
        )


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_22():
    r'''Excise doubly-nested singleton leaf.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        Note("c'4"),
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(1, 4), [
            tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 2)])])

    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(tuplet)

    r'''
    \times 2/3 {
        c'4
        d'4
        {
            {
                e'8
                f'8
            }
        }
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(tuplet.select_leaves()[-1])

    r'''
    \times 2/3 {
        c'4
        d'4
        {
            {
                e'8
            }
        }
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'4
            d'4
            {
                {
                    e'8
                }
            }
        }
        '''
        )


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_23():
    r'''Excise leaf from fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(4, 8), "c'8 d'8 e'8 f'8 g'8")

    r'''
    \times 4/5 {
        c'8
        d'8
        e'8
        f'8
        g'8
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(tuplet.select_leaves()[0])

    r'''
    \times 4/5 {
        d'8
        e'8
        f'8
        g'8
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
            d'8
            e'8
            f'8
            g'8
        }
        '''
        )


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_24():
    r'''Excise leaf from fixed-multiplier tuplet.
    '''

    #tuplet = Tuplet(Fraction(4, 5), "c'8 d'8 e'8 f'8 g'8")
    tuplet = Tuplet(Fraction(4, 5), "c'8 d'8 e'8 f'8 g'8")

    r'''
    \times 4/5 {
        c'8
        d'8
        e'8
        f'8
        g'8
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(tuplet.select_leaves()[0])

    r'''
    \times 4/5 {
        d'8
        e'8
        f'8
        g'8
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
            d'8
            e'8
            f'8
            g'8
        }
        '''
        )


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_25():
    r'''Excise nested fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2,2), [Note(0, (1,2)), Note(1, (1,2)),
        tuplettools.FixedDurationTuplet(Duration(2,4), [Note(i, (1,4)) for i in range(2, 5)])])

    r'''
    \times 2/3 {
        c'2
        cs'2
        \times 2/3 {
            d'4
            ef'4
            e'4
        }
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(tuplet.select_leaves()[-1])

    r'''
    \times 2/3 {
        c'2
        cs'2
        \times 2/3 {
            d'4
            ef'4
        }
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'2
            cs'2
            \times 2/3 {
                d'4
                ef'4
            }
        }
        '''
        )


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_26():
    r'''Excise nested fixed-multiplier tuplet.
    '''

    #tuplet = Tuplet(Fraction(2,3), [Note(0, (1,2)), Note(1, (1,2)),
    #    Tuplet(Fraction(2,3), [Note(i, (1,4)) for i in range(2, 5)])])
    tuplet = Tuplet(Fraction(2,3), [Note(0, (1,2)), Note(1, (1,2)),
        Tuplet(Fraction(2,3), [Note(i, (1,4)) for i in range(2, 5)])])

    r'''
    \times 2/3 {
        c'2
        cs'2
        \times 2/3 {
            d'4
            ef'4
            e'4
        }
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(tuplet.select_leaves()[-1])

    r'''
    \times 2/3 {
        c'2
        cs'2
        \times 2/3 {
            d'4
            ef'4
        }
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'2
            cs'2
            \times 2/3 {
                d'4
                ef'4
            }
        }
        '''
        )
