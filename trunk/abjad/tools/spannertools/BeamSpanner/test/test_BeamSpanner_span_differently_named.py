# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_BeamSpanner_span_differently_named_01():
    r'''Abjad does NOT let you span across differently named Voices.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v1.name = 'foo'
    v2 = Voice(notetools.make_repeated_notes(4))
    v2.name = 'bar'
    staff = Staff([v1, v2])
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)

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

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner(staff)')

    p = spannertools.BeamSpanner(staff[0])

    r'''
    \new Staff {
        \context Voice = "foo" {
            c'8 [
            cs'8
            d'8
            ef'8 ]
        }
        \context Voice = "bar" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8 [
                cs'8
                d'8
                ef'8 ]
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


def test_BeamSpanner_span_differently_named_02():
    r'''Abjad does NOT let you span across Staves, even if they and
    all its sub-contexts are equally named.'''

    container = Container(Staff(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    container[0].is_parallel = True
    container[1].is_parallel = True
    container[0].name, container[1].name = 'foo', 'foo'
    container[0][0].name, container[1][0].name = 'first', 'first'
    container[0][1].name, container[1][1].name = 'second', 'second'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)

    r'''
    {
        \context Staff = "foo" <<
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
        \context Staff = "foo" <<
            \context Voice = "first" {
                af'8
                a'8
                bf'8
                b'8
            }
            \context Voice = "second" {
                c''8
                cs''8
                d''8
                ef''8
            }
        >>
    }
    '''

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner([container[0][0], container[1][0]])')
