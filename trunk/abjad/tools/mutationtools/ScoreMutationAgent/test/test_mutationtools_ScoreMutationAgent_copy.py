# -*- encoding: utf-8 -*-
from abjad import *


def test_mutationtools_ScoreMutationAgent_copy_01():
    r'''Deep copy components in 'components'.
    Deep copy spanners that attach to any component in 'components'.
    Fracture spanners that attach to components not in 'components'.
    Returns Python list of copied components.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    slur = spannertools.SlurSpanner()
    slur.attach(voice[:])
    trill = spannertools.TrillSpanner()
    trill.attach(voice.select_leaves())
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0][:] + voice[1:2] + voice[2][:])

    assert testtools.compare(
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

    assert testtools.compare(
        new,
        r'''
        \new Voice {
            e'8 \startTrillSpan
            f'8 \stopTrillSpan
        }
        '''
        )
    assert inspect(voice).is_well_formed()
    assert inspect(new).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_02():
    r'''Copy one measure and fracture spanners.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    slur = spannertools.SlurSpanner()
    slur.attach(voice[:])
    trill = spannertools.TrillSpanner()
    trill.attach(voice.select_leaves())
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0][:] + voice[1:2] + voice[2][:])

    assert testtools.compare(
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

    assert testtools.compare(
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
    assert inspect(voice).is_well_formed()
    assert inspect(new).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_03():
    r'''Three notes crossing measure boundaries.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    slur = spannertools.SlurSpanner()
    slur.attach(voice[:])
    trill = spannertools.TrillSpanner()
    trill.attach(voice.select_leaves())
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0][:] + voice[1:2] + voice[2][:])

    assert testtools.compare(
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

    assert testtools.compare(
        new,
        r'''
        \new Voice {
            f'8 \startTrillSpan
            g'8 [
            a'8 ] \stopTrillSpan
        }
        '''
        )
    assert inspect(voice).is_well_formed()
    assert inspect(new).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_04():
    r'''Optional 'n' argument for multiple copies.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    slur = spannertools.SlurSpanner()
    slur.attach(voice[:])
    trill = spannertools.TrillSpanner()
    trill.attach(voice.select_leaves())
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0][:] + voice[1:2] + voice[2][:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ ( \startTrillSpan
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8 ] ) \stopTrillSpan
            }
        }
        '''
        )

    result = mutate(voice[1:2]).copy(n=3)
    new = Voice(result)
    measuretools.set_always_format_time_signature_of_measures_in_expr(new)

    assert testtools.compare(
        new,
        r'''
        \new Voice {
            {
                \time 2/8
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
            {
                \time 2/8
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
            {
                \time 2/8
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
        }
        '''
        )
    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_05():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    selection = selectiontools.ContiguousSelection(music=voice)
    new_selection = mutate(selection).copy()
    new_voice = new_selection[0]
    for component in iterationtools.iterate_components_in_expr(new_voice):
        spanners = inspect(component).get_spanners()
        for spanner in spanners:
            spanner.detach()
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
            }
        }
        '''
        )
    assert inspect(new_voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_06():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = mutate(voice[1:]).copy()
    new_voice = Voice(result)
    for component in iterationtools.iterate_components_in_expr(new_voice):
        spanners = inspect(component).get_spanners()
        for spanner in spanners:
            spanner.detach()
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
            }
        }
        '''
        )
    assert inspect(voice).is_well_formed()
    assert inspect(new_voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_07():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = mutate(voice.select_leaves()[:6]).copy()
    new_voice = Voice(result)
    for component in iterationtools.iterate_components_in_expr(new_voice):
        spanners = inspect(component).get_spanners()
        for spanner in spanners:
            spanner.detach()
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
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
    assert inspect(voice).is_well_formed()
    assert inspect(new_voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_08():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = mutate(voice[-2:]).copy()
    new_voice = Voice(result)
    for component in iterationtools.iterate_components_in_expr(new_voice):
        spanners = inspect(component).get_spanners()
        for spanner in spanners:
            spanner.detach()
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert inspect(new_voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_09():

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = mutate(voice[-2:]).copy(n=3)
    new_voice = Voice(result)
    for component in iterationtools.iterate_components_in_expr(new_voice):
        spanners = inspect(component).get_spanners()
        for spanner in spanners:
            spanner.detach()
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
            }
        }
        '''
        )
    assert inspect(new_voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_10():
    r'''Copies hairpin.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = spannertools.CrescendoSpanner()
    crescendo.attach(staff[:4])

    assert testtools.compare(
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

    assert testtools.compare(
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
    assert inspect(staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_11():
    r'''Copy consecutive notes across tuplet boundary in staff.
    Include enclosing containers.
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

    leaves = staff.select_leaves(1, 5)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_12():
    r'''Copy consecutive notes across tuplet boundary in voice and staff.
    Include enclosing containers.
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

    leaves = staff.select_leaves(1, 5)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_13():
    r'''Works fine on voices nested inside simultaneous context.
    Include enclosing containers.
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

    leaves = voice_1.select_leaves(1, 3)
    new_voice = mutate(leaves).copy(include_enclosing_containers=True)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
            d'8
            e'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert inspect(new_voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_14():
    r'''Copy consecutive notes in measure with power-of-two denominator.
    Include enclosing containers.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    leaves = measure.select_leaves(1, 3)
    new_measure = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(new_measure).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_15():
    r'''Copy consecutive notes in staff and score.
    Include enclosing containers.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    staff = score[0]
    leaves = staff.select_leaves(1, 3)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

    assert testtools.compare(
        new_staff,
        r'''
        \new Staff {
            d'8
            e'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_16():
    r'''Copy consecutive leaves from tuplet in measure with power-of-two 
    denominator. Measure without power-of-two denominator results.
    Include enclosing containers.
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

    leaves = measure.select_leaves(1, 4)
    new_measure = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(measure).is_well_formed()
    assert inspect(new_measure).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_17():
    r'''Copy consecutive leaves from tuplet in measure and voice.
    Measure without power-of-two time signature denominator results.
    Include enclosing containers.
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

    leaves = voice.select_leaves(1, 4)
    new_voice = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(voice).is_well_formed()
    assert inspect(new_voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_18():
    r'''Measures shrink when copying a partial tuplet.

    Note that test only works with fixed-duration tuplets.
    Include enclosing containers.
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

    leaves = measure.select_leaves(1, None)
    new_measure = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(measure).is_well_formed()
    assert inspect(new_measure).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_19():
    r'''Copy consecutive leaves across measure boundary.
    Include enclosing containers.
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

    leaves = staff.select_leaves(2, 4)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_20():
    r'''Copy consecutive leaves from tuplet in staff;
    pass start and stop indices local to tuplet.
    Include enclosing containers.
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

    leaves = tuplet_2.select_leaves(1, 3)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_21():
    r'''Copy consecutive leaves from measure in staff;
    pass start and stop indices local to measure.
    Include enclosing containers.
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

    leaves = measure_2.select_leaves(1, 3)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_copy_22():
    r'''Copy consecutive leaves from in-staff measure without 
    power-of-two denominator. Pass start and stop indices local to measure.
    Include enclosing containers.
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

    leaves = measure_2.select_leaves(1, 3)
    new_staff = mutate(leaves).copy(include_enclosing_containers=True)

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

    assert inspect(staff).is_well_formed()
    assert inspect(new_staff).is_well_formed()
