from abjad.leaf.leaf import _Leaf
from abjad.measure.measure import _Measure
from abjad.tools import containertools
from abjad.tools import measuretools
from abjad.tools import parenttools
from abjad.tools import spannertools
from abjad.tools.parenttools.switch import _switch
from abjad.tuplet.tuplet import _Tuplet


def _at_index(component, i, spanners = 'unfractured'):
   '''General component count-split algorithm.
      Works on leaves, tuplets, measures, contexts and unqualified containers.
      Keyword controls spanner behavior at split time.
      Use split.fractured_at_index( ) to fracture spanners.
      Use split.unfractured_at_index( ) to leave spanners unchanged.'''

   ## convenience definition leaf split at index
   if isinstance(component, _Leaf):
      if i <= 0:
         print 'foo'
         if spanners == 'fractured':
            print 'bar'
            component.spanners.fracture(direction = 'left')
         return None, component
      else:
         if spanners == 'fractured':
            component.spanners.fracture(direction = 'right')
         return component, None

   ## remember container multiplier, if any
   container_multiplier = getattr(component.duration, 'multiplier', None)

   ## partition music of input container
   left_music = component[:i]
   right_music = component[i:]

   ## instantiate new left and right containers
   if isinstance(component, _Measure):
      meter_denominator = component.meter.effective.denominator
      left_duration = sum([x.duration.prolated for x in left_music])
      right_duration = sum([x.duration.prolated for x in right_music])
      left = component.__class__(left_duration or (1, 1), left_music)
      right = component.__class__(right_duration or (1, 1), right_music)
   elif isinstance(component, _Tuplet):
      meter_denominator = None
      left = component.__class__(1, left_music)
      right = component.__class__(1, right_music)
   else:
      meter_denominator = None
      left = component.__class__(left_music)
      right = component.__class__(right_music)
   
   ## save left and right parts together for iteration
   parts = [left, right]
   nonempty_parts = [part for part in parts if len(part)]

   ## give attached spanners to children
   spannertools.give_attached_to_children(component)

   ## incorporate left and right parents in score, if possible
   parent, start, stop = parenttools.get_with_indices([component])
   if parent is not None:
      parent._music[start:stop+1] = nonempty_parts
      for part in nonempty_parts:
         part.parentage._switch(parent)
   else:
      left.parentage._switch(None)
      right.parentage._switch(None)

   ## fracture spanners, if requested
   if spanners == 'fractured':
      if len(parts) == 2:
         left.spanners.fracture(direction = 'right')

   ## set left and right multiplier equal to container multiplier, if any
   containertools.multiplier_set(left, container_multiplier)
   containertools.multiplier_set(right, container_multiplier)

   ## set left and right meter denominator, if any
   measuretools.denominator_set(left, meter_denominator)
   measuretools.denominator_set(right, meter_denominator)

   ## return new left and right parts
   return left, right
