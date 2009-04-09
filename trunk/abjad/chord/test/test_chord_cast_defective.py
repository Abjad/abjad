from abjad import *


def test_chordtools_cast_defective_01( ):
   '''Empty chord returns skip.'''
   t = Chord([ ], (1, 4))
   t = chordtools.cast_defective(t)
   assert isinstance(t, Rest)


def test_chordtools_cast_defective_02( ):
   '''Length-1 chord returns note.'''
   t = Chord([0], (1, 4))
   t = chordtools.cast_defective(t)
   assert isinstance(t, Note)


def test_chordtools_cast_defective_03( ):
   '''Chords of length 2 or greater return unaltered.'''
   t = Chord([2, 4, 5], (1, 4))
   t = chordtools.cast_defective(t)
   assert isinstance(t, Chord)
