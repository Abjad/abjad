from abjad import *


def test_Chord___setitem___01( ):
   '''Set chord item with pitch number.
   '''

   chord = Chord([3, 13, 17], (1, 4))
   chord[1] = 14

   assert chord.format == "<ef' d'' f''>4"
