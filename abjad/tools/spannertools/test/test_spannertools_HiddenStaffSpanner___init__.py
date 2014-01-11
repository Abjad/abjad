# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_HiddenStaffSpanner___init___01():
    r'''Initialize empty hidden staff spanner.
    '''

    spanner = spannertools.HiddenStaffSpanner()
    assert isinstance(spanner, spannertools.HiddenStaffSpanner)


def test_spannertools_HiddenStaffSpanner___init___02():
    r'''Hide staff around one measure.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

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
        }
        '''
        )

    spanner = spannertools.HiddenStaffSpanner()
    attach(spanner, staff[1])

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
                \stopStaff
                e'8
                f'8
                \startStaff
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_spannertools_HiddenStaffSpanner___init___03():
    r'''Hide staff around one leaf.
    '''

    note = Note(0, (1, 8))
    spanner = spannertools.HiddenStaffSpanner()
    attach(spanner, note)

    assert systemtools.TestManager.compare(
        note,
        r'''
        \stopStaff
        c'8
        \startStaff
        '''
        )

    assert inspect(note).is_well_formed()
