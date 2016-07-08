# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner___getitem___01():
    r'''Get at nonnegative index in spanner.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert beam[0] is leaves[0]


def test_spannertools_Spanner___getitem___02():
    r'''Get at negative index in spanner.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert beam[-1] is leaves[-1]


def test_spannertools_Spanner___getitem___03():
    r'''Get slice from spanner.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert beam[-2:] == leaves[-2:]


def test_spannertools_Spanner___getitem___04():
    r'''Get all spanner components.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert beam[:] == leaves[:]
