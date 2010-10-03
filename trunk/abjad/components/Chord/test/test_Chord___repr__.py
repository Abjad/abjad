from abjad import *


def test_Chord___repr___01( ):
   '''Chord repr is evaluable.
   '''

   chord = Chord([3, 13, 17], (1, 4))
   new_chord = eval(repr(chord))

   assert new_chord == chord
