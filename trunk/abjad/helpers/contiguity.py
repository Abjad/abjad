def _are_atomic_music_elements(ll):
   '''
   Return True if each of the elements in the music list ll
   have no parent.
   '''

   if ll:
      for element in ll:
         if element._parent is not None:
            return False
      return True
   return False


def _are_contiguous_music_elements(ll):
   '''
   Return True if each of the elements in music list ll 
   follow one after the other in some parent container, 
   otherwise False.

   Check for contiguous leaves (which have 'next' and 'prev' handles)
   and also tuplets, measures and other types of input (which don't).
   '''

   parent = ll[0]._parent
   if parent is None:
      return False
   first = ll[0]
   index = parent.index(first)
   for element in ll[1 : ]:
      index += 1
      if element is not parent[index]:
         return False
   return True
