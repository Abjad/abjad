from abjad.container.container import Container


def container_eject_contents(container):
   '''Remove any contents from container.
      Container keeps position-in-score and position-in-spanners.

      Return list of container contents.'''
   
   assert isinstance(container, Container)

   contents = container[:]
   for component in contents:
      component.parentage.detach( )

   return contents
