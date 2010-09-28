from abjad import *


def test_Spanner___contains___01( ):

   note = Note(0, (1, 4))
   spanner = spannertools.Spanner([Note(0, (1, 4))])

   assert not note in spanner
