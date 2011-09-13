from abjad import *


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_01():
    '''Excise leaf from tuplet and rigid measure.'''

    t = Measure((4, 4), tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 5/6\n\t\\scaleDurations #'(2 . 3) {\n\t\t{\n\t\t\td'4\n\t\t\te'4\n\t\t}\n\t\t{\n\t\t\tf'4\n\t\t\tg'4\n\t\t\ta'4\n\t\t}\n\t}\n}"


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_02():
    '''Excise leaf from tuplet and measure.'''

    t = Measure((4, 4), tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 5) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 9/10\n\t\\scaleDurations #'(4 . 5) {\n\t\t{\n\t\t\td'8\n\t\t\te'8\n\t\t\tf'8\n\t\t\tg'8\n\t\t}\n\t\t{\n\t\t\ta'8\n\t\t\tb'8\n\t\t\tc''8\n\t\t\td''8\n\t\t\te''8\n\t\t}\n\t}\n}"


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_03():
    '''Excise leaf from tuplet and measure.'''

    t = Measure((5, 6), [
        tuplettools.FixedDurationTuplet(Duration(3, 4), Note("c'4") * 5),
        tuplettools.FixedDurationTuplet(Duration(4, 8), Note(0, (1, 8)) * 7),
        ])

    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    {
        \time 5/6
        \scaleDurations #'(2 . 3) {
            \fraction \times 3/5 {
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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])

    r'''
    {
        \time 11/15
        \scaleDurations #'(8 . 15) {
            \fraction \times 3/4 {
                d'4
                e'4
                f'4
                g'4
            }
            \fraction \times 5/7 {
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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 11/15\n\t\\scaleDurations #'(8 . 15) {\n\t\t\\fraction \\times 3/4 {\n\t\t\td'4\n\t\t\te'4\n\t\t\tf'4\n\t\t\tg'4\n\t\t}\n\t\t\\fraction \\times 5/7 {\n\t\t\ta'8\n\t\t\tb'8\n\t\t\tc''8\n\t\t\td''8\n\t\t\te''8\n\t\t\tf''8\n\t\t\tg''8\n\t\t}\n\t}\n}"


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_04():
    '''Excise leaf that conflicts with meter duration;
        change meter denominator and reset tuplet target durations.'''

    t = Measure((5, 6), [
        tuplettools.FixedDurationTuplet(Duration(3, 4), Note("c'4") * 5),
        tuplettools.FixedDurationTuplet(Duration(4, 8), Note(0, (1, 8)) * 7),
        ])

    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \time 5/6
        \compressMusic #'(2 . 3) {
            \fraction \times 3/5 {
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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[-1])

    r'''
    \time 11/14
        \compressMusic #'(4 . 7) {
            \fraction \times 7/10 {
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

    assert isinstance(t, Measure)
    assert contexttools.get_effective_time_signature(t) == contexttools.TimeSignatureMark((11, 14))
    assert len(t) == 2
    tuplet = t[0]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 5
    assert tuplet.target_duration == Duration(7, 8)
    assert tuplet.prolated_duration == Duration(2, 4)
    note = t[0][0]
    assert note.written_duration == Duration(1, 4)
    assert note.prolated_duration == Duration(1, 10)
    tuplet = t[1]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 6
    assert tuplet.target_duration == Duration(4, 8)
    assert tuplet.prolated_duration == Duration(2, 7)
    note = t[1][0]
    assert note.written_duration == Duration(1, 8)
    assert note.prolated_duration == Duration(1, 21)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_05():
    '''Excise leaf that conflicts with meter duration;
        trigger tuplet insertion.'''

    t = Measure((5, 6),
        [tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(7))] +
            notetools.make_repeated_notes(3, (1, 4)))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])

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
            \fraction \times 7/6 {
                g'4
            }
            \fraction \times 7/6 {
                af'4
            }
            \fraction \times 7/6 {
                a'4
            }
        }
        '''

    assert isinstance(t, Measure)
    assert contexttools.get_effective_time_signature(t) == contexttools.TimeSignatureMark((11, 14))
    assert len(t) == 4
    tuplet = t[0]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 6
    assert tuplet.target_duration == Duration(2, 4)
    assert tuplet.prolated_duration == Duration(2, 7)
    note = t[0][0]
    assert note.written_duration == Duration(1, 8)
    assert note.prolated_duration == Duration(1, 21)
    tuplet = t[1]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 1
    assert tuplet.target_duration == Duration(7, 24)
    assert tuplet.prolated_duration == Duration(1, 6)
    note = t[1][0]
    assert note.written_duration == Duration(1, 4)
    assert note.prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_06():
    '''Excise leaf that matches meter duration;
        does not trigger trivial 1:1 tuplet insertion.'''

    t = Measure((5, 6),
        [tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(7))] +
            notetools.make_repeated_notes(3, (1, 4)))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[-1])

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

    assert isinstance(t, Measure)
    assert contexttools.get_effective_time_signature(t) == contexttools.TimeSignatureMark((4, 6))
    assert len(t) == 3
    tuplet = t[0]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 7
    assert tuplet.target_duration == Duration(2, 4)
    assert tuplet.prolated_duration == Duration(2, 6)
    note = t[0][0]
    assert note.written_duration == Duration(1, 8)
    assert note.prolated_duration == Duration(1, 21)
    note = t[1]
    assert note.written_duration == Duration(1, 4)
    assert note.prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_07():
    '''Nested fixed-duration tuplet.'''

    t = Measure((4, 4), [
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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[-1])
    measure = t
    assert isinstance(measure, Measure)
    assert contexttools.get_effective_time_signature(measure) == contexttools.TimeSignatureMark((8, 9))
    assert len(measure) == 1
    tuplet = t[0]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 3
    assert tuplet.target_duration == Duration(1)
    assert tuplet.prolated_duration == Duration(8, 9)
    assert tuplet.multiplier == Duration(3, 4)
    note = t[0][0]
    assert isinstance(note, Note)
    assert note.written_duration == Duration(1, 2)
    assert note.prolated_duration == Duration(1, 3)
    tuplet = t[0][-1]
    assert isinstance(tuplet, tuplettools.FixedDurationTuplet)
    assert len(tuplet) == 2
    assert tuplet.target_duration == Duration(1, 3)
    assert tuplet.prolated_duration == Duration(2, 9)
    assert tuplet.multiplier == Duration(2, 3)
    note = t[0][-1][0]
    assert isinstance(note, Note)
    assert note.written_duration == Duration(1, 4)
    assert note.prolated_duration == Duration(1, 9)

    r'''
    \time 8/9
        \compressMusic #'(8 . 9) {
            \fraction \times 3/4 {
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
    '''Exicse plain vanilla container.'''

    t = Container(Note("c'4") * 6)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])
    assert isinstance(t, Container)
    assert len(t) == 5
    assert t.preprolated_duration == Duration(5, 4)
    assert t.prolated_duration == Duration(5, 4)
    assert isinstance(t[0], Note)
    assert t[0].written_duration == Duration(1, 4)
    assert t[0].prolated_duration == Duration(1, 4)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_09():
    '''Container container.'''
    t = Container(Note("c'4") * 6)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])
    assert isinstance(t, Container)
    assert len(t) == 5
    assert t.preprolated_duration == Duration(5, 4)
    assert t.prolated_duration == Duration(5, 4)
    assert isinstance(t[0], Note)
    assert t[0].written_duration == Duration(1, 4)
    assert t[0].prolated_duration == Duration(1, 4)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_10():
    '''Excise voice.'''

    t = Voice(Note("c'4") * 6)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])
    assert isinstance(t, Voice)
    assert len(t) == 5
    assert t.preprolated_duration == Duration(5, 4)
    assert t.prolated_duration == Duration(5, 4)
    assert isinstance(t[0], Note)
    assert t[0].written_duration == Duration(1, 4)
    assert t[0].prolated_duration == Duration(1, 4)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_11():
    '''Staff.'''
    t = Staff(Note("c'4") * 6)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])
    assert isinstance(t, Staff)
    assert len(t) == 5
    assert t.preprolated_duration == Duration(5, 4)
    assert t.prolated_duration == Duration(5, 4)
    assert isinstance(t[0], Note)
    assert t[0].written_duration == Duration(1, 4)
    assert t[0].prolated_duration == Duration(1, 4)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_12():
    '''Container.'''

    t = Container(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t[0])
    assert isinstance(t, Container)
    assert len(t) == 1
    assert t.preprolated_duration == Duration(2, 4)
    assert t.prolated_duration == Duration(2, 4)
    assert isinstance(t[0], tuplettools.FixedDurationTuplet)
    assert t[0].target_duration == Duration(2, 4)
    assert t[0].prolated_duration == Duration(2, 4)
    assert isinstance(t[0][0], Note)
    assert t[0][0].written_duration == Duration(1, 4)
    assert t[0][0].prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_13():
    '''Container.'''

    t = Container(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t[0])
    assert isinstance(t, Container)
    assert len(t) == 1
    assert t.preprolated_duration == Duration(2, 4)
    assert t.prolated_duration == Duration(2, 4)
    assert isinstance(t[0], tuplettools.FixedDurationTuplet)
    assert t[0].target_duration == Duration(2, 4)
    assert t[0].prolated_duration == Duration(2, 4)
    assert isinstance(t[0][0], Note)
    assert t[0][0].written_duration == Duration(1, 4)
    assert t[0][0].prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_14():
    '''Excise voice.'''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t[0])
    assert isinstance(t, Voice)
    assert len(t) == 1
    assert t.preprolated_duration == Duration(2, 4)
    assert t.prolated_duration == Duration(2, 4)
    assert isinstance(t[0], tuplettools.FixedDurationTuplet)
    assert t[0].target_duration == Duration(2, 4)
    assert t[0].prolated_duration == Duration(2, 4)
    assert isinstance(t[0][0], Note)
    assert t[0][0].written_duration == Duration(1, 4)
    assert t[0][0].prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_15():
    '''Excise staff.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t[0])
    assert isinstance(t, Staff)
    assert len(t) == 1
    assert t.preprolated_duration == Duration(2, 4)
    assert t.prolated_duration == Duration(2, 4)
    assert isinstance(t[0], tuplettools.FixedDurationTuplet)
    assert t[0].target_duration == Duration(2, 4)
    assert t[0].prolated_duration == Duration(2, 4)
    assert isinstance(t[0][0], Note)
    assert t[0][0].written_duration == Duration(1, 4)
    assert t[0][0].prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_16():
    '''Excise container.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])
    assert isinstance(t, Staff)
    assert len(t) == 2
    assert t.preprolated_duration == Duration(5, 6)
    assert t.prolated_duration == Duration(5, 6)
    assert isinstance(t[0], tuplettools.FixedDurationTuplet)
    assert t[0].target_duration == Duration(2, 6)
    assert t[0].prolated_duration == Duration(2, 6)
    assert isinstance(t[0][0], Note)
    assert t[0][0].written_duration == Duration(1, 4)
    assert t[0][0].prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_17():
    '''Excise container.'''

    t = Container(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])
    assert isinstance(t, Container)
    assert len(t) == 2
    assert t.preprolated_duration == Duration(5, 6)
    assert t.prolated_duration == Duration(5, 6)
    assert isinstance(t[0], tuplettools.FixedDurationTuplet)
    assert t[0].target_duration == Duration(2, 6)
    assert t[0].prolated_duration == Duration(2, 6)
    assert isinstance(t[0][0], Note)
    assert t[0][0].written_duration == Duration(1, 4)
    assert t[0][0].prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_18():
    '''Excise voice.'''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])
    assert isinstance(t, Voice)
    assert len(t) == 2
    assert t.preprolated_duration == Duration(5, 6)
    assert t.prolated_duration == Duration(5, 6)
    assert isinstance(t[0], tuplettools.FixedDurationTuplet)
    assert t[0].target_duration == Duration(2, 6)
    assert t[0].prolated_duration == Duration(2, 6)
    assert isinstance(t[0][0], Note)
    assert t[0][0].written_duration == Duration(1, 4)
    assert t[0][0].prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_19():
    '''Excise staff.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 2)
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])
    assert isinstance(t, Staff)
    assert len(t) == 2
    assert t.preprolated_duration == Duration(5, 6)
    assert t.prolated_duration == Duration(5, 6)
    assert isinstance(t[0], tuplettools.FixedDurationTuplet)
    assert t[0].target_duration == Duration(2, 6)
    assert t[0].prolated_duration == Duration(2, 6)
    assert isinstance(t[0][0], Note)
    assert t[0][0].written_duration == Duration(1, 4)
    assert t[0][0].prolated_duration == Duration(1, 6)
    assert componenttools.is_well_formed_component(t)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_20():
    '''Excise singly-nested singleton.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        Note("c'4"),
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(1, 4), [Note("c'4")])])
    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[-1])
    assert isinstance(t, tuplettools.FixedDurationTuplet)
    assert len(t) == 2
    assert t.target_duration == Duration(2, 6)
    assert t.multiplier == Duration(2, 3)
    assert t.prolated_duration == Duration(2, 6)
    assert isinstance(t[0], Note)
    assert t[0].written_duration == Duration(1, 4)
    assert t[0].prolated_duration == Duration(1, 6)


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_21():
    '''Excise doubly-nested singleton.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        Note("c'4"),
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(1, 4), [
            tuplettools.FixedDurationTuplet(Duration(1, 4), [Note("c'4")])])])

    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[-1])

    r'''
    \times 2/3 {
        c'4
        d'4
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\times 2/3 {\n\tc'4\n\td'4\n}"


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_22():
    '''Excise doubly-nested singleton leaf.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        Note("c'4"),
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(1, 4), [
            tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 2)])])

    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[-1])

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\times 2/3 {\n\tc'4\n\td'4\n\t{\n\t\t{\n\t\t\te'8\n\t\t}\n\t}\n}"


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_23():
    '''Excise leaf from fixed-duration tuplet.'''

    t = tuplettools.FixedDurationTuplet(Duration(4, 8), "c'8 d'8 e'8 f'8 g'8")

    r'''
    \times 4/5 {
        c'8
        d'8
        e'8
        f'8
        g'8
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])

    r'''
    \times 4/5 {
        d'8
        e'8
        f'8
        g'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\times 4/5 {\n\td'8\n\te'8\n\tf'8\n\tg'8\n}"


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_24():
    '''Excise leaf from fixed-multiplier tuplet.'''

    #t = Tuplet(Fraction(4, 5), "c'8 d'8 e'8 f'8 g'8")
    t = Tuplet(Fraction(4, 5), "c'8 d'8 e'8 f'8 g'8")

    r'''
    \times 4/5 {
        c'8
        d'8
        e'8
        f'8
        g'8
    }
    '''

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[0])

    r'''
    \times 4/5 {
        d'8
        e'8
        f'8
        g'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\times 4/5 {\n\td'8\n\te'8\n\tf'8\n\tg'8\n}"


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_25():
    '''Excise nested fixed-duration tuplet.'''

    t = tuplettools.FixedDurationTuplet(Duration(2,2), [Note(0, (1,2)), Note(1, (1,2)),
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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[-1])

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\times 2/3 {\n\tc'2\n\tcs'2\n\t\\times 2/3 {\n\t\td'4\n\t\tef'4\n\t}\n}"


def test_leaftools_remove_leaf_and_shrink_durated_parent_containers_26():
    '''Excise nested fixed-multiplier tuplet.'''

    #t = Tuplet(Fraction(2,3), [Note(0, (1,2)), Note(1, (1,2)),
    #    Tuplet(Fraction(2,3), [Note(i, (1,4)) for i in range(2, 5)])])
    t = Tuplet(Fraction(2,3), [Note(0, (1,2)), Note(1, (1,2)),
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

    leaftools.remove_leaf_and_shrink_durated_parent_containers(t.leaves[-1])

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\times 2/3 {\n\tc'2\n\tcs'2\n\t\\times 2/3 {\n\t\td'4\n\t\tef'4\n\t}\n}"
