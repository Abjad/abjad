from abjad.core import _Immutable
from abjad.core import _StrictComparator


class StaffAlignmentDistances(_StrictComparator, _Immutable):
   '''Class to model distances between staves in a system.
   Specify distances by hand when initializing the class.
   Distances may be even or uneven. ::

      abjad> staves = layouttools.StaffAlignmentDistances(18, 18, 18)

   Pass instances of this class as the second argument to 
   :class:`~abjad.layout.fixed_staff_positioning.FixedStaffPositioning`.
   '''

   def __init__(self, *args):
      if any([x < 0 for x in args]):
         print 'WARNING: use positive values for staff alignment distances.'
      #self.alignment_distances = list(args)
      object.__setattr__(self, 'alignment_distances', list(args))

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, StaffAlignmentDistances):
         if self.alignment_distances == expr.alignment_distances:
            return True
      return False
