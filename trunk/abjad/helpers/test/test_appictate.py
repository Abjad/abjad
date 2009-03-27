from abjad import *
from abjad.tools import construct


def test_appictate_01( ):
   '''Appictation works on tie chains.'''

   t = Voice(construct.notes(0, [(5, 32)] * 4))
   appictate(t)

   r'''\new Voice {
           c'8 ~
           c'32
           cs'8 ~
           cs'32
           d'8 ~
           d'32
           ef'8 ~
           ef'32
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'32\n\tcs'8 ~\n\tcs'32\n\td'8 ~\n\td'32\n\tef'8 ~\n\tef'32\n}"
