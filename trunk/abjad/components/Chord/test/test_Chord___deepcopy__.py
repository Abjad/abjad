from abjad import *
import copy


def test_Chord___deepcopy___01( ):
   '''Ensure deepcopied note heads attach correctly to chord.
   '''

   chord_1 = Chord("<c' e' g'>4")
   chord_2 = copy.deepcopy(chord_1)

   assert chord_2[0]._client is chord_2
   assert chord_2[1]._client is chord_2
   assert chord_2[2]._client is chord_2
