from abjad import *


def test_componenttools_copy_components_and_fracture_crossing_spanners_01():
    '''Deep copy components in 'components'.
    Deep copy spanners that attach to any component in 'components'.
    Fracture spanners that attach to components not in 'components'.
    Return Python list of copied components.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    slur = spannertools.SlurSpanner(t[:])
    trill = spannertools.TrillSpanner(t.leaves)
    beam = spannertools.BeamSpanner(t[0][:] + t[1:2] + t[2][:])

    r'''
    \new Voice {
        \time 2/8
        c'8 [ ( \startTrillSpan
        d'8
        \time 2/8
        e'8
        f'8
        \time 2/8
        g'8
        a'8 ] ) \stopTrillSpan
    }
    '''

    result = componenttools.copy_components_and_fracture_crossing_spanners(t.leaves[2:4])
    new = Voice(result)

    r'''
    \new Voice {
        e'8 \startTrillSpan
        f'8 \stopTrillSpan
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Voice {\n\te'8 \\startTrillSpan\n\tf'8 \\stopTrillSpan\n}"


def test_componenttools_copy_components_and_fracture_crossing_spanners_02():
    '''Copy one measure and fracture spanners.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    slur = spannertools.SlurSpanner(t[:])
    trill = spannertools.TrillSpanner(t.leaves)
    beam = spannertools.BeamSpanner(t[0][:] + t[1:2] + t[2][:])

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

    result = componenttools.copy_components_and_fracture_crossing_spanners(t[1:2])
    new = Voice(result)

    r'''
    \new Voice {
        {
            \time 2/8
            e'8 [ ( \startTrillSpan
            f'8 ] ) \stopTrillSpan
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Voice {\n\t{\n\t\t\\time 2/8\n\t\te'8 [ ( \\startTrillSpan\n\t\tf'8 ] ) \\stopTrillSpan\n\t}\n}"


def test_componenttools_copy_components_and_fracture_crossing_spanners_03():
    '''Three notes crossing measure boundaries.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    slur = spannertools.SlurSpanner(t[:])
    trill = spannertools.TrillSpanner(t.leaves)
    beam = spannertools.BeamSpanner(t[0][:] + t[1:2] + t[2][:])

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

    result = componenttools.copy_components_and_fracture_crossing_spanners(t.leaves[-3:])
    new = Voice(result)

    r'''
    \new Voice {
        f'8 \startTrillSpan
        g'8 [
        a'8 ] \stopTrillSpan
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Voice {\n\tf'8 \\startTrillSpan\n\tg'8 [\n\ta'8 ] \\stopTrillSpan\n}"


def test_componenttools_copy_components_and_fracture_crossing_spanners_04():
    '''Optional 'n' argument for multiple copies.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    slur = spannertools.SlurSpanner(t[:])
    trill = spannertools.TrillSpanner(t.leaves)
    beam = spannertools.BeamSpanner(t[0][:] + t[1:2] + t[2][:])

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

    result = componenttools.copy_components_and_fracture_crossing_spanners(t[1:2], 3)
    new = Voice(result)

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

    assert componenttools.is_well_formed_component(t)
    assert new.format == "\\new Voice {\n\t{\n\t\t\\time 2/8\n\t\te'8 [ ( \\startTrillSpan\n\t\tf'8 ] ) \\stopTrillSpan\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [ ( \\startTrillSpan\n\t\tf'8 ] ) \\stopTrillSpan\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [ ( \\startTrillSpan\n\t\tf'8 ] ) \\stopTrillSpan\n\t}\n}"
