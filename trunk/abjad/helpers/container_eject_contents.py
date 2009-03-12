from abjad.container.container import Container


def container_eject_contents(container):
   '''Remove any contents from container.
      Container keeps position-in-score and position-in-spanners.

      Return list of container contents.'''
   
   assert isinstance(container, Container)

   contents = container[:]
   ## TODO: Implement components_parentage_detach_shallow( )
   for component in contents:
      component.parentage._detach( )

   return contents
