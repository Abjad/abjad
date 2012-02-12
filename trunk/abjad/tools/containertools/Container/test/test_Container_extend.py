from abjad import *
import py.test


def test_Container_extend_01():
    '''Extend container with list of leaves.
    '''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    t.extend([Note("c'8"), Note("d'8")])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        c'8
        d'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\tc'8\n\td'8\n}"


def test_Container_extend_02():
    '''Extend container with contents of other container.
    '''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    u = Voice([Note(4, (1, 8)), Note(5, (1, 8))])
    spannertools.BeamSpanner(u[:])
    t.extend(u)

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8 [
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\te'8 [\n\tf'8 ]\n}"


def test_Container_extend_03():
    '''Extending container with empty list leaves container unchanged.
    '''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])
    t.extend([])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_Container_extend_04():
    '''Extending one container with empty second container leaves both containers unchanged.
    '''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])
    t.extend(Voice([]))

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_Container_extend_05():
    '''Trying to extend container with noncomponent raises TypeError.
    '''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])

    assert py.test.raises(Exception, 't.extend(7)')
    assert py.test.raises(Exception, "t.extend('foo')")


def test_Container_extend_06():
    '''Trying to extend container with noncontainer raises exception.
    '''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])

    assert py.test.raises(Exception, 't.extend(Note(4, (1, 4)))')
    assert py.test.raises(AssertionError, "t.extend(Chord([2, 3, 5], (1, 4)))")


def test_Container_extend_07():
    '''Extend container with partial and spanned contents of other container.'''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    u = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(u[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    t.extend(u[-2:])

    "Container t is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\te'8\n\tf'8\n}"

    "Container u is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(u)
    assert u.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_Container_extend_08():
    '''Extend container with partial and spanned contents of other container.
    Covered span comes with components from donor container.
    '''

    t = Voice("c'8 d'8")
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    u = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(u[:])
    spannertools.SlurSpanner(u[-2:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 (
        f'8 ] )
    }
    '''

    t.extend(u[-2:])

    "Container t is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8 (
        f'8 )
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\te'8 (\n\tf'8 )\n}"

    "Container u is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(u)
    assert u.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_Container_extend_09():
    '''Extend container with LilyPond input string.
    '''

    container = Container([])
    container.extend("c'4 ( d'4 e'4 f'4 )")

    r'''
    {
        c'4 (
        d'4
        e'4
        f'4 )
    }
    '''

    assert componenttools.is_well_formed_component(container)
    assert container.format == "{\n\tc'4 (\n\td'4\n\te'4\n\tf'4 )\n}"
