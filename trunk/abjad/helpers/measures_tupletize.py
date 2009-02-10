from abjad.helpers.iterate import iterate
from abjad.tuplet.fd.tuplet import FixedDurationTuplet
import copy


## TODO: This is a potentially powerful function capable
##       of much generalization.
##       Maybe possible to create a Supplement class
##       to model, for example, cyclic elements of notation
##       to supply to newly created FixedDurationTuplets.
##       Also possible to create FixedMultiplierTuplets,
##       possibly with some sort of ratio indicator.
##       Also possible to strip away elements of measure
##       at tupletization-time, effectively rendering the
##       resulting tuplet an augmentation instead of diminution.

def measures_tupletize(expr, supplement = None):
   '''Tupletize the contents of every measure in expr.
      When supplement is not None, extend newly created
      FixedDurationTuplet by copy of supplement.

      Use primarily during rhythmic construction.

      Note that supplement should be a Python list of 
      notes, rests, chords, tuplets or whatever.

      No treatment of spanners yet implemented.'''

   for measure in iterate(expr, '_Measure'):
      target_duration = measure.duration.preprolated
      tuplet = FixedDurationTuplet(target_duration, measure[:])
      if supplement:
         tuplet.extend(copy.deepcopy(supplement))
