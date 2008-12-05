from abjad import *


def test_accidental_grob_format_01( ):
   '''_Accidental formats the LilyPond Accidental grob.'''
   t = Note(0, (1, 4))
   t.pitch.accidental.color = 'red'
   assert t.format == "\\once \\override Accidental #'color = #red\nc'4"
   '''
   \once \override Accidental #'color = #red
   c'4
   '''


def test_accidental_grob_format_02( ):
   '''_Accidental clear grob overrides with None.'''
   t = Note(0, (1, 4))
   t.pitch.accidental.color = 'red'
   t.pitch.accidental.color = None
   assert t.format == "c'4"
