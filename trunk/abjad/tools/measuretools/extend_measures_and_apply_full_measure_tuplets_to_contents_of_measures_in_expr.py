from abjad.tools.measuretools._apply_full_measure_tuplets_to_contents_of_measures_in_expr import \
   _apply_full_measure_tuplets_to_contents_of_measures_in_expr


def extend_measures_and_apply_full_measure_tuplets_to_contents_of_measures_in_expr(
   expr, supplement):
   '''Extend measures in `expr` with `supplement` and apply full-measure tuplets to contents 
   of measures.
   '''

   return _apply_full_measure_tuplets_to_contents_of_measures_in_expr(expr, supplement)
