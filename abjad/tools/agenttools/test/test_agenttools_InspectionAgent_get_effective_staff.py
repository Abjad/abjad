# -*- encoding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_get_effective_staff_01():
    r'''Staff changes work on the first note of a staff.
    '''

    piano = scoretools.PianoStaff(2 * Staff("c'8 d'8 e'8 f'8"))
    piano.is_simultaneous = True
    piano[0].name = 'RH'
    piano[1].name = 'LH'
    staff_change = indicatortools.StaffChange(piano[1])
    attach(staff_change, piano[0][0])

    assert systemtools.TestManager.compare(
        piano,
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

    assert inspect(piano).is_well_formed()
    assert inspect(piano[0][0]).get_effective_staff() is piano[1]
    assert inspect(piano[0][1]).get_effective_staff() is piano[1]
    assert inspect(piano[0][2]).get_effective_staff() is piano[1]
    assert inspect(piano[0][3]).get_effective_staff() is piano[1]
    assert inspect(piano[1][0]).get_effective_staff() is piano[1]
    assert inspect(piano[1][1]).get_effective_staff() is piano[1]
    assert inspect(piano[1][2]).get_effective_staff() is piano[1]
    assert inspect(piano[1][3]).get_effective_staff() is piano[1]


def test_agenttools_InspectionAgent_get_effective_staff_02():
    r'''Staff changes work on middle notes of a staff.
    '''

    piano = scoretools.PianoStaff(2 * Staff("c'8 d'8 e'8 f'8"))
    piano.is_simultaneous = True
    piano[0].name = 'RH'
    piano[1].name = 'LH'
    staff_change = indicatortools.StaffChange(piano[1])
    attach(staff_change, piano[0][0])
    staff_change = indicatortools.StaffChange(piano[0])
    attach(staff_change, piano[0][2])

    assert systemtools.TestManager.compare(
        piano,
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

    assert inspect(piano).is_well_formed()
    assert inspect(piano[0][0]).get_effective_staff() is piano[1]
    assert inspect(piano[0][1]).get_effective_staff() is piano[1]
    assert inspect(piano[0][2]).get_effective_staff() is piano[0]
    assert inspect(piano[0][3]).get_effective_staff() is piano[0]
    assert inspect(piano[1][0]).get_effective_staff() is piano[1]
    assert inspect(piano[1][1]).get_effective_staff() is piano[1]
    assert inspect(piano[1][2]).get_effective_staff() is piano[1]
    assert inspect(piano[1][3]).get_effective_staff() is piano[1]


def test_agenttools_InspectionAgent_get_effective_staff_03():
    r'''Staff changes work on the last note of a staff.
    '''

    piano = scoretools.PianoStaff(2 * Staff("c'8 d'8 e'8 f'8"))
    piano.is_simultaneous = True
    piano[0].name = 'RH'
    piano[1].name = 'LH'
    staff_change = indicatortools.StaffChange(piano[1])
    attach(staff_change, piano[0][-1])

    assert systemtools.TestManager.compare(
        piano,
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

    assert inspect(piano).is_well_formed()


def test_agenttools_InspectionAgent_get_effective_staff_04():
    r'''Redudant staff changes are allowed.
    '''

    piano = scoretools.PianoStaff(2 * Staff("c'8 d'8 e'8 f'8"))
    piano.is_simultaneous = True
    piano[0].name = 'RH'
    piano[1].name = 'LH'
    staff_change = indicatortools.StaffChange(piano[1])
    attach(staff_change, piano[0][0])
    staff_change = indicatortools.StaffChange(piano[1])
    attach(staff_change, piano[0][1])

    assert systemtools.TestManager.compare(
        piano,
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

    assert inspect(piano).is_well_formed()
    assert inspect(piano[0][0]).get_effective_staff() is piano[1]
    assert inspect(piano[0][1]).get_effective_staff() is piano[1]
    assert inspect(piano[0][2]).get_effective_staff() is piano[1]
    assert inspect(piano[0][3]).get_effective_staff() is piano[1]
    assert inspect(piano[1][0]).get_effective_staff() is piano[1]
    assert inspect(piano[1][1]).get_effective_staff() is piano[1]
    assert inspect(piano[1][2]).get_effective_staff() is piano[1]
    assert inspect(piano[1][3]).get_effective_staff() is piano[1]
