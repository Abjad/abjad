from abjad.container import Container


def contents_delete(container):
   r'''Delete `container` contents::

      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)

   ::

      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
      
   ::
      
      abjad> containertools.contents_delete(staff)
      [Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8)]

   ::

      abjad> f(staff)
      \new Staff {
      }

   Return `container` contents.

   Raise type error on noncontainer::

      abjad> containertools.contents_delete(Note(0, (1, 4)))
      TypeError
   '''
   
   if not isinstance(container, Container):
      raise TypeError('must be container.')

   contents = container[:]
   del(container[:])

   return contents
