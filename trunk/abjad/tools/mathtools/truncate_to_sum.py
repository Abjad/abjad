
def truncate_to_sum(ls, total):
   '''
   Truncate the given numeric list ls so that sum(ls) == total.
   Example:
   >>> for i in range(7):
   ...    truncate_to_sum([2,2,2], i)
   [0]
   [1]
   [2]
   [2, 1]
   [2, 2]
   [2, 2, 1]
   [2, 2, 2]
   '''
   assert total >= 0
   result = [ ]
   kind = type(ls)
   accumulation = 0
   for e in ls:
      accumulation += e
      if accumulation < total:
         result.append(e)
      else:
         result.append(total - sum(result))
         break
   return kind(result)
      

