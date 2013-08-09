# -*- encoding: utf-8 -*-
from abjad import *


def test_ContiguousLeafSelection_replace_with_01():
    r'''Replace with rests.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    selection = staff.select_leaves()
    selection.replace_with(Rest)

    r'''
    \new Staff {
        r8
        r8
        r8
        r8
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            r8
            r8
            r8
            r8
        }
        '''
        )


def test_ContiguousLeafSelection_replace_with_02():
    r'''Replace with skips.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    selection = staff.select_leaves()
    selection.replace_with(skiptools.Skip)

    r'''
    \new Staff {
        s8
        s8
        s8
        s8
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            s8
            s8
            s8
            s8
        }
        '''
        )
