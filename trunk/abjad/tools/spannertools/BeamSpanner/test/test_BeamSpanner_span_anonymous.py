# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_BeamSpanner_span_anonymous_01():
    r'''Empty container.
    '''

    container = Container([])
    beam = spannertools.BeamSpanner(container)

    r'''
    {
    }
    '''

    assert len(beam.components) == 1
    assert isinstance(beam.components[0], Container)
    assert len(beam.leaves) == 0
    assert testtools.compare(
        container.lilypond_format,
        '{\n}'
        )


def test_BeamSpanner_span_anonymous_02():
    r'''Nonempty container.
    '''

    container = Container("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    beam = spannertools.BeamSpanner(container)

    r'''
    {
        c'8 [
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8 ]
    }
    '''

    assert len(beam.components) == 1
    assert isinstance(beam.components[0], Container)
    assert len(beam.leaves) == 8
    assert testtools.compare(
        container.lilypond_format,
        "{\n\tc'8 [\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}"
        )


def test_BeamSpanner_span_anonymous_03():
    r'''Nested nonempty containers.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } { c'8 c'8 c'8 c'8 }")
    beam = spannertools.BeamSpanner(staff[:])

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        {
            c'8
            c'8
            c'8
            c'8 ]
        }
    }
    '''

    assert len(beam.components) == 2
    assert type(beam.components[0]) is Container
    assert type(beam.components[1]) is Container
    assert len(beam.leaves) == 8

    assert testtools.compare(
        staff.lilypond_format,
        "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
        )


def test_BeamSpanner_span_anonymous_04():
    r'''Beamed staff with container and top-level leaves.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } c'8 c'8")
    beam = spannertools.BeamSpanner(staff)

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        c'8
        c'8 ]
    }
    '''

    assert len(beam.components) == 1
    assert type(beam.components[0]) is Staff
    assert len(beam.leaves) == 6

    assert testtools.compare(
        staff.lilypond_format,
        "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\tc'8\n\tc'8 ]\n}"
        )


def test_BeamSpanner_span_anonymous_05():
    r'''Beamed container and top-level leaves housed in staff.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } c'8 c'8")
    beam = spannertools.BeamSpanner(staff[:])

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        c'8
        c'8 ]
    }
    '''

    assert len(beam.components) == 3
    assert type(beam.components[0]) is Container
    assert type(beam.components[1]) is Note
    assert type(staff[2]) is Note
    assert len(beam.leaves) == 6

    assert testtools.compare(
        staff.lilypond_format,
        "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\tc'8\n\tc'8 ]\n}"
        )


def test_BeamSpanner_span_anonymous_06():
    r'''Beamed leaves housed in staff and container.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } c'8 c'8")
    beam = spannertools.BeamSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        c'8
        c'8 ]
    }
    '''

    assert len(beam.components) == 6
    assert all(type(x) is Note for x in beam.components)
    assert len(beam.leaves) == 6

    assert testtools.compare(
        staff.lilypond_format,
        "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\tc'8\n\tc'8 ]\n}"
        )


def test_BeamSpanner_span_anonymous_07():
    r'''Staff with empty containers.
    '''

    staff = Staff("{} {} {}")
    beam = spannertools.BeamSpanner(staff[:])

    r'''
    \new Staff {
        {
        }
        {
        }
        {
        }
    }
    '''

    assert len(beam.components) == 3
    assert all(type(x) is Container for x in beam.components)
    assert len(beam.leaves) == 0
    
    assert testtools.compare(
        staff.lilypond_format,
        '\\new Staff {\n\t{\n\t}\n\t{\n\t}\n\t{\n\t}\n}'
        )


def test_BeamSpanner_span_anonymous_08():
    r'''Staff with empty containers in the middle.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } {} { c'8 c'8 c'8 c'8 }")
    beam = spannertools.BeamSpanner(staff[:])

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        {
        }
        {
            c'8
            c'8
            c'8
            c'8 ]
        }
    }
    '''

    assert len(beam.components) == 3
    assert all(type(x) is Container for x in beam.components)
    assert len(beam.leaves) == 8

    assert testtools.compare(
        staff.lilypond_format,
        "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t}\n\t{\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
        )


def test_BeamSpanner_span_anonymous_09():
    r'''Staff with empty containers at the edges.
    '''

    t = Staff(Container([]) * 2)
    t.insert(1, Container(Note(0, (1, 8)) * 4))
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Staff {
        {
        }
        {
            c'8 [
            c'8
            c'8
            c'8 ]
        }
        {
        }
    }
    '''

    assert len(p.components) == 3
    for x in p.components:
        assert isinstance(x, Container)
    assert len(p.leaves) == 4

    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t{\n\t}\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n\t{\n\t}\n}"
        )


def test_BeamSpanner_span_anonymous_10():
    r'''Deeply nested containers of equal depth.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    s2 = Container([s2])
    t = Voice([s1, s2])
    p = spannertools.BeamSpanner(t)
    assert len(p.components) == 1
    assert len(p.leaves) == 8

    r'''
    \new Voice {
        {
            {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        {
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
    }
    '''

    p.detach()
    p = spannertools.BeamSpanner([t[0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8

    p.detach()
    p = spannertools.BeamSpanner([t[0][0], t[1][0]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8

    p.detach()
    p = spannertools.BeamSpanner([t[0], t[1][0]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8

    p.detach()
    p = spannertools.BeamSpanner([t[0][0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8


def test_BeamSpanner_span_anonymous_11():
    r'''Deeply nested containers of unequal depth.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    t = Voice([s1, s2])

    r'''
    \new Voice {
        {
            {
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
        }
        {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    p = spannertools.BeamSpanner(t)
    assert len(p.components) == 1
    assert len(p.leaves) == 8
    p.detach()

    p = spannertools.BeamSpanner([t[0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8
    p.detach()

    p = spannertools.BeamSpanner([t[0][0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8
    p.detach()

    p = spannertools.BeamSpanner([t[0][0][0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8
    p.detach()


def test_BeamSpanner_span_anonymous_12():
    r'''Voice with containers and top-level leaves.
    '''

    s1 = Container([Note(i, (1, 8)) for i in range(2)])
    s2 = Container([Note(i, (1, 8)) for i in range(3, 5)])
    v = Voice([s1, Note(2, (1, 8)), s2])

    r'''
    \new Voice {
        {
            c'8
            cs'8
        }
        d'8
        {
            ef'8
            e'8
        }
    }
    '''

    p = spannertools.BeamSpanner(v)
    assert len(p.components) == 1
    assert len(p.leaves) == 5
    p.detach()

    p = spannertools.BeamSpanner(v[:])
    assert len(p.components) == 3
    assert len(p.leaves) == 5
    p.detach()


def test_BeamSpanner_span_anonymous_13():
    r'''Voice with tuplets and top-level leaves.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(4,7)])
    v = Voice([t1, Note(3, (1,8)), t2])

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            cs'8
            d'8
        }
        ef'8
        \times 2/3 {
            e'8
            f'8
            fs'8
        }
    }
    '''

    p = spannertools.BeamSpanner(v)
    assert len(p.components) == 1
    assert len(p.leaves) == 7
    p.detach()

    p = spannertools.BeamSpanner(v[:])
    assert len(p.components) == 3
    assert len(p.leaves) == 7
    p.detach()


def test_BeamSpanner_span_anonymous_14():
    r'''Nested tuplets.
    '''

    tinner = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tinner, Note("c'4")])

    r'''
    \times 2/3 {
        c'4
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        c'4
    }
    '''

    p = spannertools.BeamSpanner(t)
    assert len(p.components) == 1
    assert len(p.leaves) == 5
    p.detach()

    p = spannertools.BeamSpanner(t[:])
    assert len(p.components) == 3
    assert len(p.leaves) == 5


def test_BeamSpanner_span_anonymous_15():
    r'''Beams cannot cross voice boundaries.
    '''

    v1 = Voice([Note(i , (1, 8)) for i in range(3)])
    n = Note(3, (1,8))
    v2 = Voice([Note(i , (1, 8)) for i in range(4, 8)])
    t = Staff([v1, n, v2])

    r'''
    \new Staff {
        \new Voice {
            c'8
            cs'8
            d'8
        }
        ef'8
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert py.test.raises(
        AssertionError, 
        'p = spannertools.BeamSpanner([t[0], t[1]])')

    assert py.test.raises(
        AssertionError, 
        'p = spannertools.BeamSpanner([t[1], t[2]])')
