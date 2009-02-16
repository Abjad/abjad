def cumulative_products(l):
   '''Return a list of the cumulative products of the elements in l.'''

   result = [l[0]]
   for element in l[1:]:
      result.append(result[-1] * element) 

   return result
