from abjad import *


def test_componenttools_extend_in_parent_of_component_and_do_not_grow_spanners_01():
    '''Extend leaves rightwards after leaf.'''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    result = componenttools.extend_in_parent_of_component_and_do_not_grow_spanners(
        t[-1], [Note("c'8"), Note("d'8"), Note("e'8")])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
        c'8
        d'8
        e'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert result == t[-4:]
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n\tc'8\n\td'8\n\te'8\n}"


def test_componenttools_extend_in_parent_of_component_and_do_not_grow_spanners_02():
    '''Extend leaf rightwards after interior leaf.'''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    result = componenttools.extend_in_parent_of_component_and_do_not_grow_spanners(
        t[1], [Note(2.5, (1, 8))])

    r'''
    \new Voice {
        c'8 [
        d'8
        dqs'8
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\tdqs'8\n\te'8 ]\n}"
    assert result == t[1:3]
