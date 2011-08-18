from abjad import *


def test_componenttools_copy_components_and_remove_all_spanners_01():
    '''Withdraw components from spanners.
        Deepcopy unspanned components.
        Reapply spanners to components.
        Return unspanned copy.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2] + t[2][:] + t[3][:])
    slur = spannertools.SlurSpanner(t[0][:] + t[1][:] + t[2:])

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

    result = componenttools.copy_components_and_remove_all_spanners([t])
    voice = result[0]

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

    assert componenttools.is_well_formed_component(t)
    assert componenttools.is_well_formed_component(voice)
    assert voice.format == "\\new Voice {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n\t}\n}"


def test_componenttools_copy_components_and_remove_all_spanners_02():
    '''Withdraw components from spanners.
        Deepcopy unspanned components.
        Reapply spanners to components.
        Return unspanned copy.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2] + t[2][:] + t[3][:])
    slur = spannertools.SlurSpanner(t[0][:] + t[1][:] + t[2:])

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

    result = componenttools.copy_components_and_remove_all_spanners(t[1:])
    new = Voice(result)

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

    assert componenttools.is_well_formed_component(t)
    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Voice {\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n\t}\n}"


def test_componenttools_copy_components_and_remove_all_spanners_03():
    '''Withdraw components from spanners.
        Deepcopy unspanned components.
        Reapply spanners to components.
        Return unspanned copy.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2] + t[2][:] + t[3][:])
    slur = spannertools.SlurSpanner(t[0][:] + t[1][:] + t[2:])

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

    result = componenttools.copy_components_and_remove_all_spanners(t.leaves[:6])
    new = Voice(result)

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

    assert componenttools.is_well_formed_component(t)
    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n}"


def test_componenttools_copy_components_and_remove_all_spanners_04():
    '''Withdraw components from spanners.
        Deepcopy unspanned components.
        Reapply spanners to components.
        Return unspanned copy.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2] + t[2][:] + t[3][:])
    slur = spannertools.SlurSpanner(t[0][:] + t[1][:] + t[2:])

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

    result = componenttools.copy_components_and_remove_all_spanners(t[-2:])
    new = Voice(result)

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

    assert componenttools.is_well_formed_component(t)
    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Voice {\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n\t}\n}"


def test_componenttools_copy_components_and_remove_all_spanners_05():
    '''Withdraw components from spanners.
        Deepcopy unspanned components.
        Reapply spanners to components.
        Return unspanned copy.
        Use optional 'n' argument for multiple copies.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2] + t[2][:] + t[3][:])
    slur = spannertools.SlurSpanner(t[0][:] + t[1][:] + t[2:])

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

    result = componenttools.copy_components_and_remove_all_spanners(t[-2:], 3)
    new = Voice(result)

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

    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Voice {\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n\t}\n}"
