# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_BeamSpanner___init___01():
    r'''Initalize empty beam spanner.
    '''

    beam = spannertools.BeamSpanner()
    assert isinstance(beam, spannertools.BeamSpanner)


def test_BeamSpanner___init___02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.BeamSpanner(staff[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )

    assert select(staff).is_well_formed()


def test_BeamSpanner_span_anonymous_01():
    r'''Empty container.
    '''

    container = Container([])
    beam = spannertools.BeamSpanner(container)

    assert testtools.compare(
        container,
        r'''
        {
        }
        '''
        )

    assert len(beam.components) == 1
    assert isinstance(beam.components[0], Container)
    assert len(beam.leaves) == 0


def test_BeamSpanner_span_anonymous_02():
    r'''Nonempty container.
    '''

    container = Container("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    beam = spannertools.BeamSpanner(container)

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

    assert len(beam.components) == 1
    assert isinstance(beam.components[0], Container)
    assert len(beam.leaves) == 8


def test_BeamSpanner_span_anonymous_03():
    r'''Nested nonempty containers.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } { c'8 c'8 c'8 c'8 }")
    beam = spannertools.BeamSpanner(staff[:])

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

    assert len(beam.components) == 2
    assert type(beam.components[0]) is Container
    assert type(beam.components[1]) is Container
    assert len(beam.leaves) == 8


def test_BeamSpanner_span_anonymous_05():
    r'''Beamed container and top-level leaves housed in staff.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } c'8 c'8")
    beam = spannertools.BeamSpanner(staff[:])

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

    assert len(beam.components) == 3
    assert type(beam.components[0]) is Container
    assert type(beam.components[1]) is Note
    assert type(staff[2]) is Note
    assert len(beam.leaves) == 6


def test_BeamSpanner_span_anonymous_06():
    r'''Beamed leaves housed in staff and container.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } c'8 c'8")
    beam = spannertools.BeamSpanner(staff.select_leaves())

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

    assert len(beam.components) == 6
    assert all(type(x) is Note for x in beam.components)
    assert len(beam.leaves) == 6


def test_BeamSpanner_span_anonymous_07():
    r'''Staff with empty containers.
    '''

    staff = Staff("{} {} {}")
    beam = spannertools.BeamSpanner(staff[:])

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

    assert len(beam.components) == 3
    assert all(type(x) is Container for x in beam.components)
    assert len(beam.leaves) == 0


def test_BeamSpanner_span_anonymous_08():
    r'''Staff with empty containers at the edges.
    '''

    staff = Staff(Container([]) * 2)
    staff.insert(1, Container(Note(0, (1, 8)) * 4))
    beam = spannertools.BeamSpanner(staff[:])

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

    assert len(beam.components) == 3
    for x in beam.components:
        assert isinstance(x, Container)
    assert len(beam.leaves) == 4


def test_BeamSpanner_span_anonymous_09():
    r'''Deeply nested containers of equal depth.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    s2 = Container([s2])
    voice = Voice([s1, s2])
    beam = spannertools.BeamSpanner(voice[:])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                {
                    c'8 [
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
                    g'8 ]
                }
            }
        }
        '''
        )

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


def test_BeamSpanner_span_anonymous_10():
    r'''Deeply nested containers of unequal depth.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    voice = Voice([s1, s2])

    assert testtools.compare(
        voice,
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
        )

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


def test_BeamSpanner_span_anonymous_11():
    r'''Voice with containers and top-level leaves.
    '''

    s1 = Container([Note(i, (1, 8)) for i in range(2)])
    s2 = Container([Note(i, (1, 8)) for i in range(3, 5)])
    voice = Voice([s1, Note(2, (1, 8)), s2])
    beam = spannertools.BeamSpanner(voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                cs'8
            }
            d'8
            {
                ef'8
                e'8 ]
            }
        }
        '''
        )

    assert len(beam.components) == 3
    assert len(beam.leaves) == 5
    beam.detach()


def test_BeamSpanner_span_anonymous_12():
    r'''Voice with tuplets and top-level leaves.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(4,7)])
    voice = Voice([t1, Note(3, (1,8)), t2])
    beam = spannertools.BeamSpanner(voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                cs'8
                d'8
            }
            ef'8
            \times 2/3 {
                e'8
                f'8
                fs'8 ]
            }
        }
        '''
        )

    assert len(beam.components) == 3
    assert len(beam.leaves) == 7
    beam.detach()


def test_BeamSpanner_span_anonymous_13():
    r'''Nested tuplets.
    '''

    tinner = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tinner, Note("c'4")])

    assert testtools.compare(
        tuplet,
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
        )

    beam = spannertools.BeamSpanner(tuplet)
    assert len(beam.components) == 1
    assert len(beam.leaves) == 5
    beam.detach()

    beam = spannertools.BeamSpanner(tuplet[:])
    assert len(beam.components) == 3
    assert len(beam.leaves) == 5


def test_BeamSpanner_span_anonymous_14():
    r'''Beams cannot cross voice boundaries.
    '''

    v1 = Voice([Note(i , (1, 8)) for i in range(3)])
    note = Note(3, (1,8))
    v2 = Voice([Note(i , (1, 8)) for i in range(4, 8)])
    staff = Staff([v1, note, v2])

    assert testtools.compare(
        staff,
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
        )

    assert py.test.raises(
        AssertionError, 
        'beam = spannertools.BeamSpanner([staff[0], staff[1]])')

    assert py.test.raises(
        AssertionError, 
        'beam = spannertools.BeamSpanner([staff[1], staff[2]])')


def test_BeamSpanner_span_like_named_01():
    r'''Abjad lets you span liked named voices.
    '''

    staff = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    staff[0].name = 'foo'
    staff[1].name = 'foo'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)

    beam = spannertools.BeamSpanner(staff)
    assert len(beam.components) == 1
    assert isinstance(beam.components[0], Staff)
    assert len(beam.leaves) == 8

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            \context Voice = "foo" {
                e'8
                f'8
                fs'8
                g'8 ]
            }
        }
        '''
        )
    beam.detach()

    beam = spannertools.BeamSpanner(staff[:])
    assert len(beam.components) == 2
    for x in beam.components:
        assert isinstance(x, Voice)
    assert len(beam.leaves) == 8

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            \context Voice = "foo" {
                e'8
                f'8
                fs'8
                g'8 ]
            }
        }
        '''
        )


# TODO: move to slur spanner test file
def test_BeamSpanner_span_like_named_02():
    '''Abjad lets you span over liked named staves
    so long as the voices nested in the staves are named the same.
    '''

    container = Container(
        Staff([Voice(notetools.make_repeated_notes(4))]) * 2)
    container[0].name, container[1].name = 'foo', 'foo'
    container[0][0].name, container[1][0].name = 'bar', 'bar'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(
        container)
    slur = spannertools.SlurSpanner(container)


    assert testtools.compare(
        container,
        r'''
        {
            \context Staff = "foo" {
                \context Voice = "bar" {
                    c'8 (
                    cs'8
                    d'8
                    ef'8
                }
            }
            \context Staff = "foo" {
                \context Voice = "bar" {
                    e'8
                    f'8
                    fs'8
                    g'8 )
                }
            }
        }
        '''
        )

    assert select(container).is_well_formed()


def test_BeamSpanner_span_like_named_03():
    '''Like-named containers need not be lexically contiguous.
    '''

    container = Container(Container(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    container[0].is_simultaneous = True
    container[1].is_simultaneous = True
    container[0][0].name, container[1][1].name = 'first', 'first'
    container[0][1].name, container[1][0].name = 'second', 'second'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)

    beam = spannertools.BeamSpanner([container[0][0], container[1][1]])
    assert len(beam.components) == 2
    assert isinstance(beam.components[0], Voice)
    assert isinstance(beam.components[1], Voice)
    assert len(beam.leaves) == 8
    beam.detach()

    r'''
    {
        <<
            \context Voice = "first" {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            \context Voice = "second" {
                e'8
                f'8
                fs'8
                g'8
            }
        >>
        <<
            \context Voice = "second" {
                af'8
                a'8
                bf'8
                b'8
            }
            \context Voice = "first" {
                c''8
                cs''8
                d''8
                ef''8 ]
            }
        >>
    }
    '''


def test_BeamSpanner_span_like_named_04():
    '''
    Asymmetric structures are no problem.
    '''

    container = Container(Container(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    container[0].is_simultaneous = True
    container[1].is_simultaneous = True
    container[0][0].name, container[1][0].name = 'first', 'first'
    container[0][1].name, container[1][1].name = 'second', 'second'
    del(container[1][1])
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)
    beam = spannertools.BeamSpanner([container[0][0], container[1][0]])

    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    assert testtools.compare(
        container,
        r'''
        {
            <<
                \context Voice = "first" {
                    c'8 [
                    cs'8
                    d'8
                    ef'8
                }
                \context Voice = "second" {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
            >>
            <<
                \context Voice = "first" {
                    af'8
                    a'8
                    bf'8
                    b'8 ]
                }
            >>
        }
        '''
        )

    r'''
    {
        <<
            \context Voice = "first" {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            \context Voice = "second" {
                e'8
                f'8
                fs'8
                g'8
            }
        >>
        <<
            \context Voice = "first" {
                af'8
                a'8
                bf'8
                b'8 ]
            }
        >>
    }
    '''


def test_BeamSpanner_span_simultaneous_container_01():
    r'''Abjad spanners will not inspect the contents of simultaneous containers.
    '''

    container = Container([])
    container.is_simultaneous = True
    beam = spannertools.BeamSpanner(container)

    assert len(beam.components) == 1
    assert beam.components[0] is container
    assert len(beam.leaves) == 0
    assert testtools.compare(
        container,
        r'''
        <<
        >>
        '''
        )


def test_BeamSpanner_span_simultaneous_container_02():
    r'''Nonempty spanned simultaneous container.
    '''

    container = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    container.is_simultaneous = True
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)

    assert py.test.raises(AssertionError, 'beam = spannertools.BeamSpanner(container)')

#   assert len(beam.components) == 1
#   assert beam.components[0] is container
#   assert len(beam.leaves) == 0
#   assert container.lilypond_format == "<<\n\container{\n\container\tc'8\n\container\tcs'8\n\container\td'8\n\container\tef'8\n\container}\n\container{\n\container\te'8\n\container\tf'8\n\container\tfs'8\n\container\tg'8\n\container}\n>>"
#
#   r'''<<
#      {
#         c'8
#         cs'8
#         d'8
#         ef'8
#      }
#      {
#         e'8
#         f'8
#         fs'8
#         g'8
#      }
#   >>'''


def test_BeamSpanner_span_simultaneous_container_03():
    r'''Voice accepts spanner,
        even lodged within simultaneous parent container.'''

    container = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    container.is_simultaneous = True
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)
    beam = spannertools.BeamSpanner(container[0])

    assert len(beam.components) == 1
    assert isinstance(beam.components[0], Container)
    assert testtools.compare(
        container,
        r'''
        <<
            \new Voice {
                c'8 [
                cs'8
                d'8
                ef'8 ]
            }
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
        >>
        '''
        )

    r'''
    <<
        \new Voice {
            c'8 [
            cs'8
            d'8
            ef'8 ]
        }
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
    >>
    '''


def test_BeamSpanner_span_simultaneous_container_04():
    r'''Abjad forbids but LilyPond is happy.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    new = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    new.is_simultaneous = True
    staff.insert(2, new)
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)

    assert py.test.raises(AssertionError, 'beam = spannertools.BeamSpanner(staff)')


def test_BeamSpanner_span_simultaneous_container_05():
    r'''This is the proper way to follow a logical voice
    through simultaneous containers.
    LilyPond is happy here again.
    '''

    staff = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    staff[0].name, staff[1].name = 'foo', 'foo'
    new = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    new.is_simultaneous = True
    staff.insert(1, new)
    staff[1][0].name = 'foo'
    staff[1][1].name = 'bar'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)
    beam = spannertools.BeamSpanner([staff[0], staff[1][0], staff[2]])

    assert len(beam.components) == 3
    assert beam.components[0] is staff[0]
    assert beam.components[1] is staff[1][0]
    assert beam.components[2] is staff[2]
    assert len(beam.leaves) == 12
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            <<
                \context Voice = "foo" {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                \context Voice = "bar" {
                    af'8
                    a'8
                    bf'8
                    b'8
                }
            >>
            \context Voice = "foo" {
                c''8
                cs''8
                d''8
                ef''8 ]
            }
        }
        '''
        )


def test_BeamSpanner_span_differently_named_01():
    r'''You can not span across differently named voices.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v1.name = 'foo'
    v2 = Voice(notetools.make_repeated_notes(4))
    v2.name = 'bar'
    staff = Staff([v1, v2])
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(
        staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8
                cs'8
                d'8
                ef'8
            }
            \context Voice = "bar" {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    leaves = staff.select_leaves(allow_discontiguous_leaves=True)
    statement = 'spannertools.BeamSpanner(leaves)'
    assert py.test.raises(Exception, statement)
