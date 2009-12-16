from abjad.core.abjadcore import _Abjad


class FixedStaffPositioning(_Abjad):
   r'''Indicator object to model fixed-systems layout across an entire score.
   Instantiate a :class:`~abjad.layout.systemsindicator.FixedStaffPositioning`
   object with numeric indication of fixed distances between systems.
   Then pass to :func:`~abjad.tools.layout.apply_fixed_staff_positioning.apply_fixed_staff_positioning`. ::

      abjad> t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
      abjad> pitchtools.diatonicize(t)
      abjad> layout.line_break_every_prolated(t, Rational(4, 8))      

      \new Staff {
                      \time 2/8
                      c'8
                      d'8
                      \time 2/8
                      e'8
                      f'8
                      \break
                      \time 2/8
                      g'8
                      a'8
                      \time 2/8
                      b'8
                      c''8
                      \break
      }

      abjad> systems = SystemYOffsets(40, 5)
      abjad> staves = StaffAlignmentOffsets(0, 15)
      abjad> positioning = FixedStaffPositioning(systems, staves)
      abjad> layout.apply_fixed_staff_positioning(t, positioning)

      \new Staff {
                      \overrideProperty #"Score.NonMusicalPaperColumn"
                      #'line-break-system-details
                      #'((Y-offset . 20))
                      \time 2/8
                      c'8
                      d'8
                      \time 2/8
                      e'8
                      f'8
                      \break
                      \pageBreak
                      \overrideProperty #"Score.NonMusicalPaperColumn"
                      #'line-break-system-details
                      #'((Y-offset . 20))
                      \time 2/8
                      g'8
                      a'8
                      \time 2/8
                      b'8
                      c''8
                      \break
      }

   .. note:: Staff alignment offsets and staff alignment distances
      are both allowed.
   '''

   def __init__(self, system_y_offsets, staff_alignment_offsets = None):
      '''Set system y offsets and staff alignment offsets.'''
      self.system_y_offsets = system_y_offsets
      self.staff_alignment_offsets = staff_alignment_offsets

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, FixedStaffPositioning):
         if self.system_y_offsets == expr.system_y_offsets:
            if self.staff_alignment_offsets == expr.staff_alignment_offsets:
               return True
      return False

   def __ne__(self, expr):
      return not self == expr

#   ## PUBLIC ATTRIBUTES ##
#
#   @apply
#   def starting_system( ):
#      def fget(self):
#         '''Read / write zero-based index of *system_y_offsets* to apply
#         to first system in score.'''
#         return self._starting_system
#      def fset(self, arg):
#         if not isinstance(arg, int):
#            raise TypeError
#         self._starting_system = arg
#      return property(**locals( ))
#
#   @apply
#   def system_y_offsets( ):
#      def fget(self):
#         '''Read / write tuple of one or more fixed numeric distances
#         to lay out between staves within each system.'''
#         return self._system_y_offsets
#      def fset(self, arg):
#         if not isinstance(arg, tuple):
#            raise TypeError
#         self._system_y_offsets = arg
#      return property(**locals( ))
