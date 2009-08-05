from abjad.meter import Meter


def multiplier_set(container, multiplier):
   '''Fiddle with other container duration attributes to
      set container.duration.multiplier equal to multiplier.'''

   ## TODO: Reimplement as settable container duration interface attrs ##

   if container.__class__.__name__ == 'FixedDurationTuplet':
      container.duration.target = multiplier * container.duration.contents
   elif container.__class__.__name__ == 'FixedMultiplierTuplet':
      container.duration.multiplier = multiplier
   elif container.__class__.__name__ == 'RigidMeasure':
      new_duration = multiplier * container.duration.contents
      container.meter.forced = Meter(new_duration._n, new_duration._d)
