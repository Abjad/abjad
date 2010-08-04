from abjad.core import _Abjad


class StaffAlignmentOffsets(_Abjad):
   '''Class to model distances between staves in a system.
   Specify distances by hand when initializing the class.
   Distances may be even or uneven. LilyPond reads distances going
   down the page; distances should therefore be negative. ::

      abjad> staves = StaffAlignmentOffsets(0, -15, -32, -47)

   Pass instances of this class as the second argument to 
   :class:`~abjad.layout.fixed_staff_positioning.FixedStaffPositioning`.
   '''

   def __init__(self, *args):
      if any([0 < x for x in args]):
         print 'WARNING: use nonpositive values for staff alignment offsets.'
      self.alignment_offsets = list(args)

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, StaffAlignmentOffsets):
         if self.alignment_offsets == expr.alignment_offsets:
            return True
      return False
