from abjad.core import _Immutable
from abjad.core import _StrictComparator
from abjad.tools.layouttools.FixedStaffPositioning import FixedStaffPositioning
from abjad.tools.layouttools.StaffAlignmentDistances import StaffAlignmentDistances
from abjad.tools.layouttools.SystemYOffsets import SystemYOffsets
from fractions import Fraction


class LayoutSchema(_StrictComparator, _Immutable):
   r'''Indicator to line-break an arbitrary score and then
   position staves and systems regularly throughout.

   Short-cut to avoid instanting SystemYOffsets and
   StaffAlignmentOffsets by hand.
   '''

   def __init__(self, line_break_duration, system_y_offsets_tuple,
      staff_alignment_offsets_tuple, in_seconds = False):

#      self.line_break_duration = Fraction(line_break_duration)
#      self.system_y_offsets = SystemYOffsets(*system_y_offsets_tuple)
#      self.staff_alignment_offsets = StaffAlignmentDistances(*staff_alignment_offsets_tuple)
#      self.fixed_staff_positioning = FixedStaffPositioning(
#         self.system_y_offsets, self.staff_alignment_offsets)
#      self.in_seconds = False

      object.__setattr__(self, 'line_break_duration', Fraction(line_break_duration))
      object.__setattr__(self, 'system_y_offsets', SystemYOffsets(*system_y_offsets_tuple))
      object.__setattr__(self, 'staff_alignment_offsets', 
         StaffAlignmentDistances(*staff_alignment_offsets_tuple))
      object.__setattr__(self, 'fixed_staff_positioning',
         FixedStaffPositioning(self.system_y_offsets, self.staff_alignment_offsets))
      object.__setattr__(self, 'in_seconds', in_seconds)

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, LayoutSchema):
         if self.line_break_duration == expr.line_break_duration:
            if self.system_y_offsets == expr.system_y_offsets:
               if self.staff_alignment_offsets == expr.staff_alignment_offsets:
                  return True
      return False

   def __ne__(self, expr):
      return not self == expr

   ## PUBLIC ATTRIBUTES ##

#   @apply
#   def in_seconds( ):
#      '''Write docs.
#
#      .. todo:: write tests.'''
#      def fget(self):
#         return self._in_seconds
#      def fset(self, expr):
#         if not isinstance(expr, bool):
#            raise TypeError('must be true or false.')
#         self._in_seconds = expr
#      return property(**locals( ))
