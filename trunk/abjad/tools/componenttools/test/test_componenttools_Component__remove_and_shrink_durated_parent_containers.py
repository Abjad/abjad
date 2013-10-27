# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_01():
    r'''Remove leaf from tuplet and measure.
    '''

    measure = Measure((4, 4), [])
    measure.append(tuplettools.FixedDurationTuplet((2, 4), "c'4 d'4 e'4"))
    measure.append(tuplettools.FixedDurationTuplet((2, 4), "f'4 g'4 a'4"))

    assert testtools.compare(
        measure,
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
        )

    measure.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

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

    assert inspect(measure).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_02():
    r'''Remove leaf from tuplet and measure.
    '''

    measure = Measure((4, 4), [])
    tuplet_1 = tuplettools.FixedDurationTuplet((2, 4), "c'8 d' e' f' g'")
    tuplet_2 = tuplettools.FixedDurationTuplet((2, 4), "a'8 b' c'' d'' e''")
    measure.extend([tuplet_1, tuplet_2])

    assert testtools.compare(
        measure,
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
        )

    measure.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

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

    assert inspect(measure).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_03():
    r'''Remove leaf from tuplet and measure.
    '''

    measure = Measure((5, 6), [])
    tuplet_1 = tuplettools.FixedDurationTuplet(
        (3, 4), "c'4 d' e' f' g'")
    tuplet_2 = tuplettools.FixedDurationTuplet(
        (4, 8), "a'8 b' c'' d'' e'' f'' g''")
    measure.extend([tuplet_1, tuplet_2])

    assert testtools.compare(
        measure,
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
        )

    measure.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

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

    assert inspect(measure).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_04():
    r'''Remove leaf that conflicts with time signature duration.
    Change time signature denominator and reset tuplet target durations.
    '''

    measure = Measure((5, 6), [])
    tuplet_1 = tuplettools.FixedDurationTuplet(
        (3, 4), "c'4 cs' d' ef' e'")
    tuplet_2 = tuplettools.FixedDurationTuplet(
        (4, 8), "f'8 fs' g' af' a' bf' b'")
    measure.extend([tuplet_1, tuplet_2])

    assert testtools.compare(
        measure,
        r'''
        {
            \time 5/6
            \scaleDurations #'(2 . 3) {
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
        }
        '''
        )

    measure.select_leaves()[-1]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        measure,
        r'''
        {
            \time 11/14
            \scaleDurations #'(4 . 7) {
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
        }
        '''
        )

    assert inspect(measure).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_05():
    r'''Remove leaf that conflicts with time signature duration.
    Trigger tuplet insertion.
    '''

    measure = Measure((5, 6), [])
    tuplet = tuplettools.FixedDurationTuplet((4, 8), [])
    tuplet.extend("c'8 cs' d' ef' e' f' fs'")
    measure.append(tuplet)
    measure.extend("g'4 af'4 a'4")

    assert testtools.compare(
        measure,
        r'''
        {
            \time 5/6
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
                a'4
            }
        }
        '''
        )

    measure.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        measure,
        r'''
        {
            \time 11/14
            \scaleDurations #'(4 . 7) {
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
        }
        '''
        )

    assert inspect(measure).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_06():
    r'''Remove leaf that matches time signature duration.
    Does not trigger trivial 1:1 tuplet insertion.
    '''

    measure = Measure((5, 6), [])
    tuplet = tuplettools.FixedDurationTuplet((4, 8), [])
    tuplet.extend("c'8 cs' d' ef' e' f' fs'")
    measure.append(tuplet)
    measure.extend("g'4 af'4 a'4")

    assert testtools.compare(
        measure,
        r'''
        {
            \time 5/6
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
                a'4
            }
        }
        '''
        )

    measure.select_leaves()[-1]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        measure,
        r'''
        {
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
        }
        '''
        )

    assert inspect(measure).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_07():
    r'''Nested fixed-duration tuplet.
    '''

    measure = Measure((4, 4), [])
    inner_tuplet = tuplettools.FixedDurationTuplet((2, 4), "d'4 ef'4 e'4")
    outer_tuplet = tuplettools.FixedDurationTuplet((2, 2), [])
    outer_tuplet.extend([Note("c'2"), Note("cs'2"), inner_tuplet])
    measure.append(outer_tuplet)

    assert testtools.compare(
        measure,
        r'''
        {
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
        }
        '''
        )

    measure.select_leaves()[-1]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        measure,
        r'''
        {
            \time 8/9
            \scaleDurations #'(8 . 9) {
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
        }
        '''
        )

    assert inspect(measure).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_08():
    r'''Remove leaf from container.
    '''

    container = Container("c'4 c'4 c'4 c'4 c'4 c'4")

    container.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        container,
        r'''
        {
            c'4
            c'4
            c'4
            c'4
            c'4
        }
        '''
        )

    assert inspect(container).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_09():
    r'''Remove leaf from voice.
    '''

    voice = Voice(Note("c'4") * 6)

    voice.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'4
            c'4
            c'4
            c'4
            c'4
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_10():
    r'''Remove leaf from staff.
    '''

    staff = Staff(Note("c'4") * 6)

    staff.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'4
            c'4
            c'4
            c'4
            c'4
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_11():
    r'''Remove fixed-duration tuplet from container.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    tuplet_2 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    container = Container([tuplet_1, tuplet_2])

    assert testtools.compare(
        container,
        r'''
        {
            \times 2/3 {
                c'4
                c'4
                c'4
            }
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    container[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        container,
        r'''
        {
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    assert inspect(container).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_12():
    r'''Remove fixed-duration tuplet from voice.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    tuplet_2 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    voice = Voice([tuplet_1, tuplet_2])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'4
                c'4
                c'4
            }
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    voice[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_13():
    r'''Remove fixed-duration tuplet from staff.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    tuplet_2 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    staff = Staff([tuplet_1, tuplet_2])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \times 2/3 {
                c'4
                c'4
                c'4
            }
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    staff[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_14():
    r'''Remove leaf from fixed-duration tuplet in container.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    tuplet_2 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    container = Container([tuplet_1, tuplet_2])

    assert testtools.compare(
        container,
        r'''
        {
            \times 2/3 {
                c'4
                c'4
                c'4
            }
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    container.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        container,
        r'''
        {
            \times 2/3 {
                c'4
                c'4
            }
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    assert inspect(container).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_15():
    r'''Remove leaf form fixed-duration tuplet in voice.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    tuplet_2 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    voice = Voice([tuplet_1, tuplet_2])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'4
                c'4
                c'4
            }
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    voice.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'4
                c'4
            }
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_16():
    r'''Remove leaf from fixed-duration tuplet in staff.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    tuplet_2 = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'4 c'4 c'4")
    staff = Staff([tuplet_1, tuplet_2])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \times 2/3 {
                c'4
                c'4
                c'4
            }
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    staff.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \times 2/3 {
                c'4
                c'4
            }
            \times 2/3 {
                c'4
                c'4
                c'4
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_17():
    r'''Remove leaf from nested tuplet of length 1.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [])
    inner_tuplet = tuplettools.FixedDurationTuplet((1, 4), "c'4")
    tuplet.extend([Note("c'4"), Note("c'4"), inner_tuplet])

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'4
            c'4
            {
                c'4
            }
        }
        '''
        )

    tuplet.select_leaves()[-1]._remove_and_shrink_durated_parent_containers()


    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'4
            c'4
        }
        '''
        )

    assert inspect(tuplet[0]).get_duration() == Duration(1, 6)


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_18():
    r'''Remove leaf from nested tuplet of length 1.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [])
    middle_tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), [])
    inner_tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), [])
    inner_tuplet.extend("e'4")
    middle_tuplet.append(inner_tuplet)
    tuplet.extend([Note("c'4"), Note("d'4"), middle_tuplet])

    assert testtools.compare(
        tuplet,
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
        )

    tuplet.select_leaves()[-1]._remove_and_shrink_durated_parent_containers()

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'4
            d'4
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_19():
    r'''Remove leaf from nested fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [])
    middle_tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), [])
    inner_tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), [])
    inner_tuplet.extend("e'8 f'8")
    middle_tuplet.append(inner_tuplet)
    tuplet.extend([Note("c'4"), Note("d'4"), middle_tuplet])

    assert testtools.compare(
        tuplet,
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
        )

    tuplet.select_leaves()[-1]._remove_and_shrink_durated_parent_containers()

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

    assert inspect(tuplet).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_20():
    r'''Excise leaf from fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(4, 8), [])
    tuplet.extend("c'8 d'8 e'8 f'8 g'8")

    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
            c'8
            d'8
            e'8
            f'8
            g'8
        }
        '''
        )

    tuplet.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

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

    assert inspect(tuplet).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_21():
    r'''Remove leaf from tuplet.
    '''

    tuplet = Tuplet(Multiplier(4, 5), "c'8 d'8 e'8 f'8 g'8")

    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
            c'8
            d'8
            e'8
            f'8
            g'8
        }
        '''
        )

    tuplet.select_leaves()[0]._remove_and_shrink_durated_parent_containers()

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

    assert inspect(tuplet).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_22():
    r'''Remove leaf from nested fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 2), [])
    inner_tuplet = tuplettools.FixedDurationTuplet((2, 4), "d'4 ef'4 e'4")
    tuplet.extend([Note("c'2"), Note("cs'2"), inner_tuplet])
    
    assert testtools.compare(
        tuplet,
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
        )

    tuplet.select_leaves()[-1]._remove_and_shrink_durated_parent_containers()

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

    assert inspect(tuplet).is_well_formed()


def test_componenttools_Component__remove_and_shrink_durated_parent_containers_23():
    r'''Remove leaf from nested tuplet.
    '''

    tuplet = Tuplet(Multiplier(2, 3), [])
    tuplet.extend(r"c'2 cs'2 \times 2/3 { d'4 ef'4 e'4 }")

    assert testtools.compare(
        tuplet,
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
        )

    tuplet.select_leaves()[-1]._remove_and_shrink_durated_parent_containers()

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

    assert inspect(tuplet).is_well_formed()
