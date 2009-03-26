from abjad.helpers.assert_components import assert_components
from abjad.helpers.in_terms_of import _in_terms_of


def tcopy(ll):
   '''Copy list ll of contiguous music from some container.
   
     tcopy(t[37 : 39 + 1])

   Return in container equal to type of first element in ll.
   Shrink result container as necessary to preserve parent multiplier.'''

   from abjad.measure.base import _Measure

   # assert strictly contiguous components in same thread
   assert_components(ll, contiguity = 'strict', share = 'thread')

   # remember parent
   parent = ll[0].parentage.parent

   # new: remember parent multiplier, if any
   parent_multiplier = getattr(parent.duration, 'multiplier', 1)

   # new: remember parent denominator, if any
   if isinstance(parent, _Measure):
      parent_denominator = parent.meter.effective.denominator
   else:
      parent_denominator = None

   # remember parent's music
   parents_music = ll[0].parentage.parent._music

   # strip parent of music temporarily
   parent._music = [ ]

   # copy parent without music
   result = parent.copy( )

   # give music back to parent
   parent._music = parents_music

   # populate result with references to input list
   #result.extend(ll)
   result._music.extend(ll)

   # populate result with deepcopy of input list and fracture spanners
   result = result.copy( )

   # point elements in result to result as new parent
   for element in result:
      element.parentage.parent = result

   # new: resize result to match parent_multiplier, if resizable
   if result.__class__.__name__ == 'FixedDurationTuplet':
      result.duration.target = parent_multiplier * result.duration.contents
   elif result.__class__.__name__ == 'RigidMeasure':
      new_duration = parent_multiplier * result.duration.contents
      result.meter = new_duration._n, new_duration._d

   # new: rewrite result denominator, if available
   if parent_denominator is not None:
      old_meter = result.meter.effective
      old_meter_pair = (old_meter.numerator, old_meter.denominator)
      new_meter = _in_terms_of(old_meter_pair, parent_denominator)
      result.meter = new_meter

   # point elements in input list back to old parent
   for element in ll:
      element.parentage.parent = parent

   # return copy
   return result
