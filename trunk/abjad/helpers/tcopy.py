def tcopy(ll):
   '''
   Clones slice of music from some container.
   Asserts that all elements in input list ll are contiguous.
   
   Sample usage:

     tcopy(t[37 : 39 + 1])

   Returns copied music in container of type T,
   where T is the type of the parent of the first element in ll.
   '''

   # assert that all elements in ll live inside a shared container
   for i, element in enumerate(ll[ : -1]):
      try:
         assert element.next == ll[i + 1] 
      except AssertionError:
         raise AssertionError(
            'Input to tcopy( ) must share a single container.')

   # remember parent
   parent = ll[0]._parent

   # remember parent's music
   parents_music = ll[0]._parent._music

   # strip parent of music temporarily
   parent._music = [ ]

   # copy parent without music
   result = parent.copy( )

   # give music back to parent
   parent._music = parents_music

   # populate result with references to input list
   result.extend(ll)

   # populate result with deepcopy of input list;
   # fractures spanners for free
   result = result.copy( )

   #result = result._music[ : ]

   #for x in result:
   #   x._parent = None

   # give parent back to input list
   for element in ll:
      element._parent = parent

   return result
