from abjad.meter import Meter


def multiplier_set(container, multiplier):
   r'''Set `container` `multiplier`::

      abjad> tuplet = FixedDurationTuplet((2, 8), construct.scale(3))
      abjad> containertools.multiplier_set(tuplet, Rational(3, 4))
      abjad> f(tuplet)
      \fraction \times 3/4 {
         c'8
         d'8
         e'8
      }

   .. todo:: reimplement as settable container duration interface attributes.
   '''

   if container.__class__.__name__ == 'FixedDurationTuplet':
      container.duration.target = multiplier * container.duration.contents
   elif container.__class__.__name__ == 'FixedMultiplierTuplet':
      container.duration.multiplier = multiplier
   elif container.__class__.__name__ == 'RigidMeasure':
      new_duration = multiplier * container.duration.contents
      container.meter.forced = Meter(new_duration._n, new_duration._d)
