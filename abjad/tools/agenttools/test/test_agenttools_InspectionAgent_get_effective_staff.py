# -*- coding: utf-8 -*-
import abjad


def test_agenttools_InspectionAgent_get_effective_staff_01():
    r'''Staff changes work on the first note of a staff.
    '''

    staves = 2 * abjad.Staff("c'8 d'8 e'8 f'8")
    staff_group = abjad.StaffGroup(staves)
    staff_group.context_name = 'PianoStaff'
    staff_group.is_simultaneous = True
    staff_group[0].name = 'RH'
    staff_group[1].name = 'LH'
    staff_change = abjad.StaffChange(staff_group[1])
    abjad.attach(staff_change, staff_group[0][0])

    assert format(staff_group) == abjad.String.normalize(
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

    assert abjad.inspect(staff_group).is_well_formed()
    assert abjad.inspect(staff_group[0][0]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[0][1]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[0][2]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[0][3]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][0]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][1]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][2]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][3]).get_effective_staff() is staff_group[1]


def test_agenttools_InspectionAgent_get_effective_staff_02():
    r'''Staff changes work on middle notes of a staff.
    '''

    staves = 2 * abjad.Staff("c'8 d'8 e'8 f'8")
    staff_group = abjad.StaffGroup(staves)
    staff_group.context_name = 'PianoStaff'
    staff_group.is_simultaneous = True
    staff_group[0].name = 'RH'
    staff_group[1].name = 'LH'
    staff_change = abjad.StaffChange(staff_group[1])
    abjad.attach(staff_change, staff_group[0][0])
    staff_change = abjad.StaffChange(staff_group[0])
    abjad.attach(staff_change, staff_group[0][2])

    assert format(staff_group) == abjad.String.normalize(
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

    assert abjad.inspect(staff_group).is_well_formed()
    assert abjad.inspect(staff_group[0][0]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[0][1]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[0][2]).get_effective_staff() is staff_group[0]
    assert abjad.inspect(staff_group[0][3]).get_effective_staff() is staff_group[0]
    assert abjad.inspect(staff_group[1][0]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][1]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][2]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][3]).get_effective_staff() is staff_group[1]


def test_agenttools_InspectionAgent_get_effective_staff_03():
    r'''Staff changes work on the last note of a staff.
    '''

    staves = 2 * abjad.Staff("c'8 d'8 e'8 f'8")
    staff_group = abjad.StaffGroup(staves)
    staff_group.context_name = 'PianoStaff'
    staff_group.is_simultaneous = True
    staff_group[0].name = 'RH'
    staff_group[1].name = 'LH'
    staff_change = abjad.StaffChange(staff_group[1])
    abjad.attach(staff_change, staff_group[0][-1])

    assert format(staff_group) == abjad.String.normalize(
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

    assert abjad.inspect(staff_group).is_well_formed()


def test_agenttools_InspectionAgent_get_effective_staff_04():
    r'''Redudant staff changes are allowed.
    '''

    staves = 2 * abjad.Staff("c'8 d'8 e'8 f'8")
    staff_group = abjad.StaffGroup(staves)
    staff_group.context_name = 'PianoStaff'
    staff_group.is_simultaneous = True
    staff_group[0].name = 'RH'
    staff_group[1].name = 'LH'
    staff_change = abjad.StaffChange(staff_group[1])
    abjad.attach(staff_change, staff_group[0][0])
    staff_change = abjad.StaffChange(staff_group[1])
    abjad.attach(staff_change, staff_group[0][1])

    assert format(staff_group) == abjad.String.normalize(
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

    assert abjad.inspect(staff_group).is_well_formed()
    assert abjad.inspect(staff_group[0][0]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[0][1]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[0][2]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[0][3]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][0]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][1]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][2]).get_effective_staff() is staff_group[1]
    assert abjad.inspect(staff_group[1][3]).get_effective_staff() is staff_group[1]
