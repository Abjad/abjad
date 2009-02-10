from abjad.helpers.container_set_multiplier import _container_set_multiplier
from abjad.helpers.measure_set_denominator import _measure_set_denominator


def container_hew(container, i):
   '''Split container in two just before index i;
      compare with container_split( ).
      Special spanner management to leave all spanners in tact.
      Preserve parentage, if any;
      Resize resizable containers;
      Preserve container multiplier, if any;
      Preserve meter denominator, if any.'''

   # remember container multiplier, if any
   container_multiplier = getattr(container.duration, 'multiplier', None)

   # remember container meter denominator, if any
   if container.kind('_Measure'):
      meter_denominator = container.meter.effective.denominator
   else:
      meter_denominator = None

   # remember container music
   container_music = container._music

   # temporarily remove music from container
   container._music = [ ]

   # create empty lefthand container
   left = container.copy( )
   left.spanners.clear( )

   # create empty righthand container
   right = container.copy( )
   right.spanners.clear( )

   # give music back to container
   container._music = container_music

   # apportion music from container to left
   left[:] = container[:i]

   # reassign remaining music from container to right
   right[:] = container[:]

   # if parent
   if container._parent is not None:

      # get index of container in parent
      container_index = container._parent.index(container) 

      # insert left and right in place of container in parent
      container._parent[i:i+1] = [left, right] 

   # for every spanner attaching to container
   for spanner in list(container.spanners.attached):
   
      # get index of container in spanner 
      spanner_index = spanner.index(container)

      # insert left and right in spanner in place of container
      spanner[spanner_index : spanner_index + 1] = [left, right]

   # set left and right multiplier equal to container multiplier, if any
   _container_set_multiplier(left, container_multiplier)
   _container_set_multiplier(right, container_multiplier)

   # set left and right meter denominator, if any
   _measure_set_denominator(left, meter_denominator)
   _measure_set_denominator(right, meter_denominator)
