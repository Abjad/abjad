def sum_seconds(components):
   '''Sum of duration in seconds of each component in 'components' list.'''

   assert isinstance(components, list)
   return sum([component.duration.seconds for component in components])
