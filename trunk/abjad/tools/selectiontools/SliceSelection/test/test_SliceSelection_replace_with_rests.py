# -*- encoding: utf-8 -*-
from abjad import *


def test_SliceSelection_replace_with_rests_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
    staff[:5].replace_with_rests(decrease_durations_monotonically=True)

    r'''
    \new Staff {
        r2
        r8
        a'8
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            r2
            r8
            a'8
        }
        '''
        )


def test_SliceSelection_replace_with_rests_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
    staff[-5:].replace_with_rests(decrease_durations_monotonically=True)

    r'''
    \new Staff {
        c'8
        r2
        r8
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            r2
            r8
        }
        '''
        )


def test_SliceSelection_replace_with_rests_03():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
    staff[:5].replace_with_rests(decrease_durations_monotonically=False)

    r'''
    \new Staff {
        r8
        r2
        a'8
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            r8
            r2
            a'8
        }
        '''
        )


def test_SliceSelection_replace_with_rests_04():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
    staff[-5:].replace_with_rests(decrease_durations_monotonically=False)

    r'''
    \new Staff {
        c'8
        r8
        r2
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            r8
            r2
        }
        '''
        )
