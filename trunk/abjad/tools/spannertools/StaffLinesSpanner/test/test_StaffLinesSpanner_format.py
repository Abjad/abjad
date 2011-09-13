from abjad import *
import py.test


def test_StaffLinesSpanner_format_01():
    '''StaffLinesSpanner with int argument overrides StaffSymbol's line-count property.'''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    spanner = spannertools.StaffLinesSpanner(staff[2:7], 3)

    r'''
    \new Staff {
        c'8
        d'8
        \stopStaff
        \override Staff.StaffSymbol #'line-count = #3
        \startStaff
        e'8
        f'8
        g'8
        a'8
        b'8
        \stopStaff
        \revert Staff.StaffSymbol #'line-count
        \startStaff
        c''8
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8\n\td'8\n\t\\stopStaff\n\t\\override Staff.StaffSymbol #'line-count = #3\n\t\\startStaff\n\te'8\n\tf'8\n\tg'8\n\ta'8\n\tb'8\n\t\\stopStaff\n\t\\revert Staff.StaffSymbol #'line-count\n\t\\startStaff\n\tc''8\n}"


def test_StaffLinesSpanner_format_02():
    '''StaffLinesSpanner with list argument overrides StaffSymbol's line-positions property.'''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    spanner = spannertools.StaffLinesSpanner(staff[2:7], [-5, -4, -3, -2, -1, 0, 1.5, 3, 4.5])

    r'''
    \new Staff {
        c'8
        d'8
        \stopStaff
        \override Staff.StaffSymbol #'line-positions = #'(-5 -4 -3 -2 -1 0 1.5 3 4.5)
        \startStaff
        e'8
        f'8
        g'8
        a'8
        b'8
        \stopStaff
        \revert Staff.StaffSymbol #'line-positions
        \startStaff
        c''8
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8\n\td'8\n\t\\stopStaff\n\t\\override Staff.StaffSymbol #'line-positions = #'(-5 -4 -3 -2 -1 0 1.5 3 4.5)\n\t\\startStaff\n\te'8\n\tf'8\n\tg'8\n\ta'8\n\tb'8\n\t\\stopStaff\n\t\\revert Staff.StaffSymbol #'line-positions\n\t\\startStaff\n\tc''8\n}"


def test_StaffLinesSpanner_format_03():
    '''StaffLinesSpanner's lines property can be changed.'''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    spanner = spannertools.StaffLinesSpanner(staff[1:3], 1)

    r'''
    \new Staff {
        c'8
        \stopStaff
        \override Staff.StaffSymbol #'line-count = #1
        \startStaff
        d'8
        e'8
        \stopStaff
        \revert Staff.StaffSymbol #'line-count
        \startStaff
        f'8
        g'8
        a'8
        b'8
        c''8
    }
    '''

    spanner.lines = [-1.5, 0, 1.5]

    r'''
    \new Staff {
        c'8
        \stopStaff
        \override Staff.StaffSymbol #'line-positions = #'(-1.5 0 1.5)
        \startStaff
        d'8
        e'8
        \stopStaff
        \revert Staff.StaffSymbol #'line-positions
        \startStaff
        f'8
        g'8
        a'8
        b'8
        c''8
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8\n\t\\stopStaff\n\t\\override Staff.StaffSymbol #'line-positions = #'(-1.5 0 1.5)\n\t\\startStaff\n\td'8\n\te'8\n\t\\stopStaff\n\t\\revert Staff.StaffSymbol #'line-positions\n\t\\startStaff\n\tf'8\n\tg'8\n\ta'8\n\tb'8\n\tc''8\n}"
