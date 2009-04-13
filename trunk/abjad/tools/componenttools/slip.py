from abjad.tools import parenttools


## TODO: Generalize componenttools.slip( ) to take component list. ##

def slip(component):
   '''Give spanners attached directly to container to children.
      Give children to parent.
      Return component.'''

   parent, start, stop = parenttools.get_with_indices([component])
   result = parent[start:stop+1] = list(component.music)
   return component
