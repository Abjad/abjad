from abjad.core import _Abjad
from abjad.core import _Immutable


class FixedStaffPositioning(_Abjad, _Immutable):
   r'''Indicator object to model fixed-systems layout across an entire score.
   Instantiate a :class:`~abjad.layouttools.systemsindicator.FixedStaffPositioning`
   object with numeric indication of fixed distances between systems.
   Then pass to :func:`~abjad.tools.layouttools.apply_fixed_staff_positioning.apply_fixed_staff_positioning`. ::

      abjad> t = Staff(RigidMeasure((2, 8), notetools.make_repeated_notes(2)) * 4)
      abjad> pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
      abjad> layouttools.set_line_breaks_cyclically_by_line_duration_ge(t, Rational(4, 8))      

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
      abjad> layouttools.apply_fixed_staff_positioning(t, positioning)

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
      #self.system_y_offsets = system_y_offsets
      #self.staff_alignment_offsets = staff_alignment_offsets
      object.__setattr__(self, '_system_y_offsets', system_y_offsets)
      object.__setattr__(self, '_staff_alignment_offsets', staff_alignment_offsets)

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, FixedStaffPositioning):
         if self.system_y_offsets == expr.system_y_offsets:
            if self.staff_alignment_offsets == expr.staff_alignment_offsets:
               return True
      return False

   def __ne__(self, expr):
      return not self == expr

   ## PUBLIC ATTRIBUTES ##

   @property
   def staff_alignment_offsets(self):
      return self._staff_alignment_offsets

   @property
   def system_y_offsets(self):
      return self._system_y_offsets
