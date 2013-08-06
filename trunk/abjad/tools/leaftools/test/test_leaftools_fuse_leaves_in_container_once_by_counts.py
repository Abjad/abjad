# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_fuse_leaves_in_container_once_by_counts_01():

    t = Voice(notetools.make_repeated_notes(5, Duration(1, 16)))
    spannertools.SlurSpanner(t[:])
    leaftools.fuse_leaves_in_container_once_by_counts(
        t,
        [1, 2, 2],
        leaf_class=Note,
        decrease_durations_monotonically=True)

    r'''
    \new Voice {
      c'16 (
      c'8
      c'8 )
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'16 (
            c'8
            c'8 )
        }
        '''
        )


def test_leaftools_fuse_leaves_in_container_once_by_counts_02():

    t = Voice(notetools.make_repeated_notes(5))
    spannertools.SlurSpanner(t[:])
    leaftools.fuse_leaves_in_container_once_by_counts(
        t, 
        [5], 
        leaf_class=Note,
        decrease_durations_monotonically=True)

    r'''
    \new Voice {
      c'2 ( ~
      c'8 )
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'2 ( ~
            c'8 )
        }
        '''
        )


def test_leaftools_fuse_leaves_in_container_once_by_counts_03():

    t = Voice(notetools.make_repeated_notes(5))
    leaftools.fuse_leaves_in_container_once_by_counts(
        t, 
        [1, 2, 2], 
        leaf_class=Rest, 
        decrease_durations_monotonically=True)

    r'''
    \new Voice {
      r8
      r4
      r4
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
        '\\new Voice {\n\tr8\n\tr4\n\tr4\n}'
        )


def test_leaftools_fuse_leaves_in_container_once_by_counts_04():

    t = Voice(notetools.make_repeated_notes(5))
    spannertools.SlurSpanner(t)
    leaftools.fuse_leaves_in_container_once_by_counts(
        t, 
        [5], 
        leaf_class=Note, 
        decrease_durations_monotonically=False)

    r'''
    \new Voice {
      c'8 ( ~
      c'2 )
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 ( ~
            c'2 )
        }
        '''
        )
