from abjad import *


def test_Articulation_direction_string_01( ):

   t = Note(0, (1, 4))
   a = marktools.Articulation('staccato')(t)

   assert a.direction_string == '-'

   a.direction_string = '^'
   
   assert a.direction_string == '^'
