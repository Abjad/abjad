from abjad.container import Container
from abjad.tools.containertools.extend_cyclic import extend_cyclic as \
   containertools_extend_cyclic


def contents_multiply(container, total = 2):
   r'''.. versionadded:: 1.1.1

   Multiply `container` contents to `total` repetitions::

      abjad> staff = Staff(construct.scale(2))
      abjad> Beam(staff.leaves)
      abjad> containertools.contents_multiply(staff, 3)
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

      abjad> staff = Staff(construct.scale(2))
      abjad> Beam(staff.leaves)
      abjad> containertools.contents_multiply(staff, 1)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
      }

   Empty `container` when ``total = 0``::

      abjad> staff = Staff(construct.scale(2))
      abjad> Beam(staff.leaves)
      abjad> containertools.contents_multiply(staff, 0)
      abjad> f(staff)
      \new Staff {
      }

   Return `container`.

   .. todo:: rename this function because 'multiply' clashes
      with duration multiplication. Possibly 'reproduce'.
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
   return containertools_extend_cyclic(container, n = n, total = total)
