# -*- encoding: utf-8 -*-
import py.test
from abjad import *


def test_componenttools_copy_governed_component_subtree_by_leaf_range_01():
    r'''Copy consecutive notes across tuplet boundary in staff.
    '''

    staff = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")

    assert testtools.compare(
        staff,
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
        )

    new_staff = componenttools.copy_governed_component_subtree_by_leaf_range(
        staff, 1, 5)

    assert testtools.compare(
        new_staff,
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

    assert select(staff).is_well_formed()
    assert select(new_staff).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_02():
    r'''Copy consecutive notes across tuplet boundary in voice and staff.
    '''

    voice = Voice(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")
    staff = Staff([voice])

    assert testtools.compare(
        staff,
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
        )

    new_staff = componenttools.copy_governed_component_subtree_by_leaf_range(
        staff, 1, 5)

    assert testtools.compare(
        new_staff,
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

    assert select(staff).is_well_formed()
    assert select(new_staff).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_03():
    r'''Can not copy from simultaneous container.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    staff.is_simultaneous = True

    statement = 'componenttools.copy_governed_component_subtree_'
    statement += 'by_leaf_range(staff, 1, 5)'
    assert py.test.raises(Exception, statement)


def test_componenttools_copy_governed_component_subtree_by_leaf_range_04():
    r'''Works fine on voices nested inside simultaneous context.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("g'8 a'8 b'8 c''8")
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True

    assert testtools.compare(
        staff,
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
        )

    new_voice = componenttools.copy_governed_component_subtree_by_leaf_range(
        staff[0], 1, 3)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
            d'8
            e'8
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert select(new_voice).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_05():
    r'''Copy consecutive notes in measure with power-of-two denominator.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    new_measure = componenttools.copy_governed_component_subtree_by_leaf_range(
        measure, 1, 3)

    assert testtools.compare(
        new_measure,
        r'''
        {
            \time 2/8
            d'8
            e'8
        }
        '''
        )

    assert select(new_measure).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_06():
    r'''Copy consecutive notes in staff and score.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    staff = score[0]
    new_staff = componenttools.copy_governed_component_subtree_by_leaf_range(
        staff, 1, 3)

    assert testtools.compare(
        new_staff,
        r'''
        \new Staff {
            d'8
            e'8
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert select(new_staff).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_07():
    r'''Copy consecutive leaves from tuplet in measure with power-of-two 
    denominator. Measure without power-of-two denominator results.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(4, 8), [])
    tuplet.extend("c'8 d'8 e'8 f'8 g'8")
    measure = Measure((4, 8), [tuplet])

    assert testtools.compare(
        measure,
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
        )

    new_measure = componenttools.copy_governed_component_subtree_by_leaf_range(
        measure, 1, 4)

    assert testtools.compare(
        new_measure,
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

    assert select(measure).is_well_formed()
    assert select(new_measure).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_08():
    r'''Copy consecutive leaves from tuplet in measure and voice.
    Measure without power-of-two time signature denominator results.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(4, 8), [])
    tuplet.extend("c'8 d'8 e'8 f'8 g'8")
    voice = Voice([Measure((4, 8), [tuplet])])

    assert testtools.compare(
        voice,
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
        )

    new_voice = componenttools.copy_governed_component_subtree_by_leaf_range(
        voice, 1, 4)

    assert testtools.compare(
        new_voice,
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

    assert select(voice).is_well_formed()
    assert select(new_voice).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_09():
    r'''Measures shrink when copying a partial tuplet.

    Note that test only works with fixed-duration tuplets.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
    tuplet_2 = tuplettools.FixedDurationTuplet((2, 8), "f'8 g'8 a'8")
    measure = Measure((4, 8), [tuplet_1, tuplet_2])

    assert testtools.compare(
        measure,
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
        )

    new_measure = componenttools.copy_governed_component_subtree_by_leaf_range(
        measure, 1)

    assert testtools.compare(
        new_measure,
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

    assert select(measure).is_well_formed()
    assert select(new_measure).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_10():
    r'''Copy consecutive leaves across measure boundary.
    '''

    measure_1 = Measure((3, 8), "c'8 d'8 e'8")
    measure_2 = Measure((3, 8), "f'8 g'8 a'8")
    staff = Staff([measure_1, measure_2])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/8
                c'8
                d'8
                e'8
            }
            {
                f'8
                g'8
                a'8
            }
        }
        '''
        )

    new_staff = componenttools.copy_governed_component_subtree_by_leaf_range(
        staff, 2, 4)

    assert testtools.compare(
        new_staff,
        r'''
        \new Staff {
            {
                \time 1/8
                e'8
            }
            {
                f'8
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert select(new_staff).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_11():
    r'''Copy consecutive leaves from tuplet in staff;
    pass start and stop indices local to tuplet.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
    tuplet_2 = tuplettools.FixedDurationTuplet((2, 8), "f'8 g'8 a'8")
    staff = Staff([tuplet_1, tuplet_2])

    assert testtools.compare(
        staff,
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
        )

    new_staff = componenttools.copy_governed_component_subtree_by_leaf_range(
        staff[1], 1, 3)

    assert testtools.compare(
        new_staff,
        r'''
        \new Staff {
            \times 2/3 {
                g'8
                a'8
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert select(new_staff).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_12():
    r'''Copy consecutive leaves from measure in staff;
    pass start and stop indices local to measure.
    '''

    measure_1 = Measure((3, 8), "c'8 d'8 e'8")
    measure_2 = Measure((3, 8), "f'8 g'8 a'8")
    staff = Staff([measure_1, measure_2])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/8
                c'8
                d'8
                e'8
            }
            {
                f'8
                g'8
                a'8
            }
        }
        '''
        )

    new_staff = componenttools.copy_governed_component_subtree_by_leaf_range(
        staff[1], 1, 3)

    assert testtools.compare(
        new_staff,
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

    assert select(staff).is_well_formed()
    assert select(new_staff).is_well_formed()


def test_componenttools_copy_governed_component_subtree_by_leaf_range_13():
    r'''Copy consecutive leaves from in-staff measure without 
    power-of-two denominator. Pass start and stop indices local to measure.
    '''

    measure_1 = Measure((3, 9), "c'8 d'8 e'8")
    measure_2 = Measure((3, 9), "f'8 g'8 a'8")
    staff = Staff([measure_1, measure_2])

    assert testtools.compare(
        staff,
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
                \scaleDurations #'(8 . 9) {
                    f'8
                    g'8
                    a'8
                }
            }
        }
        '''
        )

    new_staff = componenttools.copy_governed_component_subtree_by_leaf_range(
        staff[1], 1, 3)

    assert testtools.compare(
        new_staff,
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

    assert select(staff).is_well_formed()
    assert select(new_staff).is_well_formed()
