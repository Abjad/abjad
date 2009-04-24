def sum_preprolated(components):
   '''Sum of preprolated duration of each component in 'components' list.'''

   assert isinstance(components, list)
   return sum([component.duration.preprolated for component in components])
