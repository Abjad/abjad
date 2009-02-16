def cumulative_sums(l):
   '''Return a list of the cumulative sums of the integer elements in l.'''

   result = [l[0]]
   for element in l[1:]:
      result.append(result[-1] + element) 

   return result
