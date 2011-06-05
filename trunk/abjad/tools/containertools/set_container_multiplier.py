from abjad.tools.metertools import Meter


## TODO: reimplement as settable attribute of container duration interface.
def set_container_multiplier(container, multiplier):
   r'''Set `container` `multiplier`::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")

   ::

      abjad> f(tuplet)
      \times 2/3 {
         c'8
         d'8
         e'8
      }

   ::

      abjad> containertools.set_container_multiplier(tuplet, Duration(3, 4))

   ::

      abjad> f(tuplet)
      \fraction \times 3/4 {
         c'8
         d'8
         e'8
      }
   
   Return none.

   .. versionchanged:: 1.1.2
      renamed ``containertools.multiplier_set( )`` to
      ``containertools.set_container_multiplier( )``.
   '''
   from abjad.components import Measure
   from abjad.components import Tuplet
   from abjad.tools import tuplettools

   if isinstance(container, tuplettools.FixedDurationTuplet):
      container.duration.target = multiplier * container.duration.contents
   elif isinstance(container, Tuplet):
      container.duration.multiplier = multiplier
   elif isinstance(container, Measure):
      new_duration = multiplier * container.duration.contents
      container._attach_explicit_meter(new_duration.numerator, new_duration.denominator)
