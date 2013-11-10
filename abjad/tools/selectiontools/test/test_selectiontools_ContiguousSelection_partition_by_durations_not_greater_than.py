# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_ContiguousSelection_partition_by_durations_not_greater_than_01():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = Tempo(Duration(1, 4), 60, _target_context=Staff)
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
    parts = leaves.partition_by_durations_not_greater_than(
        [0.75],
        cyclic=True,
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
    assert parts[0] == list(staff.select_leaves()[:1])
    assert parts[1] == list(staff.select_leaves()[1:2])
    assert parts[2] == list(staff.select_leaves()[2:3])
    assert parts[3] == list(staff.select_leaves()[3:4])
    assert parts[4] == list(staff.select_leaves()[4:5])
    assert parts[5] == list(staff.select_leaves()[5:6])
    assert parts[6] == list(staff.select_leaves()[6:7])


def test_selectiontools_ContiguousSelection_partition_by_durations_not_greater_than_02():

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
    parts = leaves.partition_by_durations_not_greater_than(
        [Duration(3, 16)],
        cyclic=True,
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
    assert parts[0] == list(staff.select_leaves()[:1])
    assert parts[1] == list(staff.select_leaves()[1:2])
    assert parts[2] == list(staff.select_leaves()[2:3])
    assert parts[3] == list(staff.select_leaves()[3:4])
    assert parts[4] == list(staff.select_leaves()[4:5])
    assert parts[5] == list(staff.select_leaves()[5:6])
    assert parts[6] == list(staff.select_leaves()[6:7])


def test_selectiontools_ContiguousSelection_partition_by_durations_not_greater_than_03():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    tempo = Tempo(Duration(1, 4), 60, _target_context=Staff)
    attach(tempo, staff)

    leaves = staff.select_leaves()
    parts = leaves.partition_by_durations_not_greater_than(
        [0.75],
        cyclic=False,
        in_seconds=True,
        overhang=False,
        )

    "[[Note(c', 8)]]"

    assert len(parts) == 1
    assert parts[0] == list(staff.select_leaves()[:1])


def test_selectiontools_ContiguousSelection_partition_by_durations_not_greater_than_04():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
        "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |")
    leaves = staff.select_leaves()
    parts = leaves.partition_by_durations_not_greater_than(
        [Duration(3, 16)],
        cyclic=False,
        in_seconds=False,
        overhang=False,
        )

    "[[Note(c', 8)]]"

    assert len(parts) == 1
    assert parts[0] == list(staff.select_leaves()[:1])
