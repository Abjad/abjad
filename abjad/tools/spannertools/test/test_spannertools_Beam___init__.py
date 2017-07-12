# -*- coding: utf-8 -*-
import abjad
import pytest


def test_spannertools_Beam___init___01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
    beam = abjad.Beam()
    abjad.attach(beam, staff[:4])

    assert format(staff) == abjad.String.normalize(
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

    assert len(beam) == 4


def test_spannertools_Beam___init___02():
    r'''Nonempty container.
    '''

    container = abjad.Container("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    beam = abjad.Beam()
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
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

    assert len(beam) == 8


def test_spannertools_Beam___init___03():
    r'''Nested nonempty containers.
    '''

    staff = abjad.Staff("{ c'8 c'8 c'8 c'8 } { c'8 c'8 c'8 c'8 }")
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(staff) == abjad.String.normalize(
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

    assert len(beam) == 8


def test_spannertools_Beam___init___04():
    r'''Beamed container and top-level leaves housed in staff.
    '''

    staff = abjad.Staff("{ c'8 c'8 c'8 c'8 } c'8 c'8")
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(staff) == abjad.String.normalize(
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

    assert len(beam) == 6


def test_spannertools_Beam___init___05():
    r'''Beamed leaves housed in staff and container.
    '''

    staff = abjad.Staff("{ c'8 c'8 c'8 c'8 } c'8 c'8")
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(staff) == abjad.String.normalize(
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

    assert len(beam) == 6


def test_spannertools_Beam___init___06():
    r'''Staff with empty containers at the edges.
    '''

    staff = abjad.Staff(abjad.Container([]) * 2)
    staff.insert(1, abjad.Container(abjad.Note(0, (1, 8)) * 4))
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(staff) == abjad.String.normalize(
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

    assert len(beam) == 4


def test_spannertools_Beam___init___07():
    r'''Deeply nested containers of equal depth.
    '''

    voice = abjad.Voice("{ { c'8 cs'8 d'8 ef'8 } } { { e'8 f'8 fs'8 g'8 } }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
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

    assert len(beam) == 8


def test_spannertools_Beam___init___08():
    r'''Deeply nested containers of unequal depth.
    '''

    voice = abjad.Voice("{ { { c'8 cs'8 d'8 ef'8 } } } { e'8 f'8 fs'8 g'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                {
                    {
                        c'8 [
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
                g'8 ]
            }
        }
        '''
        ), repr(f(voice))

    assert len(beam) == 8


def test_spannertools_Beam___init___09():
    r'''Voice with containers and top-level leaves.
    '''

    voice = abjad.Voice("{ c'8 cs'8 } d'8 { ef'8 e'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
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

    assert len(beam) == 5

def test_spannertools_Beam___init___10():
    r'''Voice with tuplets and top-level leaves.
    '''

    voice = abjad.Voice(r"\times 2/3 { c'8 cs' d' } ef'8 \times 2/3 { e'8 f' fs' }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
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

    assert len(beam) == 7


def test_spannertools_Beam___init___11():
    r'''Nested tuplets.
    '''

    tuplet = abjad.Tuplet((2, 3), r"c'4 \times 2/3 { c'8 c'8 c'8 } c'4")
    beam = abjad.Beam()
    abjad.attach(beam, tuplet[1][:])

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'4
            \times 2/3 {
                c'8 [
                c'8
                c'8 ]
            }
            c'4
        }
        '''
        )

    assert len(beam) == 3


def test_spannertools_Beam___init___12():
    r'''Beams can not cross voice boundaries.
    '''

    staff = abjad.Staff([
        abjad.Voice("c'8 cs'8 d'8"),
        abjad.Note("ef'8"),
        abjad.Voice("e'8 f' fs' g'")]
        )

    assert format(staff) == abjad.String.normalize(
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

    beam = abjad.Beam()
    leaves = abjad.select(staff).by_leaf()
    statement = 'attach(beam, leavs)'
    assert pytest.raises(Exception, statement)


def test_spannertools_Beam___init___13():
    r'''You can span the counttime components of like-named voices.
    '''

    staff = abjad.Staff([abjad.Voice("c'8 cs'8 d'8 ef'8"), abjad.Voice("e'8 f'8 fs'8 g'8")])
    staff[0].name = 'foo'
    staff[1].name = 'foo'
    beam = abjad.Beam()
    abjad.attach(beam, staff[0][:] + staff[1][:])

    assert format(staff) == abjad.String.normalize(
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

    assert len(beam) == 8


def test_spannertools_Beam___init___14():
    '''Like-named containers need not be lexically contiguous.
    '''

    container = abjad.Container(r'''
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

    beam = abjad.Beam()
    abjad.attach(beam, container[0][0][:] + container[1][1][:])

    assert format(container) == abjad.String.normalize(
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

    assert len(beam) == 8


def test_spannertools_Beam___init___15():
    '''Asymmetric structures are no problem.
    '''

    container = abjad.Container(
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

    beam = abjad.Beam()
    abjad.attach(beam, container[0][0][:] + container[1][0][:])

    assert format(container) == abjad.String.normalize(
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

    assert len(beam) == 8


def test_spannertools_Beam___init___16():
    r'''Notes in voice accept spanner even lodged within
    simultaneous parent container.
    '''

    container = abjad.Container(
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

    beam = abjad.Beam()
    abjad.attach(beam, container[0][:])

    assert format(container) == abjad.String.normalize(
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

    assert len(beam) == 4


def test_spannertools_Beam___init___17():
    r'''You can not yet span noncontiguous counttime components
    in the same logical voice. Lilypond is happy with this situation, though.
    '''

    staff = abjad.Staff(
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

    assert format(staff) == abjad.String.normalize(
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
    beam = abjad.Beam()
    statement = 'beam.attacch(leaves)'
    assert pytest.raises(Exception, statement)


def test_spannertools_Beam___init___18():
    r'''You can span counttime components in three chunks.
    '''

    staff = abjad.Staff(r'''
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
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(staff) == abjad.String.normalize(
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

    assert len(beam) == 12


def test_spannertools_Beam___init___19():
    r'''You can not span across differently named voices.
    '''

    staff = abjad.Staff([abjad.Voice("c'8 cs'8 d'8 ef'8"), abjad.Voice("e'8 f'8 fs'8 g'8")])
    staff[0].name = 'foo'
    staff[1].name = 'bar'

    assert format(staff) == abjad.String.normalize(
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

    selector = abjad.select().by_leaf(flatten=True)
    leaves = selector(staff)
    beam = abjad.Beam()
    statement = 'attach(beam, leaves)'
    assert pytest.raises(Exception, statement)
