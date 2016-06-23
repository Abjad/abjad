# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Selection_partition_by_durations_01():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = Tempo(Duration(1, 4), 60)
    attach(tempo, staff, scope=Staff)

    assert format(staff) == stringtools.normalize(
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


    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [1.5],
        cyclic=True,
        fill=Exact,
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
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:3])
    assert parts[1] == list(leaves[3:6])


def test_selectiontools_Selection_partition_by_durations_02():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = Tempo(Duration(1, 4), 60)
    attach(tempo, staff, scope=Staff)

    assert format(staff) == stringtools.normalize(
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

    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [1.5],
        cyclic=True,
        fill=Exact,
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
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:3])
    assert parts[1] == list(leaves[3:6])
    assert parts[2] == list(leaves[6:8])


def test_selectiontools_Selection_partition_by_durations_03():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert format(staff) == stringtools.normalize(
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

    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [Duration(3, 8)],
        cyclic=True,
        fill=Exact,
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
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:3])
    assert parts[1] == list(leaves[3:6])
    assert parts[2] == list(leaves[6:8])


def test_selectiontools_Selection_partition_by_durations_04():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = Tempo(Duration(1, 4), 60)
    attach(tempo, staff, scope=Staff)

    assert format(staff) == stringtools.normalize(
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

    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [1.5],
        cyclic=False,
        fill=Exact,
        in_seconds=True,
        overhang=False,
        )

    "[[Note(c'', 8), Note(b', 8), Note(a', 8)]]"

    assert len(parts) == 1
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:3])


def test_selectiontools_Selection_partition_by_durations_05():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert format(staff) == stringtools.normalize(
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

    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [Duration(3, 8)],
        cyclic=False,
        fill=Exact,
        in_seconds=False,
        overhang=False,
        )

    "[[Note(c'', 8), Note(b', 8), Note(a', 8)]]"

    assert len(parts) == 1
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:3])


def test_selectiontools_Selection_partition_by_durations_06():

    staff = Staff()
    staff.extend("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    staff.extend("abj: | 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert format(staff) == stringtools.normalize(
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

    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [Duration(3, 16), Duration(1, 16)],
        cyclic=True,
        fill=More,
        in_seconds=False,
        overhang=True,
        )

    r'''
    [
        [Note(c', 8), Note(d', 8)],
        [Note(e', 8)], [Note(f', 8), Note(g', 8)],
        [Note(a', 8)], [Note(b', 8), Note(c'', 8)]
    ]
    '''

    assert len(parts) == 5
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:2])
    assert parts[1] == list(leaves[2:3])
    assert parts[2] == list(leaves[3:5])
    assert parts[3] == list(leaves[5:6])
    assert parts[4] == list(leaves[6:])


def test_selectiontools_Selection_partition_by_durations_07():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = Tempo(Duration(1, 4), 60)
    attach(tempo, staff, scope=Staff)

    assert format(staff) == stringtools.normalize(
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

    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [0.75],
        cyclic=True,
        fill=Less,
        in_seconds=True,
        overhang=False,
        )

    r'''
    [
        [Note(c', 8)],
        [Note(d', 8)],
        [Note(e', 8)],
        [Note(f', 8)],
        [Note(g', 8)],
        [Note(a', 8)],
        [Note(b', 8)]
    ]
    '''

    assert len(parts) == 7
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:1])
    assert parts[1] == list(leaves[1:2])
    assert parts[2] == list(leaves[2:3])
    assert parts[3] == list(leaves[3:4])
    assert parts[4] == list(leaves[4:5])
    assert parts[5] == list(leaves[5:6])
    assert parts[6] == list(leaves[6:7])


def test_selectiontools_Selection_partition_by_durations_08():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert format(staff) == stringtools.normalize(
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

    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [Duration(3, 16)],
        cyclic=True,
        fill=Less,
        in_seconds=False,
        overhang=False,
        )

    r'''
    [
        [Note(c', 8)],
        [Note(d', 8)],
        [Note(e', 8)],
        [Note(f', 8)],
        [Note(g', 8)],
        [Note(a', 8)],
        [Note(b', 8)]
    ]
    '''

    assert len(parts) == 7
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:1])
    assert parts[1] == list(leaves[1:2])
    assert parts[2] == list(leaves[2:3])
    assert parts[3] == list(leaves[3:4])
    assert parts[4] == list(leaves[4:5])
    assert parts[5] == list(leaves[5:6])
    assert parts[6] == list(leaves[6:7])


def test_selectiontools_Selection_partition_by_durations_09():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = Tempo(Duration(1, 4), 60)
    attach(tempo, staff, scope=Staff)

    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [0.75],
        cyclic=False,
        fill=Less,
        in_seconds=True,
        overhang=False,
        )

    "[[Note(c', 8)]]"

    assert len(parts) == 1
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:1])


def test_selectiontools_Selection_partition_by_durations_10():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    parts = leaves.partition_by_durations(
        [Duration(3, 16)],
        cyclic=False,
        fill=Less,
        in_seconds=False,
        overhang=False,
        )

    "[[Note(c', 8)]]"

    assert len(parts) == 1
    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)
    assert parts[0] == list(leaves[:1])