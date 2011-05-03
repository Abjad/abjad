from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def list_written_durations_of_leaves_in_expr(expr):
   '''.. versionadded:: 1.1.2

   List the written durations of leaves in `expr`::

      abjad> staff = Staff(tuplettools.FixedDurationTuplet((2, 8), macros.scale(3)) * 2)
      abjad> leaftools.list_written_durations_of_leaves_in_expr(staff)
      [Fraction(1, 8), Fraction(1, 8), Fraction(1, 8), Fraction(1, 8), Fraction(1, 8), Fraction(1, 8)]

   Return list of fractions.
   '''

   durations = [ ]

   for leaf in iterate_leaves_forward_in_expr(expr):
      durations.append(leaf.duration.written)

   return durations
