from abjad import *


def test_parenttools_get_first_01( ):

   t = Staff(construct.scale(4))
   
   assert parenttools.get_first(t[0], Staff) is t
   assert parenttools.get_first(t[0], Score) is None
