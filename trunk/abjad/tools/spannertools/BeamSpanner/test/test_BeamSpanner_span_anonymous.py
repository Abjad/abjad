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
        container,
        r'''
        {
        }
        '''
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
        container,
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
        staff,
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
        staff,
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
        staff,
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
        staff,
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
        staff,
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
        )


def test_BeamSpanner_span_anonymous_09():
    r'''Staff with empty containers at the edges.
    '''

    staff = Staff(Container([]) * 2)
    staff.insert(1, Container(Note(0, (1, 8)) * 4))
    beam = spannertools.BeamSpanner(staff[:])

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

    assert len(beam.components) == 3
    for x in beam.components:
        assert isinstance(x, Container)
    assert len(beam.leaves) == 4

    assert testtools.compare(
        staff,
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
        )


def test_BeamSpanner_span_anonymous_10():
    r'''Deeply nested containers of equal depth.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    s2 = Container([s2])
    voice = Voice([s1, s2])
    beam = spannertools.BeamSpanner(voice)
    assert len(beam.components) == 1
    assert len(beam.leaves) == 8

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

    beam.detach()
    beam = spannertools.BeamSpanner([voice[0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    beam.detach()
    beam = spannertools.BeamSpanner([voice[0][0], voice[1][0]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    beam.detach()
    beam = spannertools.BeamSpanner([voice[0], voice[1][0]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    beam.detach()
    beam = spannertools.BeamSpanner([voice[0][0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8


def test_BeamSpanner_span_anonymous_11():
    r'''Deeply nested containers of unequal depth.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    voice = Voice([s1, s2])

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

    beam = spannertools.BeamSpanner(voice)
    assert len(beam.components) == 1
    assert len(beam.leaves) == 8
    beam.detach()

    beam = spannertools.BeamSpanner([voice[0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8
    beam.detach()

    beam = spannertools.BeamSpanner([voice[0][0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8
    beam.detach()

    beam = spannertools.BeamSpanner([voice[0][0][0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8
    beam.detach()


def test_BeamSpanner_span_anonymous_12():
    r'''Voice with containers and top-level leaves.
    '''

    s1 = Container([Note(i, (1, 8)) for i in range(2)])
    s2 = Container([Note(i, (1, 8)) for i in range(3, 5)])
    voice = Voice([s1, Note(2, (1, 8)), s2])

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

    beam = spannertools.BeamSpanner(voice)
    assert len(beam.components) == 1
    assert len(beam.leaves) == 5
    beam.detach()

    beam = spannertools.BeamSpanner(voice[:])
    assert len(beam.components) == 3
    assert len(beam.leaves) == 5
    beam.detach()


def test_BeamSpanner_span_anonymous_13():
    r'''Voice with tuplets and top-level leaves.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(4,7)])
    voice = Voice([t1, Note(3, (1,8)), t2])

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

    beam = spannertools.BeamSpanner(voice)
    assert len(beam.components) == 1
    assert len(beam.leaves) == 7
    beam.detach()

    beam = spannertools.BeamSpanner(voice[:])
    assert len(beam.components) == 3
    assert len(beam.leaves) == 7
    beam.detach()


def test_BeamSpanner_span_anonymous_14():
    r'''Nested tuplets.
    '''

    tinner = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tinner, Note("c'4")])

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

    beam = spannertools.BeamSpanner(tuplet)
    assert len(beam.components) == 1
    assert len(beam.leaves) == 5
    beam.detach()

    beam = spannertools.BeamSpanner(tuplet[:])
    assert len(beam.components) == 3
    assert len(beam.leaves) == 5


def test_BeamSpanner_span_anonymous_15():
    r'''Beams cannot cross voice boundaries.
    '''

    v1 = Voice([Note(i , (1, 8)) for i in range(3)])
    note = Note(3, (1,8))
    v2 = Voice([Note(i , (1, 8)) for i in range(4, 8)])
    staff = Staff([v1, note, v2])

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
        'beam = spannertools.BeamSpanner([staff[0], staff[1]])')

    assert py.test.raises(
        AssertionError, 
        'beam = spannertools.BeamSpanner([staff[1], staff[2]])')
