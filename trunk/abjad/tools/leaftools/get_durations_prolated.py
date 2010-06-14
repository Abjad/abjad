from abjad.tools import iterate


def get_durations_prolated(expr):
   '''.. versionadded:: 1.1.2

   Get the prolated duration of every leaf in `expr`::

      abjad> staff = Staff(FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3)) * 2)
      abjad> leaftools.get_durations_prolated(staff)
      [Rational(1, 12), Rational(1, 12), Rational(1, 12), Rational(1, 12), Rational(1, 12), Rational(1, 12)]
   '''

   durations = [ ]

   for leaf in iterate.leaves_forward_in(expr):
      durations.append(leaf.duration.prolated)

   return durations
