from abjad.core.abjadcore import _Abjad


class FixedSystemsIndicator(_Abjad):
   r'''Indicator object to model fixed-systems layout across an entire score.
   Instantiate a :class:`~abjad.layout.systemsindicator.FixedSystemsIndicator`
   object with numeric indication of fixed distances between systems.
   Then pass to :func:`~abjad.tools.layout.apply_fixed_systems_indicator.apply_fixed_systems_indicator`.

   ::

      t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
      pitchtools.diatonicize(t)
      layout.line_break_every_prolated(t, Rational(4, 8))      

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

      system_indicator = FixedSystemsIndicator((20, ), 1)
      layout.apply_fixed_systems_indicator(t, system_indicator)

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
   '''

   def __init__(self, y_offset_tuple, starting_system = 0):
      '''Set y offset values and starting system number.'''
      self.y_offset_tuple = y_offset_tuple
      self.starting_system = starting_system

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, FixedSystemsIndicator):
         if self.y_offset_tuple == expr.y_offset_tuple:
            if self.starting_system == expr.starting_system:
               return True
      return False

   def __ne__(self, expr):
      return not self == expr

   ## PUBLIC ATTRIBUTES ##

   @apply
   def starting_system( ):
      def fget(self):
         '''Read / write zero-based index of *y_offset_tuple* to apply
         to first system in score.'''
         return self._starting_system
      def fset(self, arg):
         if not isinstance(arg, int):
            raise TypeError
         self._starting_system = arg
      return property(**locals( ))

   @apply
   def y_offset_tuple( ):
      def fget(self):
         '''Read / write tuple of one or more fixed numeric distances
         to lay out between staves within each system.'''
         return self._y_offset_tuplet
      def fset(self, arg):
         if not isinstance(arg, tuple):
            raise TypeError
         self._y_offset_tuplet = arg
      return property(**locals( ))
