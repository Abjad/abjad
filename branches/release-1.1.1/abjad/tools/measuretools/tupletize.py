from abjad.measure.measure import _Measure
from abjad.tools import iterate
from abjad.tuplet import FixedDurationTuplet
import copy


def tupletize(expr, supplement = None):
   '''Tupletize the contents of every measure in expr.
      When supplement is not None, extend newly created
      FixedDurationTuplet by copy of supplement.

      Use primarily during rhythmic construction.

      Note that supplement should be a Python list of 
      notes, rests, chords, tuplets or whatever.'''

   for measure in iterate.naive(expr, _Measure):
      target_duration = measure.duration.preprolated
      tuplet = FixedDurationTuplet(target_duration, measure[:])
      if supplement:
         tuplet.extend(copy.deepcopy(supplement))
