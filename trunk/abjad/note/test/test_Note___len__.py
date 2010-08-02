from abjad import *


def test_Note___len___01( ):

   t = Note(0, (1, 4))
   assert len(t) == 1


def test_Note___len___02( ):

   t = Note(None, (1, 4))
   assert len(t) == 0
