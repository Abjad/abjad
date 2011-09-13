from abjad import *


def test_contexttools_get_effective_staff_01():
    '''Staff changes work on the first note of a staff.'''

    piano = scoretools.PianoStaff(Staff("c'8 d'8 e'8 f'8") * 2)
    piano.is_parallel = True
    piano[0].name = 'RH'
    piano[1].name = 'LH'
    contexttools.StaffChangeMark(piano[1])(piano[0][0])

    r'''
    \new PianoStaff <<
        \context Staff = "RH" {
            \change Staff = LH
            c'8
            d'8
            e'8
            f'8
        }
        \context Staff = "LH" {
            c'8
            d'8
            e'8
            f'8
        }
    >>
    '''

    assert componenttools.is_well_formed_component(piano)
    assert contexttools.get_effective_staff(piano[0][0]) is piano[1]
    assert contexttools.get_effective_staff(piano[0][1]) is piano[1]
    assert contexttools.get_effective_staff(piano[0][2]) is piano[1]
    assert contexttools.get_effective_staff(piano[0][3]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][0]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][1]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][2]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][3]) is piano[1]

    assert piano.format == '\\new PianoStaff <<\n\t\\context Staff = "RH" {\n\t\t\\change Staff = LH\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n\t\\context Staff = "LH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n>>'


def test_contexttools_get_effective_staff_02():
    '''Staff changes work on middle notes of a staff.'''

    piano = scoretools.PianoStaff(Staff("c'8 d'8 e'8 f'8") * 2)
    piano.is_parallel = True
    piano[0].name = 'RH'
    piano[1].name = 'LH'
    contexttools.StaffChangeMark(piano[1])(piano[0][0])
    contexttools.StaffChangeMark(piano[0])(piano[0][2])

    r'''
    \new PianoStaff <<
        \context Staff = "RH" {
            \change Staff = LH
            c'8
            d'8
            \change Staff = RH
            e'8
            f'8
        }
        \context Staff = "LH" {
            c'8
            d'8
            e'8
            f'8
        }
    >>
    '''

    assert componenttools.is_well_formed_component(piano)
    assert contexttools.get_effective_staff(piano[0][0]) is piano[1]
    assert contexttools.get_effective_staff(piano[0][1]) is piano[1]
    assert contexttools.get_effective_staff(piano[0][2]) is piano[0]
    assert contexttools.get_effective_staff(piano[0][3]) is piano[0]
    assert contexttools.get_effective_staff(piano[1][0]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][1]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][2]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][3]) is piano[1]

    assert piano.format == '\\new PianoStaff <<\n\t\\context Staff = "RH" {\n\t\t\\change Staff = LH\n\t\tc\'8\n\t\td\'8\n\t\t\\change Staff = RH\n\t\te\'8\n\t\tf\'8\n\t}\n\t\\context Staff = "LH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n>>'


def test_contexttools_get_effective_staff_03():
    '''Staff changes work on the last note of a staff.'''

    piano = scoretools.PianoStaff(Staff("c'8 d'8 e'8 f'8") * 2)
    piano.is_parallel = True
    piano[0].name = 'RH'
    piano[1].name = 'LH'
    contexttools.StaffChangeMark(piano[1])(piano[0][-1])

    r'''
    \new PianoStaff <<
        \context Staff = "RH" {
            c'8
            d'8
            e'8
            \change Staff = LH
            f'8
        }
        \context Staff = "LH" {
            c'8
            d'8
            e'8
            f'8
        }
    >>
    '''

    assert componenttools.is_well_formed_component(piano)
    assert piano.format == '\\new PianoStaff <<\n\t\\context Staff = "RH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\t\\change Staff = LH\n\t\tf\'8\n\t}\n\t\\context Staff = "LH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n>>'


def test_contexttools_get_effective_staff_04():
    '''Redudant staff changes are allowed.'''

    piano = scoretools.PianoStaff(Staff("c'8 d'8 e'8 f'8") * 2)
    piano.is_parallel = True
    piano[0].name = 'RH'
    piano[1].name = 'LH'
    contexttools.StaffChangeMark(piano[1])(piano[0][0])
    contexttools.StaffChangeMark(piano[1])(piano[0][1])

    r'''
    \new PianoStaff <<
        \context Staff = "RH" {
            \change Staff = LH
            c'8
            \change Staff = LH
            d'8
            e'8
            f'8
        }
        \context Staff = "LH" {
            c'8
            d'8
            e'8
            f'8
        }
    >>
    '''

    assert componenttools.is_well_formed_component(piano)
    assert contexttools.get_effective_staff(piano[0][0]) is piano[1]
    assert contexttools.get_effective_staff(piano[0][1]) is piano[1]
    assert contexttools.get_effective_staff(piano[0][2]) is piano[1]
    assert contexttools.get_effective_staff(piano[0][3]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][0]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][1]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][2]) is piano[1]
    assert contexttools.get_effective_staff(piano[1][3]) is piano[1]

    assert piano.format == '\\new PianoStaff <<\n\t\\context Staff = "RH" {\n\t\t\\change Staff = LH\n\t\tc\'8\n\t\t\\change Staff = LH\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n\t\\context Staff = "LH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n>>'
