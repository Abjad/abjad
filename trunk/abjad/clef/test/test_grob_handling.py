from abjad import *


def test_clef_grob_format_01( ):
   '''The Abjad _Clef formats the LilyPond Clef grob
      set automatically to the LilyPond Staff context.'''
   t = Note(0, (1, 4))
   t.clef.color = 'red'
   assert t.format == "\\once \\override Staff.Clef #'color = #red\nc'4"
   '''
   \once \override Staff.Clef #'color = #red
   c'4
   '''
