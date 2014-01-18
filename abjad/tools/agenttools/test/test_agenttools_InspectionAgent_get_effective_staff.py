# -*- encoding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_get_effective_staff_01():
    r'''Staff changes work on the first note of a staff.
    '''

    staves = 2 * Staff("c'8 d'8 e'8 f'8")
    piano_staff = StaffGroup(staves)
    piano_staff.context_name = 'PianoStaff'
    piano_staff.is_simultaneous = True
    piano_staff[0].name = 'RH'
    piano_staff[1].name = 'LH'
    staff_change = indicatortools.StaffChange(piano_staff[1])
    attach(staff_change, piano_staff[0][0])

    assert systemtools.TestManager.compare(
        piano_staff,
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
        )

    assert inspect_(piano_staff).is_well_formed()
    assert inspect_(piano_staff[0][0]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[0][1]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[0][2]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[0][3]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][0]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][1]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][2]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][3]).get_effective_staff() is piano_staff[1]


def test_agenttools_InspectionAgent_get_effective_staff_02():
    r'''Staff changes work on middle notes of a staff.
    '''

    staves = 2 * Staff("c'8 d'8 e'8 f'8")
    piano_staff = StaffGroup(staves)
    piano_staff.context_name = 'PianoStaff'
    piano_staff.is_simultaneous = True
    piano_staff[0].name = 'RH'
    piano_staff[1].name = 'LH'
    staff_change = indicatortools.StaffChange(piano_staff[1])
    attach(staff_change, piano_staff[0][0])
    staff_change = indicatortools.StaffChange(piano_staff[0])
    attach(staff_change, piano_staff[0][2])

    assert systemtools.TestManager.compare(
        piano_staff,
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
        )

    assert inspect_(piano_staff).is_well_formed()
    assert inspect_(piano_staff[0][0]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[0][1]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[0][2]).get_effective_staff() is piano_staff[0]
    assert inspect_(piano_staff[0][3]).get_effective_staff() is piano_staff[0]
    assert inspect_(piano_staff[1][0]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][1]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][2]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][3]).get_effective_staff() is piano_staff[1]


def test_agenttools_InspectionAgent_get_effective_staff_03():
    r'''Staff changes work on the last note of a staff.
    '''

    staves = 2 * Staff("c'8 d'8 e'8 f'8")
    piano_staff = StaffGroup(staves)
    piano_staff.context_name = 'PianoStaff'
    piano_staff.is_simultaneous = True
    piano_staff[0].name = 'RH'
    piano_staff[1].name = 'LH'
    staff_change = indicatortools.StaffChange(piano_staff[1])
    attach(staff_change, piano_staff[0][-1])

    assert systemtools.TestManager.compare(
        piano_staff,
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
        )

    assert inspect_(piano_staff).is_well_formed()


def test_agenttools_InspectionAgent_get_effective_staff_04():
    r'''Redudant staff changes are allowed.
    '''

    staves = 2 * Staff("c'8 d'8 e'8 f'8")
    piano_staff = StaffGroup(staves)
    piano_staff.context_name = 'PianoStaff'
    piano_staff.is_simultaneous = True
    piano_staff[0].name = 'RH'
    piano_staff[1].name = 'LH'
    staff_change = indicatortools.StaffChange(piano_staff[1])
    attach(staff_change, piano_staff[0][0])
    staff_change = indicatortools.StaffChange(piano_staff[1])
    attach(staff_change, piano_staff[0][1])

    assert systemtools.TestManager.compare(
        piano_staff,
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
        )

    assert inspect_(piano_staff).is_well_formed()
    assert inspect_(piano_staff[0][0]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[0][1]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[0][2]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[0][3]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][0]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][1]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][2]).get_effective_staff() is piano_staff[1]
    assert inspect_(piano_staff[1][3]).get_effective_staff() is piano_staff[1]
