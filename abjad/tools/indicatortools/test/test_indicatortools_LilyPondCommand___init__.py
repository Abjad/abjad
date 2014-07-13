# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_LilyPondCommand___init___01():
    r'''Initializes LilyPond command from command name.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff.select_leaves())
    command = indicatortools.LilyPondCommand(r'slurDotted')
    attach(command, staff[0])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_indicatortools_LilyPondCommand___init___02():
    r'''Set LilyPond command from command name.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff.select_leaves())
    command = indicatortools.LilyPondCommand(r'slurUp')
    attach(command, staff[0])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \slurUp
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_indicatortools_LilyPondCommand___init___03():
    r'''Initializes LilyPond command from string and format slot.
    '''

    command = indicatortools.LilyPondCommand('break', 'closing')
    assert isinstance(command, indicatortools.LilyPondCommand)