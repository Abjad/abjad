from abjad import *


def test_Mode___init____01( ):
   '''Init with mode name string.'''

   mode = tonalharmony.Mode('dorian')
   assert mode.mode_name_string == 'dorian'


def test_Mode___init____02( ):
   '''Init with other mode instance.'''

   mode = tonalharmony.Mode('dorian')
   new = tonalharmony.Mode(mode)
   
   assert new.mode_name_string == 'dorian'
