# -*- encoding: utf-8 -*-
from abjad import *


def test_Component_get_effective_staff_01():
    r'''Staff changes work on the first note of a staff.
    '''

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

    assert select(piano).is_well_formed()
    assert piano[0][0].get_effective_staff() is piano[1]
    assert piano[0][1].get_effective_staff() is piano[1]
    assert piano[0][2].get_effective_staff() is piano[1]
    assert piano[0][3].get_effective_staff() is piano[1]
    assert piano[1][0].get_effective_staff() is piano[1]
    assert piano[1][1].get_effective_staff() is piano[1]
    assert piano[1][2].get_effective_staff() is piano[1]
    assert piano[1][3].get_effective_staff() is piano[1]

    assert testtools.compare(
        piano.lilypond_format,
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


def test_Component_get_effective_staff_02():
    r'''Staff changes work on middle notes of a staff.
    '''

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

    assert select(piano).is_well_formed()
    assert piano[0][0].get_effective_staff() is piano[1]
    assert piano[0][1].get_effective_staff() is piano[1]
    assert piano[0][2].get_effective_staff() is piano[0]
    assert piano[0][3].get_effective_staff() is piano[0]
    assert piano[1][0].get_effective_staff() is piano[1]
    assert piano[1][1].get_effective_staff() is piano[1]
    assert piano[1][2].get_effective_staff() is piano[1]
    assert piano[1][3].get_effective_staff() is piano[1]

    assert testtools.compare(
        piano.lilypond_format,
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


def test_Component_get_effective_staff_03():
    r'''Staff changes work on the last note of a staff.
    '''

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

    assert select(piano).is_well_formed()
    assert testtools.compare(
        piano.lilypond_format,
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


def test_Component_get_effective_staff_04():
    r'''Redudant staff changes are allowed.
    '''

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

    assert select(piano).is_well_formed()
    assert piano[0][0].get_effective_staff() is piano[1]
    assert piano[0][1].get_effective_staff() is piano[1]
    assert piano[0][2].get_effective_staff() is piano[1]
    assert piano[0][3].get_effective_staff() is piano[1]
    assert piano[1][0].get_effective_staff() is piano[1]
    assert piano[1][1].get_effective_staff() is piano[1]
    assert piano[1][2].get_effective_staff() is piano[1]
    assert piano[1][3].get_effective_staff() is piano[1]

    assert testtools.compare(
        piano.lilypond_format,
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
