# -*- encoding: utf-8 -*-
from abjad import *


def test_agenttools_MutationAgent_copy_01():
    r'''Deep copies components.
    Deep copies spanners that attach to client.
    Fractures spanners that attach to components not in client.
    Returns Python list of copied components.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    slur = Slur()
    attach(slur, voice[:])
    trill = spannertools.TrillSpanner()
    attach(trill, voice.select_leaves())
    beam = Beam()
    attach(beam, voice[0][:] + voice[1:2] + voice[2][:])

    assert systemtools.TestManager.compare(
        voice,
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

    selection = voice.select_leaves()[2:4]
    result = mutate(selection).copy()
    new = Voice(result)

    assert systemtools.TestManager.compare(
        new,
        r'''
        \new Voice {
            e'8 \startTrillSpan
            f'8 \stopTrillSpan
        }
        '''
        )
    assert inspect_(voice).is_well_formed()
    assert inspect_(new).is_well_formed()


def test_agenttools_MutationAgent_copy_02():
    r'''Copy one measure and fracture spanners.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    slur = Slur()
    attach(slur, voice[:])
    trill = spannertools.TrillSpanner()
    attach(trill, voice.select_leaves())
    beam = Beam()
    attach(beam, voice[0][:] + voice[1:2] + voice[2][:])

    assert systemtools.TestManager.compare(
        voice,
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

    assert systemtools.TestManager.compare(
        new,
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
    assert inspect_(voice).is_well_formed()
    assert inspect_(new).is_well_formed()


def test_agenttools_MutationAgent_copy_03():
    r'''Three notes crossing measure boundaries.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    slur = Slur()
    attach(slur, voice[:])
    trill = spannertools.TrillSpanner()
    attach(trill, voice.select_leaves())
    beam = Beam()
    attach(beam, voice[0][:] + voice[1:2] + voice[2][:])

    assert systemtools.TestManager.compare(
        voice,
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

    selection = voice.select_leaves()[-3:]
    result = mutate(selection).copy()
    new = Voice(result)

    assert systemtools.TestManager.compare(
        new,
        r'''
        \new Voice {
            f'8 \startTrillSpan
            g'8 [
            a'8 ] \stopTrillSpan
        }
        '''
        )
    assert inspect_(voice).is_well_formed()
    assert inspect_(new).is_well_formed()


def test_agenttools_MutationAgent_copy_04():
    r'''Optional 'n' argument for multiple copies.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    slur = Slur()
    attach(slur, voice[:])
    trill = spannertools.TrillSpanner()
    attach(trill, voice.select_leaves())
    beam = Beam()
    attach(beam, voice[0][:] + voice[1:2] + voice[2][:])

    assert systemtools.TestManager.compare(
        voice,
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

    assert systemtools.TestManager.compare(
        new,
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
    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_copy_05():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = Beam()
    attach(beam, voice[:2] + voice[2][:] + voice[3][:])
    slur = Slur()
    attach(slur, voice[0][:] + voice[1][:] + voice[2:])

    assert systemtools.TestManager.compare(
        voice,
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

    selection = selectiontools.ContiguousSelection(music=voice)
    new_selection = mutate(selection).copy()
    new_voice = new_selection[0]
    for component in iterate(new_voice).by_class():
        detach(spannertools.Spanner, component)

    assert systemtools.TestManager.compare(
        new_voice,
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
    assert inspect_(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_06():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = Beam()
    attach(beam, voice[:2] + voice[2][:] + voice[3][:])
    slur = Slur()
    attach(slur, voice[0][:] + voice[1][:] + voice[2:])

    assert systemtools.TestManager.compare(
        voice,
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

    assert systemtools.TestManager.compare(
        new_voice,
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
    assert inspect_(voice).is_well_formed()
    assert inspect_(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_07():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = Beam()
    attach(beam, voice[:2] + voice[2][:] + voice[3][:])
    slur = Slur()
    attach(slur, voice[0][:] + voice[1][:] + voice[2:])

    assert systemtools.TestManager.compare(
        voice,
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

    result = mutate(voice.select_leaves()[:6]).copy()
    new_voice = Voice(result)
    for component in iterate(new_voice).by_class():
        detach(spannertools.Spanner, component)

    assert systemtools.TestManager.compare(
        new_voice,
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
    assert inspect_(voice).is_well_formed()
    assert inspect_(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_08():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = Beam()
    attach(beam, voice[:2] + voice[2][:] + voice[3][:])
    slur = Slur()
    attach(slur, voice[0][:] + voice[1][:] + voice[2:])

    assert systemtools.TestManager.compare(
        voice,
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

    assert systemtools.TestManager.compare(
        new_voice,
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

    assert inspect_(voice).is_well_formed()
    assert inspect_(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_09():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = Beam()
    attach(beam, voice[:2] + voice[2][:] + voice[3][:])
    slur = Slur()
    attach(slur, voice[0][:] + voice[1][:] + voice[2:])

    assert systemtools.TestManager.compare(
        voice,
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

    assert systemtools.TestManager.compare(
        new_voice,
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
    assert inspect_(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_10():
    r'''Copies hairpin.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    crescendo = Crescendo()
    attach(crescendo, staff[:4])

    assert systemtools.TestManager.compare(
        staff,
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

    assert systemtools.TestManager.compare(
        staff,
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
    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_copy_11():
    r'''Copy consecutive notes across tuplet boundary in staff.
    Includes enclosing containers.
    '''

    staff = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")

    assert systemtools.TestManager.compare(
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

    leaves = staff.select_leaves(1, 5)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()
    assert inspect_(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_12():
    r'''Copy consecutive notes across tuplet boundary in voice and staff.
    Includes enclosing containers.
    '''

    voice = Voice(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")
    staff = Staff([voice])

    assert systemtools.TestManager.compare(
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

    leaves = staff.select_leaves(1, 5)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()
    assert inspect_(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_13():
    r'''Works fine on voices nested inside simultaneous context.
    Includes enclosing containers.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("g'8 a'8 b'8 c''8")
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True

    assert systemtools.TestManager.compare(
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

    leaves = voice_1.select_leaves(1, 3)
    new_voice = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
        new_voice,
        r'''
        \new Voice {
            d'8
            e'8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
    assert inspect_(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_14():
    r'''Copy consecutive notes in measure with power-of-two denominator.
    Includes enclosing containers.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    leaves = measure.select_leaves(1, 3)
    new_measure = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
        new_measure,
        r'''
        {
            \time 2/8
            d'8
            e'8
        }
        '''
        )

    assert inspect_(new_measure).is_well_formed()


def test_agenttools_MutationAgent_copy_15():
    r'''Copy consecutive notes in staff and score.
    Includes enclosing containers.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    staff = score[0]
    leaves = staff.select_leaves(1, 3)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
        new_staff,
        r'''
        \new Staff {
            d'8
            e'8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
    assert inspect_(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_16():
    r'''Copy consecutive leaves from tuplet in measure with power-of-two 
    denominator. Measure without power-of-two denominator results.
    Includes enclosing containers.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(4, 8), [])
    tuplet.extend("c'8 d'8 e'8 f'8 g'8")
    measure = Measure((4, 8), [tuplet])
    measure.should_scale_contents = True

    assert systemtools.TestManager.compare(
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

    leaves = measure.select_leaves(1, 4)
    new_measure = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
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

    assert inspect_(measure).is_well_formed()
    assert inspect_(new_measure).is_well_formed()


def test_agenttools_MutationAgent_copy_17():
    r'''Copy consecutive leaves from tuplet in measure and voice.
    Measure without power-of-two time signature denominator results.
    Includes enclosing containers.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(4, 8), [])
    tuplet.extend("c'8 d'8 e'8 f'8 g'8")
    measure = Measure((4, 8), [tuplet])
    measure.should_scale_contents = True
    voice = Voice([measure])

    assert systemtools.TestManager.compare(
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

    leaves = voice.select_leaves(1, 4)
    new_voice = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
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

    assert inspect_(voice).is_well_formed()
    assert inspect_(new_voice).is_well_formed()


def test_agenttools_MutationAgent_copy_18():
    r'''Measures shrink when copying a partial tuplet.
    Note that test only works with fixed-duration tuplets.
    Includes enclosing containers.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
    tuplet_2 = scoretools.FixedDurationTuplet((2, 8), "f'8 g'8 a'8")
    measure = Measure((4, 8), [tuplet_1, tuplet_2])
    measure.should_scale_contents = True

    assert systemtools.TestManager.compare(
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

    leaves = measure.select_leaves(1, None)
    new_measure = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
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

    assert inspect_(measure).is_well_formed()
    assert inspect_(new_measure).is_well_formed()


def test_agenttools_MutationAgent_copy_19():
    r'''Copy consecutive leaves across measure boundary.
    Includes enclosing containers.
    '''

    measure_1 = Measure((3, 8), "c'8 d'8 e'8")
    measure_2 = Measure((3, 8), "f'8 g'8 a'8")
    staff = Staff([measure_1, measure_2])

    assert systemtools.TestManager.compare(
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

    leaves = staff.select_leaves(2, 4)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()
    assert inspect_(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_20():
    r'''Copy consecutive leaves from tuplet in staff;
    pass start and stop indices local to tuplet.
    Includes enclosing containers.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
    tuplet_2 = scoretools.FixedDurationTuplet((2, 8), "f'8 g'8 a'8")
    staff = Staff([tuplet_1, tuplet_2])

    assert systemtools.TestManager.compare(
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

    leaves = tuplet_2.select_leaves(1, 3)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()
    assert inspect_(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_21():
    r'''Copy consecutive leaves from measure in staff;
    pass start and stop indices local to measure.
    Includes enclosing containers.
    '''

    measure_1 = Measure((3, 8), "c'8 d'8 e'8")
    measure_2 = Measure((3, 8), "f'8 g'8 a'8")
    staff = Staff([measure_1, measure_2])

    assert systemtools.TestManager.compare(
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

    leaves = measure_2.select_leaves(1, 3)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()
    assert inspect_(new_staff).is_well_formed()


def test_agenttools_MutationAgent_copy_22():
    r'''Copy consecutive leaves from in-staff measure without 
    power-of-two denominator. Pass start and stop indices local to measure.
    Includes enclosing containers.
    '''

    measure_1 = Measure((3, 9), "c'8 d'8 e'8")
    measure_1.should_scale_contents = True
    measure_2 = Measure((3, 9), "f'8 g'8 a'8")
    measure_2.should_scale_contents = True
    staff = Staff([measure_1, measure_2])

    assert systemtools.TestManager.compare(
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

    leaves = measure_2.select_leaves(1, 3)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()
    assert inspect_(new_staff).is_well_formed()
