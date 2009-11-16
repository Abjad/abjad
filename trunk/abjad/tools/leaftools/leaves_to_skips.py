from abjad.skip import Skip
from abjad.tools import iterate


def leaves_to_skips(expr):
   r'''.. versionadded:: 1.1.1

   Iterate `expr` and change notes, rests and chords into skips.

   Pass `expr` an an Abjad component or a Python list of Abjad
   components. 

   Return ``None``. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.scale(2)) * 2)
      abjad> leaftools.leaves_to_skips(staff[0])

   ::
   
      abjad> print staff.format
      \new Staff {
            \time 2/8
            s8
            s8
            \time 2/8
            c'8
            d'8
      }
   '''

   for leaf in iterate.leaves_forward_in(expr):
      Skip(leaf)
