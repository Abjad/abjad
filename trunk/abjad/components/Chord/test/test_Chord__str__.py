from abjad import *


def test_Chord__str___01( ):

   chord = Chord([3, 13, 17], (1, 4))

   assert str(chord) == "<ef' cs'' f''>4"
