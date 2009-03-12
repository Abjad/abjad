from abjad import *


def retrograde(container):
   '''Retrograde in place the contents of container.
      Container and any of its children may be spanned.'''

   from abjad.container.container import Container

   def offset(x, y):
      if x.offset.score < y.offset.score:
         return -1
      elif x.offset.score > y.offset.score:
         return 1
      else:
         return 0

   if isinstance(container, list):
      container.reverse( )
      return container
   elif isinstance(container, Container):
      container._music.reverse( )
      spanners = container.spanners.contained
      for s in spanners:
         s._components.sort(offset)
