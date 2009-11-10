from abjad.container import Container


def contents_delete(container):
   '''Remove contents from container.
   Return list of container contents.
   '''
   
   assert isinstance(container, Container)

   contents = container[:]
   del(container[:])

   return contents
