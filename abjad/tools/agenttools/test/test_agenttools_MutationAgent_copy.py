# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_MutationAgent_copy_01():
    r'''Deep copies components.
    Deep copies spanners that attach to client.
    Fractures spanners that attach to components not in client.
    Returns Python list of copied components.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = select(voice).by_leaf()
    slur = Slur()
    attach(slur, leaves)
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ ( \startTrillSpan
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ] ) \stopTrillSpan
            }
        }
        '''
        )

    selection = select(leaves[2:4])
    result = mutate(selection).copy()
    new = Voice(result)

    assert format(new) == String.normalize(
        r'''
        \new Voice {
            e'8 [ ( \startTrillSpan
            f'8 ] ) \stopTrillSpan
        }
        '''
        )
    assert inspect(voice).is_well_formed()
    assert inspect(new).is_well_formed()


def test_agenttools_MutationAgent_copy_02():
    r'''Copy one measure and fracture spanners.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = select(voice).by_leaf()
    slur = Slur()
    attach(slur, leaves)
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ ( \startTrillSpan
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ] ) \stopTrillSpan
            }
        }
        '''
        )

    result = mutate(voice[1:2]).copy()
    new = Voice(result)

    assert format(new) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
        }
        '''
        )
    assert inspect(voice).is_well_formed()
    assert inspect(new).is_well_formed()


def test_agenttools_MutationAgent_copy_03():
    r'''Three notes crossing measure boundaries.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = select(voice).by_leaf()
    slur = Slur()
    attach(slur, leaves)
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ ( \startTrillSpan
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ] ) \stopTrillSpan
            }
        }
        '''
        )

    selection = select(leaves[-3:])
    result = mutate(selection).copy()
    new = Voice(result)

    assert format(new) == String.normalize(
        r'''
        \new Voice {
            f'8 [ ( \startTrillSpan
            g'8
            a'8 ] ) \stopTrillSpan
        }
        '''
        )
    assert inspect(voice).is_well_formed()
    assert inspect(new).is_well_formed()


def test_agenttools_MutationAgent_copy_04():
    r'''Optional 'n' argument for multiple copies.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = select(voice).by_leaf()
    slur = Slur()
    attach(slur, leaves)
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ ( \startTrillSpan
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ] ) \stopTrillSpan
            }
        }
        '''
        )

    result = mutate(voice[1:2]).copy(n=3)
    new = Voice(result)

    assert format(new) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
            {
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
            {
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
        }
        '''
        )
    assert inspect(voice).is_well_formed()


def test_agenttools_MutationAgent_copy_05():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8 ] )
            }
        }
        '''
        )

    selection = selectiontools.Selection(music=voice)
    new_selection = mutate(selection).copy()
    new_voice = new_selection[0]
    for component in iterate(new_voice).by_class():
        detach(spannertools.Spanner, component)

    assert format(new_voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )
    assert inspect(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_06():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = mutate(voice[1:]).copy()
    new_voice = Voice(result)
    for component in iterate(new_voice).by_class():
        detach(spannertools.Spanner, component)

    assert format(new_voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )
    assert inspect(voice).is_well_formed()
    assert inspect(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_07():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8 ] )
            }
        }
        '''
        )

    leaves = select(leaves[:6])
    result = mutate(leaves).copy()
    new_voice = Voice(result)
    for component in iterate(new_voice).by_class():
        detach(spannertools.Spanner, component)

    assert format(new_voice) == String.normalize(
        r'''
        \new Voice {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        '''
        )
    assert inspect(voice).is_well_formed()
    assert inspect(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_08():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = mutate(voice[-2:]).copy()
    new_voice = Voice(result)
    for component in iterate(new_voice).by_class():
        detach(spannertools.Spanner, component)

    assert format(new_voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert inspect(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_09():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    slur = Slur()
    attach(slur, leaves)

    assert format(voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = mutate(voice[-2:]).copy(n=3)
    new_voice = Voice(result)
    for component in iterate(new_voice).by_class():
        detach(spannertools.Spanner, component)

    assert format(new_voice) == String.normalize(
        r'''
        \new Voice {
            {
                \time 2/8
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )
    assert inspect(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_10():
    r'''Copies hairpin.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    crescendo = Crescendo()
    attach(crescendo, staff[:4])

    assert format(staff) == String.normalize(
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    new_notes = mutate(staff[:4]).copy()
    staff.extend(new_notes)

    assert format(staff) == String.normalize(
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            e'8
            f'8
            fs'8
            g'8
            c'8 \<
            cs'8
            d'8
            ef'8 \!
        }
        '''
        )
    assert inspect(staff).is_well_formed()


def test_agenttools_MutationAgent_copy_11():
    r'''Copy consecutive notes across tuplet boundary in staff.
    Includes enclosing containers.
    '''

    staff = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")
    leaves = select(staff).by_leaf()

    assert format(staff) == String.normalize(
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

    leaves = select(leaves[1:5])
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert format(new_staff) == String.normalize(
        r'''
        \new Staff {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'8
                e'8
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'8
                g'8
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_12():
    r'''Copy consecutive notes across tuplet boundary in voice and staff.
    Includes enclosing containers.
    '''

    voice = Voice(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")
    staff = Staff([voice])
    leaves = select(staff).by_leaf()

    assert format(staff) == String.normalize(
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

    leaves = select(leaves[1:5])
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert format(new_staff) == String.normalize(
        r'''
        \new Staff {
            \new Voice {
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    d'8
                    e'8
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    f'8
                    g'8
                }
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_13():
    r'''Works fine on voices nested inside simultaneous context.
    Includes enclosing containers.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("g'8 a'8 b'8 c''8")
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    leaves = select(staff).by_leaf()

    assert format(staff) == String.normalize(
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

    leaves = select(leaves[1:3])
    new_voice = mutate(leaves).copy(include_enclosing_containers=True)

    assert format(new_voice) == String.normalize(
        r'''
        \new Voice {
            d'8
            e'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert inspect(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_14():
    r'''Copy consecutive notes in measure with power-of-two denominator.
    Includes enclosing containers.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    leaves = measure[1:3]
    new_measure = mutate(leaves).copy(include_enclosing_containers=True)

    assert format(new_measure) == String.normalize(
        r'''
        {
            \time 2/8
            d'8
            e'8
        }
        '''
        )

    assert inspect(new_measure).is_well_formed()


def test_agenttools_MutationAgent_copy_15():
    r'''Copy consecutive notes in staff and score.
    Includes enclosing containers.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    staff = score[0]
    leaves = staff[1:3]
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert format(new_staff) == String.normalize(
        r'''
        \new Staff {
            d'8
            e'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_16():
    r'''Copy consecutive leaves across measure boundary.
    Includes enclosing containers.
    '''

    measure_1 = Measure((3, 8), "c'8 d'8 e'8")
    measure_2 = Measure((3, 8), "f'8 g'8 a'8")
    staff = Staff([measure_1, measure_2])
    leaves = select(staff).by_leaf()

    assert format(staff) == String.normalize(
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

    leaves = select(leaves[2:4])
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert format(new_staff) == String.normalize(
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

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_17():
    r'''Copy consecutive leaves from measure in staff;
    pass start and stop indices local to measure.
    Includes enclosing containers.
    '''

    measure_1 = Measure((3, 8), "c'8 d'8 e'8")
    measure_2 = Measure((3, 8), "f'8 g'8 a'8")
    staff = Staff([measure_1, measure_2])

    assert format(staff) == String.normalize(
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

    leaves = measure_2[1:3]
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert format(new_staff) == String.normalize(
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

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_18():
    r'''Copy consecutive leaves from in-staff measure without
    power-of-two denominator. Pass start and stop indices local to measure.
    Includes enclosing containers.
    '''

    measure_1 = Measure((3, 9), "c'8 d'8 e'8")
    measure_1.implicit_scaling = True
    measure_2 = Measure((3, 9), "f'8 g'8 a'8")
    measure_2.implicit_scaling = True
    staff = Staff([measure_1, measure_2])

    assert format(staff) == String.normalize(
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

    leaves = measure_2[1:3]
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert format(new_staff) == String.normalize(
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

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_19():
    r'''Copy indicators while maintaining "is_annotation" flag.
    '''

    old_staff = Staff("c'4 d'4 e'4 f'4")
    indicator = indicatortools.BendAfter()
    attach(indicator, old_staff[0], is_annotation=True)
    assert format(old_staff) == String.normalize(
        r'''
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }
        ''')
    assert inspect(old_staff[0]).get_indicators() == (indicator,)

    new_staff = mutate(old_staff).copy()
    assert format(new_staff) == String.normalize(
        r'''
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }
        ''')
    assert inspect(new_staff[0]).get_indicators() == (indicator,)

    assert inspect(old_staff[0]).get_indicators()[0] is not \
        inspect(new_staff[0]).get_indicators()[0]
