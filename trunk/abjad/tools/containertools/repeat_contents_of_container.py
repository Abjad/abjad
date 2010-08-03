from abjad.components.Container import Container
from abjad.tools.containertools.repeat_last_n_elements_of_container import repeat_last_n_elements_of_container


def repeat_contents_of_container(container, total = 2):
   r'''.. versionadded:: 1.1.1

   Multiply `container` contents to `total` repetitions::

      abjad> staff = Staff(macros.scale(2))
      abjad> Beam(staff.leaves)
      abjad> containertools.repeat_contents_of_container(staff, 3)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
         c'8 [
         d'8 ]
         c'8 [
         d'8 ]
      }

   Leave `container` unchanged when ``total = 1``::

      abjad> staff = Staff(macros.scale(2))
      abjad> Beam(staff.leaves)
      abjad> containertools.repeat_contents_of_container(staff, 1)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
      }

   Empty `container` when ``total = 0``::

      abjad> staff = Staff(macros.scale(2))
      abjad> Beam(staff.leaves)
      abjad> containertools.repeat_contents_of_container(staff, 0)
      abjad> f(staff)
      \new Staff {
      }

   Return `container`.

   .. todo:: rename this function because 'multiply' clashes
      with duration multiplication. Possibly 'reproduce'.

   .. versionchanged:: 1.1.2
      renamed ``containertools.contents_multiply( )`` to
      ``containertools.repeat_contents_of_container( )``.
   '''

   if not isinstance(container, Container):
      raise TypeError('must be container: %s' % container)

   if not isinstance(total, int):
      raise TypeError('must be int: %s' % total)

   if not 0 <= total:
      raise ValueError('must be greater than or equal to zero: %s' % total)

   ## empty container when total is zero
   if total == 0:
      del(container[:])
      return container

   ## reproduce container contents when total is greater than zero
   n = len(container)
   return repeat_last_n_elements_of_container(container, n = n, total = total)
