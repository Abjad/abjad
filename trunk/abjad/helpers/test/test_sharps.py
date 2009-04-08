from abjad import *


def test_sharps_01( ):
   '''The sharps( ) helper renotates an individual pitch.'''
   t = Pitch('df', 4)
   sharps(t)
   assert t == Pitch('cs', 4)


def test_sharps_02( ):
   '''The sharps( ) helper renotates the pitch of one note.'''
   t = Note(('df', 4), 4)
   sharps(t)
   assert t.pitch == Pitch('cs', 4)


def test_sharps_03( ):
   '''The sharps( ) helper renotates the pitches of all notes in a chord.'''
   t = Chord([('df', 4), ('f', 4), ('af', 4)], (1, 4))
   sharps(t)
   assert t.pitches == (Pitch('cs', 4), Pitch('f', 4), Pitch('gs', 4)) 


def test_sharps_04( ):
   '''The sharps( ) helper renotates all pitches in any arbirary expression.'''
   t = Staff(run(12))
   pitches.chromaticize(t)
   sharps(t)

   r'''
   \new Staff {
      c'8
      cs'8
      d'8
      ds'8
      e'8
      f'8
      fs'8
      g'8
      gs'8
      a'8
      as'8
      b'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tds'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\tgs'8\n\ta'8\n\tas'8\n\tb'8\n}"
