# -*- encoding: utf-8 -*-
from abjad import *


def test_SlurSpanner___init___01():
    r'''Init empty slur spanner.
    '''

    slur = spannertools.SlurSpanner()
    assert isinstance(slur, spannertools.SlurSpanner)


def test_SlurSpanner___init___02():
    r'''You can span across staves if they and
    all their subcontexts are equally named.
    '''

    container = Container(
        Staff(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    container[0].is_simultaneous = True
    container[1].is_simultaneous = True
    container[0].name, container[1].name = 'foo', 'foo'
    container[0][0].name, container[1][0].name = 'first', 'first'
    container[0][1].name, container[1][1].name = 'second', 'second'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(
        container)
    leaves = container[0][0][:] +  container[1][0][:]
    slur = spannertools.SlurSpanner(leaves)

    assert testtools.compare(
        container,
        r'''
        {
            \context Staff = "foo" <<
                \context Voice = "first" {
                    c'8 (
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
                    b'8 )
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
        )

    assert inspect(container).is_well_formed()


def test_SlurSpanner___init___03():
    '''You can span over liked named staves
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

    assert inspect(container).is_well_formed()


