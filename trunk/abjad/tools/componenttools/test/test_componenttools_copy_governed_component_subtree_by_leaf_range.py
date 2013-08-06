# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_componenttools_copy_governed_component_subtree_by_leaf_range_01():
    r'''Copy consecutive notes across tuplet boundary, in staff.
    '''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t, 1, 5)

    r'''
    \new Staff {
        \times 2/3 {
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
        }
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        \new Staff {
            \times 2/3 {
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
            }
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_02():
    r'''Copy consecutive notes across tuplet boundary, in voice and staff.
    '''

    t = Staff([Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        \new Voice {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8
            }
        }
    }
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t, 1, 5)

    r'''
    \new Staff {
    \new Voice {
        \times 2/3 {
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
        }
    }
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        \new Staff {
            \new Voice {
                \times 2/3 {
                    d'8
                    e'8
                }
                \times 2/3 {
                    f'8
                    g'8
                }
            }
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_03():
    r'''Copy leaves from sequential containers only.
    '''

    t = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    t.is_parallel = True

    statement = 'componenttools.copy_governed_component_subtree_'
    statement += 'by_leaf_range(t, 1, 5)'
    assert py.test.raises(Exception, statement)


def test_componenttools_copy_governed_component_subtree_by_leaf_range_04():
    r'''Works fine on voices nested inside parallel context.
    '''

    t = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    t.is_parallel = True
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff <<
        \new Voice {
            c'8
            d'8
            e'8
            f'8
        }
        \new Voice {
            g'8
            a'8
            b'8
            c''8
        }
    >>
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t[0], 1, 3)

    r'''
    \new Voice {
        d'8
        e'8
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        \new Voice {
            d'8
            e'8
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_05():
    r'''Copy consecutive notes in measure with power-of-two time signature denominator.
    '''

    t = Measure((4, 8), "c'8 d'8 e'8 f'8")
    u = componenttools.copy_governed_component_subtree_by_leaf_range(t, 1, 3)

    r'''
    {
        \time 2/8
        d'8
        e'8
    }
    '''

    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        {
            \time 2/8
            d'8
            e'8
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_06():
    r'''Copy consecutive notes in staff and score.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    t = score[0]
    new = componenttools.copy_governed_component_subtree_by_leaf_range(t, 1, 3)

    r'''
    \new Staff {
        d'8
        e'8
    }
    '''

    assert select(t).is_well_formed()
    assert select(new).is_well_formed()
    assert testtools.compare(
        new.lilypond_format,
        r'''
        \new Staff {
            d'8
            e'8
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_07():
    r'''Copy consecutive leaves from tuplet in measure with power-of-two time signature denominator.
    Measure without power-of-two time signature denominator results.
    '''

    t = Measure((4, 8), [tuplettools.FixedDurationTuplet(Duration(4, 8), "c'8 d'8 e'8 f'8 g'8")])

    r'''
    {
        \time 4/8
        \times 4/5 {
            c'8
            d'8
            e'8
            f'8
            g'8
        }
    }
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t, 1, 4)

    r'''
    {
        \time 3/10
        \scaleDurations #'(4 . 5) {
            {
                d'8
                e'8
                f'8
            }
        }
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        {
            \time 3/10
            \scaleDurations #'(4 . 5) {
                {
                    d'8
                    e'8
                    f'8
                }
            }
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_08():
    r'''Copy consecutive leaves from tuplet in measure and voice.
    Measure without power-of-two time signature denominator results.
    '''

    t = Voice([Measure((4, 8),
        [tuplettools.FixedDurationTuplet(Duration(4, 8), "c'8 d'8 e'8 f'8 g'8")])])

    r'''
    \new Voice {
        {
            \time 4/8
            \times 4/5 {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
        }
    }
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t, 1, 4)

    r'''
    \new Voice {
        {
            \time 3/10
            \scaleDurations #'(4 . 5) {
                {
                    d'8
                    e'8
                    f'8
                }
            }
        }
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        \new Voice {
            {
                \time 3/10
                \scaleDurations #'(4 . 5) {
                    {
                        d'8
                        e'8
                        f'8
                    }
                }
            }
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_09():
    r'''Measures shrink down when we copy a partial tuplet.
    '''

    t = Measure((4, 8),
        tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    {
        \time 4/8
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t, 1)

    r'''
    {
        \time 5/12
        \scaleDurations #'(2 . 3) {
            {
                d'8
                e'8
            }
            {
                f'8
                g'8
                a'8
            }
        }
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        {
            \time 5/12
            \scaleDurations #'(2 . 3) {
                {
                    d'8
                    e'8
                }
                {
                    f'8
                    g'8
                    a'8
                }
            }
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_10():
    r'''Copy consecutive leaves across measure boundary.
    '''

    t = Staff(Measure((3, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 3/8
            c'8
            d'8
            e'8
        }
        {
            \time 3/8
            f'8
            g'8
            a'8
        }
    }
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t, 2, 4)
    measuretools.set_always_format_time_signature_of_measures_in_expr(u)

    r'''
    \new Staff {
        {
            \time 1/8
            e'8
        }
        {
            \time 1/8
            f'8
        }
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        \new Staff {
            {
                \time 1/8
                e'8
            }
            {
                \time 1/8
                f'8
            }
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_11():
    r'''Copy consecutive leaves from tuplet in staff;
        pass start and stop indices local to tuplet.
    '''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t[1], 1, 3)

    r'''
    \new Staff {
        \times 2/3 {
            g'8
            a'8
        }
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        \new Staff {
            \times 2/3 {
                g'8
                a'8
            }
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_12():
    r'''Copy consecutive leaves from measure in staff;
    pass start and stop indices local to measure.
    '''

    t = Staff(Measure((3, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 3/8
            c'8
            d'8
            e'8
        }
        {
            \time 3/8
            f'8
            g'8
            a'8
        }
    }
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t[1], 1, 3)
    measuretools.set_always_format_time_signature_of_measures_in_expr(u)

    r'''
    \new Staff {
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        \new Staff {
            {
                \time 2/8
                g'8
                a'8
            }
        }
        '''
        )


def test_componenttools_copy_governed_component_subtree_by_leaf_range_13():
    r'''Copy consecutive leaves from in-staff measure without power-of-two time signature denominator.
    Pass start and stop indices local to measure.
    '''

    t = Staff(Measure((3, 9), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 3/9
            \scaleDurations #'(8 . 9) {
                c'8
                d'8
                e'8
            }
        }
        {
            \time 3/9
            \scaleDurations #'(8 . 9) {
                f'8
                g'8
                a'8
            }
        }
    }
    '''

    u = componenttools.copy_governed_component_subtree_by_leaf_range(t[1], 1, 3)
    measuretools.set_always_format_time_signature_of_measures_in_expr(u)

    r'''
    \new Staff {
        {
            \time 2/9
            \scaleDurations #'(8 . 9) {
                g'8
                a'8
            }
        }
    }
    '''

    assert select(t).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u.lilypond_format,
        r'''
        \new Staff {
            {
                \time 2/9
                \scaleDurations #'(8 . 9) {
                    g'8
                    a'8
                }
            }
        }
        '''
        )
