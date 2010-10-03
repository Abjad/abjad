from abjad import *
from abjad.tools.skiptools import Skip


def test_Skip___repr___01( ):
   '''Skip repr is evaluable.
   '''

   skip = Skip('s8.')
   new_skip = eval(repr(skip))

   assert new_skip == skip
