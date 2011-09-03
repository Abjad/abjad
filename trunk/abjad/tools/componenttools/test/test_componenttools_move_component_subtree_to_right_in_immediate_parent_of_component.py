from abjad import *


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_01():
    '''Flip leaf under continuous spanner.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(t[1])

    r'''
    \new Voice {
        c'8 [
        e'8
        d'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\te'8\n\td'8\n\tf'8 ]\n}"


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_02():
    '''Flip leaf across spanner boundaries.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:2])
    spannertools.BeamSpanner(t[2:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8 [
        f'8 ]
    }
    '''

    componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(t[1])

    r'''
    \new Voice {
        c'8 [
        e'8 ]
        d'8 [
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\te'8 ]\n\td'8 [\n\tf'8 ]\n}"


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_03():
    '''Flip leaf from within to without spanner.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:2])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8
        f'8
    }
    '''

    componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(t[1])

    r'''
    \new Voice {
        c'8 [
        e'8 ]
        d'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\te'8 ]\n\td'8\n\tf'8\n}"


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_04():
    '''Donate from empty container to leaf.'''

    t = Voice([Container("c'8 d'8"), Container([])])
    spannertools.GlissandoSpanner(t[:])
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 ]
        }
        {
        }
    }
    '''

    #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[1:2], Note(4, (1, 8)))
    # ALSO WORKS:
    componenttools.move_parentage_and_spanners_from_components_to_components(t[1:2], [Note(4, (1, 8))])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\te'8 ]\n}"


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_05():
    '''Donate from empty container to nonempty container.'''

    t = Voice([Container("c'8 d'8"), Container([])])
    spannertools.GlissandoSpanner(t[:])
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 ]
        }
        {
        }
    }
    '''

    container = Container([Note(4, (1, 8)), Note(5, (1, 8))])
    #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[1:2], container)
    # ALSO WORKS:
    componenttools.move_parentage_and_spanners_from_components_to_components(t[1:2], [container])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            e'8 \glissando
            f'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t{\n\t\te'8 \\glissando\n\t\tf'8 ]\n\t}\n}"


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_06():
    '''Donate from note to rest.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)

    r'''
    \new Voice {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    old = t.leaves[2]
    #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t.leaves[2:3], Rest((1, 8)))
    # ALSO WORKS:
    componenttools.move_parentage_and_spanners_from_components_to_components(t.leaves[2:3], [Rest((1, 8))])

    r'''
    \new Voice {
        {
            c'8 [
            d'8
        }
        {
            r8
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\tr8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_07():
    '''Donate from note to tuplet.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.GlissandoSpanner(t[:])
    spannertools.BeamSpanner(t.leaves)

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

    tuplet = tuplettools.FixedDurationTuplet(Duration(1, 8), Note(0, (1, 16)) * 3)
    #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[1][:1], tuplet)
    # ALSO WORKS:
    componenttools.move_parentage_and_spanners_from_components_to_components(t[1][:1], [tuplet])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            \times 2/3 {
                c'16 \glissando
                c'16 \glissando
                c'16 \glissando
            }
            f'8 \glissando
        }
        {
            g'8 \glissando
            a'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tc'16 \\glissando\n\t\t\tc'16 \\glissando\n\t\t\tc'16 \\glissando\n\t\t}\n\t\tf'8 \\glissando\n\t}\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"
