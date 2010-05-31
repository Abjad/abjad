from abjad.container import Container


def contents_reverse(container):
   r'''.. versionadded:: 1.1.1

   Reverse `container` contents in place::

      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves[:2])
      abjad> Slur(staff.leaves[2:])
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
         e'8 (
         f'8 )
      }
      
   ::
      
      abjad> containertools.contents_reverse(staff)
      Staff{4}

   ::

      abjad> f(staff)
      \new Staff {
         f'8 (
         e'8 )
         d'8 [
         c'8 ]
      }

   Return `container`.
   '''

   def offset(x, y):
      if x.offset.prolated.start < y.offset.prolated.start:
         return -1
      elif x.offset.prolated.start > y.offset.prolated.start:
         return 1
      else:
         return 0

   if isinstance(container, list):
      container.reverse( )
   elif isinstance(container, Container):
      container._music.reverse( )
      spanners = container.spanners.contained
      for s in spanners:
         s._components.sort(offset)

   return container
