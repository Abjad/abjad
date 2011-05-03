from abjad import *


def test_ClefMark___init___01( ):

   clef_1 = contexttools.ClefMark('treble')
   clef_2 = contexttools.ClefMark(clef_1)

   assert clef_1 == clef_2
   assert not clef_1 is clef_2
