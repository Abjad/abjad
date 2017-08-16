import abjad
import pytest


def test_spannertools_StaffLinesSpanner_format_01():
    r'''StaffLinesSpanner with int argument abjad.overrides StaffSymbol's
    line-count property.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    spanner = abjad.StaffLinesSpanner(lines=3)
    abjad.attach(spanner, staff[2:7])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8
            d'8
            \stopStaff
            \once \override Staff.StaffSymbol.line-count = 3
            \startStaff
            e'8
            f'8
            g'8
            a'8
            b'8
            \stopStaff
            \startStaff
            c''8
        }
        '''
        )


def test_spannertools_StaffLinesSpanner_format_02():
    r'''StaffLinesSpanner with list argument abjad.overrides
    StaffSymbol's line-positions property.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    spanner = abjad.StaffLinesSpanner(
        lines=[-5, -4, -3, -2, -1, 0, 1.5, 3, 4.5],
        )
    abjad.attach(spanner, staff[2:7])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8
            d'8
            \stopStaff
            \once \override Staff.StaffSymbol.line-positions = #'(-5 -4 -3 -2 -1 0 1.5 3 4.5)
            \startStaff
            e'8
            f'8
            g'8
            a'8
            b'8
            \stopStaff
            \startStaff
            c''8
        }
        '''
        )


def test_spannertools_StaffLinesSpanner_format_03():

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    spanner = abjad.StaffLinesSpanner(lines=[-1.5, 0, 1.5])
    abjad.attach(spanner, staff[1:3])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8
            \stopStaff
            \once \override Staff.StaffSymbol.line-positions = #'(-1.5 0 1.5)
            \startStaff
            d'8
            e'8
            \stopStaff
            \startStaff
            f'8
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )
