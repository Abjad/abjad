# -*- coding: utf-8 -*-
import abjad


def test_spannertools_HiddenStaffSpanner___init___01():
    r'''Initialize empty hidden staff spanner.
    '''

    spanner = abjad.HiddenStaffSpanner()
    assert isinstance(spanner, abjad.HiddenStaffSpanner)


def test_spannertools_HiddenStaffSpanner___init___02():
    r'''Hide staff around one measure.
    '''

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = abjad.select(staff).by_leaf()

    assert format(staff) == abjad.String.normalize(
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

    spanner = abjad.HiddenStaffSpanner()
    abjad.attach(spanner, leaves[2:4])

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_HiddenStaffSpanner___init___03():
    r'''Hide staff around one leaf.
    '''

    note = abjad.Note(0, (1, 8))
    spanner = abjad.HiddenStaffSpanner()
    abjad.attach(spanner, note)

    assert format(note) == abjad.String.normalize(
        r'''
        \stopStaff
        c'8
        \startStaff
        '''
        )

    assert abjad.inspect(note).is_well_formed()
