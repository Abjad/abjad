# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_ContiguousSelection_partition_by_durations_not_less_than_01():

    staff = Staff()
    staff.extend("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    staff.extend("abj: | 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert systemtools.TestManager.compare(
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
    parts = leaves.partition_by_durations_not_less_than(
        [Duration(3, 16), Duration(1, 16)], 
        cyclic=True, 
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
    assert parts[0] == list(staff.select_leaves()[:2])
    assert parts[1] == list(staff.select_leaves()[2:3])
    assert parts[2] == list(staff.select_leaves()[3:5])
    assert parts[3] == list(staff.select_leaves()[5:6])
    assert parts[4] == list(staff.select_leaves()[6:])
