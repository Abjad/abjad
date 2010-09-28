from abjad.tools.metertools import Meter


def set_container_multiplier(container, multiplier):
   r'''Set `container` `multiplier`::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> containertools.set_container_multiplier(tuplet, Fraction(3, 4))
      abjad> f(tuplet)
      \fraction \times 3/4 {
         c'8
         d'8
         e'8
      }

   .. todo:: reimplement as settable container duration interface attributes.

   .. versionchanged:: 1.1.2
      renamed ``containertools.multiplier_set( )`` to
      ``containertools.set_container_multiplier( )``.
   '''
   from abjad.components.Measure import Measure
   #from abjad.components.Tuplet import Tuplet
   from abjad.components.Tuplet import Tuplet
   from abjad.tools import tuplettools

   if isinstance(container, tuplettools.FixedDurationTuplet):
      container.duration.target = multiplier * container.duration.contents
   #elif isinstance(container, Tuplet):
   elif isinstance(container, Tuplet):
      container.duration.multiplier = multiplier
   elif isinstance(container, Measure):
      new_duration = multiplier * container.duration.contents
      container._attach_explicit_meter(new_duration.numerator, new_duration.denominator)
