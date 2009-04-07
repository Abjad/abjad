def container_set_multiplier(container, multiplier):
   '''Fiddle with other container duration attributes to
      set container.duration.multiplier equal to multiplier.'''

   if container.__class__.__name__ == 'FixedDurationTuplet':
      container.duration.target = multiplier * container.duration.contents
   elif container.__class__.__name__ == 'RigidMeasure':
      new_duration = multiplier * container.duration.contents
      container.meter.forced = new_duration._n, new_duration._d
