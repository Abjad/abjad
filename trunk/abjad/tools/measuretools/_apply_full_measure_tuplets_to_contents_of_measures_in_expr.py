from abjad.tools import iterate
from abjad.components._Tuplet import FixedDurationTuplet
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr
import copy


def _apply_full_measure_tuplets_to_contents_of_measures_in_expr(expr, supplement = None):
   '''Tupletize the contents of every measure in expr.
   When supplement is not None, extend newly created
   FixedDurationTuplet by copy of supplement.

   Use primarily during rhythmic construction.

   Note that supplement should be a Python list of 
   notes, rests, chords, tuplets or whatever.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.tupletize( )``
      to ``measuretools._apply_full_measure_tuplets_to_contents_of_measures_in_expr( )``.
   '''

   for measure in iterate_measures_forward_in_expr(expr):
      target_duration = measure.duration.preprolated
      tuplet = FixedDurationTuplet(target_duration, measure[:])
      if supplement:
         tuplet.extend(copy.deepcopy(supplement))
