from abjad import *
from abjad.components._Component import _Component


def test_Annotation___call___01( ):

   staff = Staff(macros.scale(4))
   annotation = marktools.Annotation('foo')(staff[0])

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert annotation.target_context is _Component
   assert annotation.effective_context is staff[0]
