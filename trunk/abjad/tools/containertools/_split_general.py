from abjad.tools import clone
from abjad.tools import measuretools
from abjad.tools.containertools.multiplier_set import multiplier_set


def _split_general(container, i, spanners = 'unfractured'):
   '''General container split algorithm.
      Works on tuplets, measures, contexts and unqualified containers.
      Keyword controls spanner behavior at split time.
      Use containertools.split_fractured( ) to fracture spanners.
      Use containertools.split_unfractured( ) to leave spanners unchanged.'''

   from abjad.measure.measure import _Measure

   # remember container multiplier, if any
   container_multiplier = getattr(container.duration, 'multiplier', None)

   # remember container meter denominator, if any
   if isinstance(container, _Measure):
      meter_denominator = container.meter.effective.denominator
   else:
      meter_denominator = None

   # remember container music
   container_music = container._music

   # temporarily remove music from container
   container._music = [ ]

   # create empty lefthand container
   left = clone.unspan([container])[0]
   left.spanners.clear( )

   # create empty righthand container
   right = clone.unspan([container])[0]
   right.spanners.clear( )

   # give music back to container
   container._music = container_music

   # apportion music from container to left ...
   # ... and do not withdraw from spanners!
   #left[:] = container[:i]
   left._music[:] = container[:i]
   for component in left:
      component.parentage._switch(left)

   # reassign remaining music from container to right ...
   # ... and do not withdraw from spanners!
   #right[:] = container[:]
   right._music[:] = container[:]
   for component in right:
      component.parentage._switch(right)

   # if parent
   if container.parentage.parent is not None:

      # get index of container in parent
      container_index = container.parentage.parent.index(container)

      # insert left and right in place of container in parent
      container.parentage.parent[container_index : container_index + 1] = \
         [left, right] 

   # for every spanner attaching to container
   for spanner in list(container.spanners.attached):
   
      # get index of container in spanner 
      spanner_index = spanner.index(container)

      # insert left and right in spanner in place of container
      #spanner[spanner_index : spanner_index + 1] = [left, right]
      spanner._components[spanner_index:spanner_index+1] = [left, right]
   left.spanners._update(list(container.spanners.attached))
   right.spanners._update(list(container.spanners.attached))

   # fracture spanners across newly hewn parts, if requested
   if spanners == 'fractured':
      left.spanners.fracture(direction = 'right')

   # set left and right multiplier equal to container multiplier, if any
   multiplier_set(left, container_multiplier)
   multiplier_set(right, container_multiplier)

   # set left and right meter denominator, if any
   measuretools.denominator_set(left, meter_denominator)
   measuretools.denominator_set(right, meter_denominator)

   # return new left and right parts
   return left, right
