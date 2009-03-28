from abjad.helpers.container_set_multiplier import _container_set_multiplier
from abjad.helpers.measure_set_denominator import _measure_set_denominator


def container_hew(container, i, spanners = 'preserve'):
   r'''Split container in two just before index i.
      Compare with container_split( ).
      Special spanner management to leave all spanners in tact.
      Preserve parentage, if any.
      Resize resizable containers.
      Preserve container multiplier, if any.
      Preserve meter denominator, if any.

      Example of hewing binary measure:

      t = Voice(RigidMeasure((3, 8), run(3)) * 2)
      diatonicize(t)
      p = Beam(t[:])

      \new Voice {
                      \time 3/8
                      c'8 [
                      d'8
                      e'8
                      \time 3/8
                      f'8
                      g'8
                      a'8 ]
      }
                 
      container_hew(t[1], 1)

      \new Voice {
                      \time 3/8
                      c'8 [
                      d'8
                      e'8
                      \time 1/8
                      f'8
                      \time 2/8
                      g'8
                      a'8 ]
      }'''

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
   left = container.copy( )
   left.spanners.clear( )

   # create empty righthand container
   right = container.copy( )
   right.spanners.clear( )

   # give music back to container
   container._music = container_music

   # apportion music from container to left ...
   # ... and do not withdraw from spanners!
   #left[:] = container[:i]
   left._music[:] = container[:i]
   for component in left:
      component.parentage._switchParentTo(left)

   # reassign remaining music from container to right ...
   # ... and do not withdraw from spanners!
   #right[:] = container[:]
   right._music[:] = container[:]
   for component in right:
      component.parentage._switchParentTo(right)

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
   if spanners == 'fracture':
      left.spanners.fracture(direction = 'right')

   # set left and right multiplier equal to container multiplier, if any
   _container_set_multiplier(left, container_multiplier)
   _container_set_multiplier(right, container_multiplier)

   # set left and right meter denominator, if any
   _measure_set_denominator(left, meter_denominator)
   _measure_set_denominator(right, meter_denominator)

   # return new left and right parts
   return left, right
