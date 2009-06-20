from abjad import *
import py.test


def test_chordtools_get_notehead_01( ):
   '''Return reference to notehead in chord with pitch equal to pitch.'''

   chord = Chord([0, 2, 11], Rational(1, 4))

   notehead = chordtools.get_notehead(chord, 0)
   assert notehead.pitch.number == 0

   notehead = chordtools.get_notehead(chord, 2)
   assert notehead.pitch.number == 2

   notehead = chordtools.get_notehead(chord, 11)
   assert notehead.pitch.number == 11


def test_chordtools_get_notehead_02( ):
   '''Raise MissingNoteHeadError and ExtraNoteHeadError as required.'''

   chord = Chord([0, 2, 2], Rational(1, 4))

   assert py.test.raises(
      MissingNoteHeadError, 'chordtools.get_notehead(chord, 9)')
   
   assert py.test.raises(
      ExtraNoteHeadError, 'chordtools.get_notehead(chord, 2)')
