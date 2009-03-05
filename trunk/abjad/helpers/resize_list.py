from __future__ import division
import math

def _resize_list(lst, size):
   '''
   Returns a resized copy of the given list. 
   If len(list) < size, append copies of list to itself and truncate excedent.
   If len(list) > size, simply truncate.
   '''
   assert isinstance(lst, list)
   assert isinstance(size, int)
   assert size > 0
   assert len(lst) > 0

   if len(lst) == size:
      return lst[:]
   elif len(lst) > size:
      return lst[0:size]
   else:
      lst = lst * int(math.ceil(size / len(lst)))
      return lst[0:size]
