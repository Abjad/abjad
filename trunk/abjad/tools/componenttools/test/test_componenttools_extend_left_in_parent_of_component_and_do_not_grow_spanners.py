from abjad import *


def test_componenttools_extend_left_in_parent_of_component_and_do_not_grow_spanners_01():
    '''Extend leaves leftwards of leaf. Do not extend edge spanners.'''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16")]
    result = componenttools.extend_left_in_parent_of_component_and_do_not_grow_spanners(t[0], notes)

    r'''
    \new Voice {
        c'16
        d'16
        e'16
        c'8 [
        d'8
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert result == t[:4]
    assert t.format == "\\new Voice {\n\tc'16\n\td'16\n\te'16\n\tc'8 [\n\td'8\n\te'8 ]\n}"


def test_componenttools_extend_left_in_parent_of_component_and_do_not_grow_spanners_02():
    '''Extend leaf leftwards of interior leaf. Do extend interior spanners.'''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    result = componenttools.extend_left_in_parent_of_component_and_do_not_grow_spanners(
        t[1], [Note(1.5, (1, 8))])

    r'''
    \new Voice {
        c'8 [
        dqf'8
        d'8
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\tdqf'8\n\td'8\n\te'8 ]\n}"
    assert result == t[1:3]
