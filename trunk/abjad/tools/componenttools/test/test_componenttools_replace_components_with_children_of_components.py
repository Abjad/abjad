from abjad import *


def test_componenttools_replace_components_with_children_of_components_01():
    '''Containers can 'slip out' of score structure.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t.leaves)

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    sequential = t[0]
    componenttools.replace_components_with_children_of_components(t[0:1])

    r'''
    \new Staff {
        c'8 [
        d'8
        {
            e'8
            f'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(sequential) == 0
    assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_componenttools_replace_components_with_children_of_components_02():
    '''Slip leaf from parentage and spanners.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    spannertools.GlissandoSpanner(t[:])

    note = t[1]
    componenttools.replace_components_with_children_of_components([note])

    r'''
    \new Voice {
        c'8 [ \glissando
        e'8 \glissando
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\te'8 \\glissando\n\tf'8 ]\n}"


def test_componenttools_replace_components_with_children_of_components_03():
    '''Slip multiple leaves.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    spannertools.GlissandoSpanner(t[:])

    r'''
    \new Voice {
        c'8 [ \glissando
        d'8 \glissando
        e'8 \glissando
        f'8 ]
    }
    '''

    componenttools.replace_components_with_children_of_components(t[:2])

    r'''
    \new Voice {
        e'8 [ \glissando
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\te'8 [ \\glissando\n\tf'8 ]\n}"


def test_componenttools_replace_components_with_children_of_components_04():
    '''Slip multiple containers.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)
    spannertools.GlissandoSpanner(t.leaves)

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            e'8 \glissando
            f'8 \glissando
        }
        {
            g'8 \glissando
            a'8 ]
        }
    }
    '''

    componenttools.replace_components_with_children_of_components(t[:2])

    r'''
    \new Voice {
        c'8 [ \glissando
        d'8 \glissando
        e'8 \glissando
        f'8 \glissando
        {
            g'8 \glissando
            a'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\td'8 \\glissando\n\te'8 \\glissando\n\tf'8 \\glissando\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"
