from abjad import *


def test_pitches_make_flat_01( ):
   '''The pitches.make_flat( ) helper renotates an individual pitch.'''
   t = Pitch('cs', 4)
   pitches.make_flat(t)
   assert t == Pitch('df', 4)


def test_pitches_make_flat_02( ):
   '''The pitches.make_flat( ) helper renotates the pitch of one note.'''
   t = Note(('cs', 4), 4)
   pitches.make_flat(t)
   assert t.pitch == Pitch('df', 4)


def test_pitches_make_flat_03( ):
   '''The pitches.make_flat( ) helper renotates the pitches of all notes in a chord.'''
   t = Chord([('cs', 4), ('f', 4), ('as', 4)], (1, 4))
   pitches.make_flat(t)
   assert t.pitches == (Pitch('df', 4), Pitch('f', 4), Pitch('bf', 4)) 


def test_pitches_make_flat_04( ):
   '''The pitches.make_flat( ) helper renotates all pitches in any arbirary expression.'''
   t = Staff([Note(n, (1, 8)) for n in range(12, 0, -1)])
   pitches.make_flat(t)

   r'''
   \new Staff {
           c''8
           b'8
           bf'8
           a'8
           af'8
           g'8
           gf'8
           f'8
           e'8
           ef'8
           d'8
           df'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc''8\n\tb'8\n\tbf'8\n\ta'8\n\taf'8\n\tg'8\n\tgf'8\n\tf'8\n\te'8\n\tef'8\n\td'8\n\tdf'8\n}"
