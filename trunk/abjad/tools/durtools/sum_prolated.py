def sum_prolated(components):
   '''Sum of prolated duration of each component in 'components' list.'''

   assert isinstance(components, list)
   return sum([component.duration.prolated for component in components])
