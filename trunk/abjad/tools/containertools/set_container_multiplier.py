from abjad.tools.metertools import Meter


def set_container_multiplier(container, multiplier):
   r'''Set `container` `multiplier`::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> containertools.set_container_multiplier(tuplet, Rational(3, 4))
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

   if container.__class__.__name__ == 'FixedDurationTuplet':
      container.duration.target = multiplier * container.duration.contents
   elif container.__class__.__name__ == 'FixedMultiplierTuplet':
      container.duration.multiplier = multiplier
   elif container.__class__.__name__ == 'RigidMeasure':
      new_duration = multiplier * container.duration.contents
      container.meter.forced = Meter(new_duration.numerator, new_duration.denominator)
