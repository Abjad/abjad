# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_BeamSpanner_span_like_named_01():
    r'''Abjad lets you span liked named voices.
    '''

    staff = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    staff[0].name = 'foo'
    staff[1].name = 'foo'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)

    p = spannertools.BeamSpanner(staff)
    assert len(p.components) == 1
    assert isinstance(p.components[0], Staff)
    assert len(p.leaves) == 8
    assert testtools.compare(
        staff.lilypond_format,
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
    p.detach()

    p = spannertools.BeamSpanner(staff[:])
    assert len(p.components) == 2
    for x in p.components:
        assert isinstance(x, Voice)
    assert len(p.leaves) == 8
    assert testtools.compare(
        staff.lilypond_format,
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


def test_BeamSpanner_span_like_named_02():
    '''
    Abjad does NOT lets you span over liked named staves.
    '''

    container = Container(Staff([Voice(notetools.make_repeated_notes(4))]) * 2)
    container[0].name, container[1].name = 'foo', 'foo'
    container[0][0].name, container[1][0].name = 'bar', 'bar'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner(container)')

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner(container[:])')

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner([container[0][0], container[1][0]])')


def test_BeamSpanner_span_like_named_03():
    '''
    Like-named containers need not be lexically contiguous.
    '''

    container = Container(Container(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    container[0].is_parallel = True
    container[1].is_parallel = True
    container[0][0].name, container[1][1].name = 'first', 'first'
    container[0][1].name, container[1][0].name = 'second', 'second'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)

    p = spannertools.BeamSpanner([container[0][0], container[1][1]])
    assert len(p.components) == 2
    assert isinstance(p.components[0], Voice)
    assert isinstance(p.components[1], Voice)
    assert len(p.leaves) == 8
    p.detach()

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
    container[0].is_parallel = True
    container[1].is_parallel = True
    container[0][0].name, container[1][0].name = 'first', 'first'
    container[0][1].name, container[1][1].name = 'second', 'second'
    del(container[1][1])
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)
    p = spannertools.BeamSpanner([container[0][0], container[1][0]])

    assert len(p.components) == 2
    assert len(p.leaves) == 8

    assert testtools.compare(
        container.lilypond_format,
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
