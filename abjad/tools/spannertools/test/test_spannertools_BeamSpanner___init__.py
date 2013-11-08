# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_BeamSpanner___init___01():
    r'''Initalize empty beam spanner.
    '''

    beam = BeamSpanner()
    assert isinstance(beam, BeamSpanner)


def test_BeamSpanner___init___02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beam = BeamSpanner()
    attach(beam, staff[:4])

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

    assert inspect(staff).is_well_formed()


def test_BeamSpanner___init___03():
    r'''Empty container.
    '''

    container = Container([])
    beam = BeamSpanner()
    attach(beam, container)

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


def test_BeamSpanner___init___04():
    r'''Nonempty container.
    '''

    container = Container("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    beam = BeamSpanner()
    attach(beam, container)

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


def test_BeamSpanner___init___05():
    r'''Nested nonempty containers.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } { c'8 c'8 c'8 c'8 }")
    beam = BeamSpanner()
    attach(beam, staff[:])

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


def test_BeamSpanner___init___06():
    r'''Beamed container and top-level leaves housed in staff.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } c'8 c'8")
    beam = BeamSpanner()
    attach(beam, staff[:])

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


def test_BeamSpanner___init___07():
    r'''Beamed leaves housed in staff and container.
    '''

    staff = Staff("{ c'8 c'8 c'8 c'8 } c'8 c'8")
    beam = BeamSpanner()
    attach(beam, staff.select_leaves())

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


def test_BeamSpanner___init___08():
    r'''Staff with empty containers.
    '''

    staff = Staff("{} {} {}")
    beam = BeamSpanner()
    attach(beam, staff[:])

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


def test_BeamSpanner___init___09():
    r'''Staff with empty containers at the edges.
    '''

    staff = Staff(Container([]) * 2)
    staff.insert(1, Container(Note(0, (1, 8)) * 4))
    beam = BeamSpanner()
    attach(beam, staff[:])

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


def test_BeamSpanner___init___10():
    r'''Deeply nested containers of equal depth.
    '''

    voice = Voice("{ { c'8 cs'8 d'8 ef'8 } } { { e'8 f'8 fs'8 g'8 } }")
    beam = BeamSpanner()
    attach(beam, voice[:])

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

    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    detach(beam, voice)
    beam = BeamSpanner()
    attach(beam, [voice[0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    detach(beam, voice)
    beam = BeamSpanner()
    attach(beam, [voice[0][0], voice[1][0]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    detach(beam, voice)
    beam = BeamSpanner()
    attach(beam, [voice[0], voice[1][0]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    detach(beam, voice)
    beam = BeamSpanner()
    attach(beam, [voice[0][0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8


def test_BeamSpanner___init___11():
    r'''Deeply nested containers of unequal depth.
    '''

    voice = Voice("{ { { c'8 cs'8 d'8 ef'8 } } } { e'8 f'8 fs'8 g'8 }")
    beam = BeamSpanner()
    attach(beam, voice[:])

    # note that calling testtools.compare() here breaks Python's assertions

    beam = BeamSpanner()
    attach(beam, [voice[0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8
    beam.detach()

    beam = BeamSpanner()
    attach(beam, [voice[0][0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8
    beam.detach()

    beam = BeamSpanner()
    attach(beam, [voice[0][0][0], voice[1]])
    assert len(beam.components) == 2
    assert len(beam.leaves) == 8
    beam.detach()


def test_BeamSpanner___init___12():
    r'''Voice with containers and top-level leaves.
    '''

    voice = Voice("{ c'8 cs'8 } d'8 { ef'8 e'8 }")
    beam = BeamSpanner()
    attach(beam, voice[:])

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


def test_BeamSpanner___init___13():
    r'''Voice with tuplets and top-level leaves.
    '''

    voice = Voice(r"\times 2/3 { c'8 cs' d' } ef'8 \times 2/3 { e'8 f' fs' }")
    beam = BeamSpanner()
    attach(beam, voice[:])

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


def test_BeamSpanner___init___14():
    r'''Nested tuplets.
    '''

    tuplet = Tuplet((2, 3), r"c'4 \times 2/3 { c'8 c'8 c'8 } c'4")

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

    beam = BeamSpanner()
    attach(beam, tuplet)
    assert len(beam.components) == 1
    assert len(beam.leaves) == 5
    beam.detach()

    beam = BeamSpanner()
    attach(beam, tuplet[:])
    assert len(beam.components) == 3
    assert len(beam.leaves) == 5


def test_BeamSpanner___init___15():
    r'''Beams cannot cross voice boundaries.
    '''

    staff = Staff([
        Voice("c'8 cs'8 d'8"), 
        Note("ef'8"), 
        Voice("e'8 f' fs' g'")]
        )

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

    beam = BeamSpanner()
    statement = 'attach(beam, [staff[0], staff[1]])'
    assert pytest.raises(Exception, statement)

    statement = 'attach(beam, [staff[1], staff[2]])'
    assert pytest.raises(Exception, statement)


def test_BeamSpanner___init___16():
    r'''You can span the counttime components of like-named voices.
    '''

    staff = Staff([Voice("c'8 cs'8 d'8 ef'8"), Voice("e'8 f'8 fs'8 g'8")])
    staff[0].name = 'foo'
    staff[1].name = 'foo'
    beam = BeamSpanner()
    attach(beam, staff[0][:] + staff[1][:])

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

    assert len(beam.components) == 8
    assert len(beam.leaves) == 8


def test_BeamSpanner___init___17():
    '''Like-named containers need not be lexically contiguous.
    '''

    container = Container(r'''
        <<
            \context Voice = "first" {
                c'8
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
                ef''8
            }
        >>
        ''')

    beam = BeamSpanner()
    attach(beam, container[0][0][:] + container[1][1][:])

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
        )

    assert len(beam.components) == 8
    assert len(beam.leaves) == 8


def test_BeamSpanner___init___18():
    '''Asymmetric structures are no problem.
    '''

    container = Container(
        r'''
        <<
            \context Voice = "first" {
                c'8
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
                b'8
            }
        >>
        ''')

    beam = BeamSpanner()
    attach(beam, container[0][0][:] + container[1][0][:])

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

    assert len(beam.components) == 8
    assert len(beam.leaves) == 8


def test_BeamSpanner___init___19():
    r'''Spanners will not inspect the contents of simultaneous containers.
    '''

    container = Container([])
    container.is_simultaneous = True
    beam = BeamSpanner()
    attach(beam, container)

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


def test_BeamSpanner___init___20():
    r'''Notes in voice accept spanner even lodged within 
    simultaneous parent container.
    '''

    container = Container(
        r'''
        <<
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
        >>
        ''')

    beam = BeamSpanner()
    attach(beam, container[0][:])

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

    assert len(beam.components) == 4


def test_BeamSpanner___init___21():
    r'''You can not yet span noncontiguous counttime components
    in the same logical voice. Lilypond is happy with this situation, though.
    '''

    staff = Staff(
        r'''
        c'8
        cs'8
        <<
            \new Voice {
                d'8
                ef'8
                e'8
                f'8
            }
            \new Voice {
                fs'8
                g'8
                af'8
                a'8
            }
        >>
        bf'8
        b'8
        ''')

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            cs'8
            <<
                \new Voice {
                    d'8
                    ef'8
                    e'8
                    f'8
                }
                \new Voice {
                    fs'8
                    g'8
                    af'8
                    a'8
                }
            >>
            bf'8
            b'8
        }
        '''
        )

    leaves = staff[:2] + staff[-2:]
    beam = BeamSpanner()
    statement = 'beam.attacch(leaves)'
    assert pytest.raises(Exception, statement)


def test_BeamSpanner___init___22():
    r'''You can span counttime components in three chunks.
    '''

    staff = Staff(r'''
        \context Voice = "foo" {
            c'8
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
            ef''8
        }
        ''')

    leaves = staff[0][:] + staff[1][0][:] + staff[2][:]
    beam = BeamSpanner()
    attach(beam, leaves)

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

    assert len(beam.components) == 12
    assert len(beam.leaves) == 12


def test_BeamSpanner___init___23():
    r'''You can not span across differently named voices.
    '''

    staff = Staff([Voice("c'8 cs'8 d'8 ef'8"), Voice("e'8 f'8 fs'8 g'8")])
    staff[0].name = 'foo'
    staff[1].name = 'bar'

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
    beam = BeamSpanner()
    statement = 'attach(beam, leaves)'
    assert pytest.raises(Exception, statement)
