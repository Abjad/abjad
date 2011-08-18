from abjad import *


def test_containertools_repeat_contents_of_container_01():
    '''Multiply notes in voice.'''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])
    containertools.repeat_contents_of_container(t, total = 3)

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        c'8 [
        d'8 ]
        c'8 [
        d'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\tc'8 [\n\td'8 ]\n\tc'8 [\n\td'8 ]\n}"


def test_containertools_repeat_contents_of_container_02():
    '''Multiplication by one leaves contents unchanged.'''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])
    containertools.repeat_contents_of_container(t, total = 1)

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_containertools_repeat_contents_of_container_03():
    '''Multiplication by zero empties container.'''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])
    containertools.repeat_contents_of_container(t, total = 0)

    r'''
    \new Voice {
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Voice {\n}'
