# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_ContiguousSelection_partition_by_durations_exactly_01():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = marktools.TempoMark(Duration(1, 4), 60, target_context=Staff)
    attach(tempo, staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \tempo 4=60
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )


    leaves = staff.select_leaves()
    parts = leaves.partition_by_durations_exactly(
        [1.5],
        cyclic=True,
        in_seconds=True,
        overhang=False
        )

    r'''
    [
        [Note(c'', 8), Note(b', 8), Note(a', 8)],
        [Note(g', 8), Note(f', 8), Note(e', 8)]
    ]
    '''

    assert len(parts) == 2
    assert parts[0] == list(staff.select_leaves()[:3])
    assert parts[1] == list(staff.select_leaves()[3:6])


def test_selectiontools_ContiguousSelection_partition_by_durations_exactly_02():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = marktools.TempoMark(Duration(1, 4), 60, target_context = Staff)
    attach(tempo, staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \tempo 4=60
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )

    leaves = staff.select_leaves()
    parts = leaves.partition_by_durations_exactly(
        [1.5],
        cyclic=True,
        in_seconds=True,
        overhang=True,
        )

    r'''
    [
        [Note(c'', 8), Note(b', 8), Note(a', 8)],
        [Note(g', 8), Note(f', 8), Note(e', 8)],
        [Note(d', 8), Note(c', 8)]
    ]
    '''

    assert len(parts) == 3
    assert parts[0] == list(staff.select_leaves()[:3])
    assert parts[1] == list(staff.select_leaves()[3:6])
    assert parts[2] == list(staff.select_leaves()[6:8])


def test_selectiontools_ContiguousSelection_partition_by_durations_exactly_03():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )

    leaves = staff.select_leaves()
    parts = leaves.partition_by_durations_exactly(
        [Duration(3, 8)],
        cyclic=True,
        in_seconds=False,
        overhang=True,
        )

    r'''
    [
        [Note(c'', 8), Note(b', 8), Note(a', 8)]
        [Note(g', 8), Note(f', 8), Note(e', 8)]
        [Note(d', 8), Note(c', 8)]
    ]
    '''

    assert len(parts) == 3
    assert parts[0] == list(staff.select_leaves()[:3])
    assert parts[1] == list(staff.select_leaves()[3:6])
    assert parts[2] == list(staff.select_leaves()[6:8])


def test_selectiontools_ContiguousSelection_partition_by_durations_exactly_04():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = marktools.TempoMark(Duration(1, 4), 60, target_context=Staff)
    attach(tempo, staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \tempo 4=60
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )

    leaves = staff.select_leaves()
    parts = leaves.partition_by_durations_exactly(
        [1.5],
        cyclic=False,
        in_seconds=True,
        overhang=False,
        )

    "[[Note(c'', 8), Note(b', 8), Note(a', 8)]]"

    assert len(parts) == 1
    assert parts[0] == list(staff.select_leaves()[:3])


def test_selectiontools_ContiguousSelection_partition_by_durations_exactly_05():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )

    leaves = staff.select_leaves()
    parts = leaves.partition_by_durations_exactly(
        [Duration(3, 8)],
        cyclic=False,
        in_seconds=False,
        overhang=False,
        )

    "[[Note(c'', 8), Note(b', 8), Note(a', 8)]]"

    assert len(parts) == 1
    assert parts[0] == list(staff.select_leaves()[:3])
