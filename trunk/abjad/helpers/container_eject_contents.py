from abjad.container.container import Container


def container_eject_contents(container):
   '''Remove contents from container.
      Return list of container contents.'''
   
   assert isinstance(container, Container)

   contents = container[:]
   del(container[:])

   return contents
