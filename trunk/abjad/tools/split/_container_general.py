from abjad.measure.measure import _Measure
from abjad.tools import containertools
from abjad.tools import measuretools
from abjad.tools import parenttools
from abjad.tuplet.tuplet import _Tuplet


def _container_general(container, i, spanners = 'unfractured'):
   '''General container split algorithm.
      Works on tuplets, measures, contexts and unqualified containers.
      Keyword controls spanner behavior at split time.
      Use split.container_fractured( ) to fracture spanners.
      Use split.container_unfractured( ) to leave spanners unchanged.'''

   # remember container multiplier, if any
   container_multiplier = getattr(container.duration, 'multiplier', None)

   # remember container meter denominator, if any
   if isinstance(container, _Measure):
      meter_denominator = container.meter.effective.denominator
   else:
      meter_denominator = None

   left_music = container[:i]
   right_music = container[i:]

   if isinstance(container, _Measure):
      left_duration = sum([x.duration.prolated for x in left_music])
      right_duration = sum([x.duration.prolated for x in right_music])
      #right = container.__class__(right_duration, container[i:])
      #left = container.__class__(left_duration, container[:i])
      right = container.__class__(right_duration, right_music)
      left = container.__class__(left_duration, left_music)
   elif isinstance(container, _Tuplet):
      #right = container.__class__(1, container[i:])
      #left = container.__class__(1, container[:i])
      right = container.__class__(1, right_music)
      left = container.__class__(1, left_music)
   else:
      #right = container.__class__(container[i:])
      #left = container.__class__(container[:i])
      right = container.__class__(right_music)
      left = container.__class__(left_music)
   
   parts = [left, right]

#   print container, container.spanners.attached
#   print left, left.spanners.attached
#   print right, right.spanners.attached
#   print ''
   
   ## QUESTION: Can this first branch be bequeath( ) or donate( )? ##

   parent, start, stop = parenttools.get_with_indices([container])
   if parent is not None:
      #parent[start:stop+1] = [part for part in parts if len(part)]
      nonempty = [part for part in parts if len(part)]
      parent._music[start:stop+1] = nonempty
      for part in nonempty:
         part.parentage._switch(parent)
      for spanner in list(container.spanners.attached):
         i = spanner.index(container)
         spanner._components[i:i+1] = nonempty
         for part in nonempty:
            part.spanners._add(spanner)
   else:
      ## TODO: Implement spannertools._give_attached_to( ) ##
      for spanner in list(container.spanners.attached):
         i = spanner.index(container)
         spanner._components[i:i+1] = parts
         parts.spanners.attached._add(spanner) # fix this line
      left.parentage._switch(None)
      right.parentage._switch(None)

   #print container, container.spanners.attached
   #print left, left.spanners.attached
   #print right, right.spanners.attached
   #print ''

   if spanners == 'fractured':
      if len(parts) == 2:
         left.spanners.fracture(direction = 'right')
   
   # set left and right multiplier equal to container multiplier, if any
   containertools.multiplier_set(left, container_multiplier)
   containertools.multiplier_set(right, container_multiplier)

   # set left and right meter denominator, if any
   measuretools.denominator_set(left, meter_denominator)
   measuretools.denominator_set(right, meter_denominator)

   # return new left and right parts
   return left, right
