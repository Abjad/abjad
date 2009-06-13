from abjad.measure.measure import _Measure
from abjad.tools.layout._line_break_every import _line_break_every


def line_break_every_prolated(expr, line_duration, klass = _Measure):
   r'''Iterate *klass* instances in *expr* and accumulate prolated duration.
   Add line break after every total less than or equal to *line_duration*.

   ::

      t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
      pitchtools.diatonicize(t)

      \new Staff {
                      \time 2/8
                      c'8
                      d'8
                      \time 2/8
                      e'8
                      f'8
                      \time 2/8
                      g'8
                      a'8
                      \time 2/8
                      b'8
                      c''8
      }

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
   '''

   _line_break_every(expr, line_duration, klass, 'prolated')
