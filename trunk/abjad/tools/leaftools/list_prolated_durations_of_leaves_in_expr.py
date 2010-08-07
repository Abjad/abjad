from abjad.tools import iterate


def list_prolated_durations_of_leaves_in_expr(expr):
   '''.. versionadded:: 1.1.2

   Get the prolated duration of every leaf in `expr`::

      abjad> staff = Staff(FixedDurationTuplet((2, 8), macros.scale(3)) * 2)
      abjad> leaftools.list_prolated_durations_of_leaves_in_expr(staff)
      [Rational(1, 12), Rational(1, 12), Rational(1, 12), Rational(1, 12), Rational(1, 12), Rational(1, 12)]

   .. versionchanged:: 1.1.2
      renamed ``leaftools.get_durations_prolated( )`` to
      ``leaftools.list_prolated_durations_of_leaves_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.get_prolated_durations_from_leaves_in_expr( )`` to
      ``leaftools.list_prolated_durations_of_leaves_in_expr( )``.
   '''

   durations = [ ]

   for leaf in iterate.leaves_forward_in_expr(expr):
      durations.append(leaf.duration.prolated)

   return durations
