from abjad.leaf.leaf import _Leaf
from abjad.measure.measure import _Measure
from abjad.meter import Meter
from abjad.tools import containertools
from abjad.tools import durtools
from abjad.tools import measuretools
from abjad.tools import metertools
from abjad.tools import parenttools
from abjad.tools import spannertools
from abjad.tools.parenttools.switch import _switch
from abjad.tuplet.tuplet import _Tuplet


def _at_index(component, i, spanners = 'unfractured'):
   '''General component index split algorithm.
      Works on leaves, tuplets, measures, contexts and unqualified containers.
      Keyword controls spanner behavior at split time.
      Use split.fractured_at_index( ) to fracture spanners.
      Use split.unfractured_at_index( ) to leave spanners unchanged.'''

   ## convenience leaf index split definition
   if isinstance(component, _Leaf):
      if i <= 0:
         if spanners == 'fractured':
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
      left_pair = durtools.in_terms_of_binary_multiple(
         left_duration, meter_denominator)
      left_meter = Meter(*left_pair)
      left = component.__class__(left_meter, left_music)
      right_duration = sum([x.duration.prolated for x in right_music])
      right_pair = durtools.in_terms_of_binary_multiple(
         right_duration, meter_denominator)
      right_meter = Meter(*right_pair)
      right = component.__class__(right_meter, right_music)
   elif isinstance(component, _Tuplet):
      left = component.__class__(1, left_music)
      right = component.__class__(1, right_music)
      containertools.multiplier_set(left, container_multiplier)
      containertools.multiplier_set(right, container_multiplier)
   else:
      left = component.__class__(left_music)
      right = component.__class__(right_music)
      containertools.multiplier_set(left, container_multiplier)
      containertools.multiplier_set(right, container_multiplier)
   
   ## save left and right halves together for iteration
   halves = [left, right]
   nonempty_halves = [half for half in halves if len(half)]

   ## give attached spanners to children
   spannertools.give_attached_to_children(component)

   ## incorporate left and right parents in score, if possible
   parent, start, stop = parenttools.get_with_indices([component])
   if parent is not None:
      parent._music[start:stop+1] = nonempty_halves
      for part in nonempty_halves:
         part.parentage._switch(parent)
   else:
      left.parentage._switch(None)
      right.parentage._switch(None)

   ## fracture spanners, if requested
   if spanners == 'fractured':
      if len(halves) == 2:
         left.spanners.fracture(direction = 'right')

   ## return new left and right halves
   return left, right
