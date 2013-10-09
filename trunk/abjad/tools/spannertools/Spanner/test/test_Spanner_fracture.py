# -*- encoding: utf-8 -*-
from abjad import *


def test_Spanner_fracture_01():
    r'''Fracture container spanner to the right of index 1.
    '''

    staff = Staff(r'''
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        {
            e'8
            f'8
            fs'8
            g'8
        }
        {
            af'8
            a'8
            bf'8
            b'8
        }
        ''')
    beam = spannertools.BeamSpanner(staff[:])
    original, left, right = beam.fracture(1, direction=Right)

    assert len(original.components) == 3
    assert original.components[0] is staff[0]
    assert original.components[1] is staff[1]
    assert original.components[2] is staff[2]
    assert len(original.leaves) == 12

    assert len(left.components) == 2
    assert left.components[0] is staff[0]
    assert left.components[1] is staff[1]
    assert len(left.leaves) == 8

    assert len(right.components) == 1
    assert right.components[0] is staff[2]
    assert len(right.leaves) == 4

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            {
                e'8
                f'8
                fs'8
                g'8 ]
            }
            {
                af'8 [
                a'8
                bf'8
                b'8 ]
            }
        }
        '''
        )

    r'''
    \new Staff {
        {
            c'8 [
            cs'8
            d'8
            ef'8
        }
        {
            e'8
            f'8
            fs'8
            g'8 ]
        }
        {
            af'8 [
            a'8
            bf'8
            b'8 ]
        }
    }
    '''
