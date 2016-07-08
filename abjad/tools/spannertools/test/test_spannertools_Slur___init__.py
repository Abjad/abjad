# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Slur___init___01():
    r'''Initialize empty slur spanner.
    '''

    slur = Slur()
    assert isinstance(slur, Slur)


def test_spannertools_Slur___init___02():
    r'''You can span across staves if they and
    all their subcontexts are equally named.
    '''

    container = Container(
        r'''
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
        '''
        )

    leaves = container[0][0][:] + container[1][0][:]
    slur = Slur()
    attach(slur, leaves)

    assert format(container) == stringtools.normalize(
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

    assert inspect_(container).is_well_formed()


def test_spannertools_Slur___init___03():
    '''You can span over liked named staves
    so long as the voices nested in the staves are named the same.
    '''

    container = Container(
        r'''
        \context Staff = "foo" {
            \context Voice = "bar" {
                c'8
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
                g'8
            }
        }
        '''
        )

    slur = Slur()
    leaves = select(container).by_leaf()
    attach(slur, leaves)

    assert format(container) == stringtools.normalize(
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

    assert inspect_(container).is_well_formed()
