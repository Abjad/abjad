def integer_tripartition(n, smallest = 'middle', biggest = 'middle'):
   '''Partition integer n into three parts, returned as a tuple.'''

   assert isinstance(n, int)
   assert smallest in ('left', 'middle', 'right')
   assert biggest in ('left', 'middle', 'right')
   
   small = int(n / 3)
   big = small + 1

   if n % 3 == 0:
      return small, small, small
   elif n % 3 == 1:
      if biggest == 'left':
         return big, small, small
      elif biggest == 'middle':
         return small, big, small
      elif biggest == 'right':
         return small, small, big
   elif n % 3 == 2:
      if smallest == 'left':
         return small, big, big
      elif smallest == 'middle':
         return big, small, big
      elif smallest == 'right':
         return big, big, small
