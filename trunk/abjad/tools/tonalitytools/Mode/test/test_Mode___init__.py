from abjad import *
from abjad.tools import tonalitytools


def test_Mode___init___01( ):
    '''Init with mode name string.'''

    mode = tonalitytools.Mode('dorian')
    assert mode.mode_name_string == 'dorian'


def test_Mode___init___02( ):
    '''Init with other mode instance.'''

    mode = tonalitytools.Mode('dorian')
    new = tonalitytools.Mode(mode)

    assert new.mode_name_string == 'dorian'
