from abjad.tools import iterate


def get_written_durations_from_leaves_in_expr(expr):
   '''.. versionadded:: 1.1.2

   Get the written duration of every leaf in `expr`::

      abjad> staff = Staff(FixedDurationTuplet((2, 8), macros.scale(3)) * 2)
      abjad> leaftools.get_written_durations_from_leaves_in_expr(staff)
      [Rational(1, 8), Rational(1, 8), Rational(1, 8), Rational(1, 8), Rational(1, 8), Rational(1, 8)]

   .. versionchanged:: 1.1.2
      renamed ``leaftools.get_durations_written( )`` to
      ``leaftools.get_written_durations_from_leaves_in_expr( )``.
   '''

   durations = [ ]

   for leaf in iterate.leaves_forward_in_expr(expr):
      durations.append(leaf.duration.written)

   return durations
