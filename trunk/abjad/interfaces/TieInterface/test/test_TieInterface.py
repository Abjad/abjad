from abjad import *


def test_TieInterface_01( ):
   '''Attributes format correcty.
   '''

   t = Note(0, (1, 4))
   t.override.tie.color = 'red'
   assert t.format == "\\once \\override Tie #'color = #red\nc'4"
  

def test_TieInterface_02( ):
   '''Clear deletes assigned attributes.
   '''

   t = Note(0, (1, 4))
   t.override.tie.color = 'red'
   assert t.format == "\\once \\override Tie #'color = #red\nc'4"
   del(t.override.tie)
   assert t.format == "c'4"
