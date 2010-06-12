from abjad.tools.componenttools.clone_components_and_immediate_parent_of_first_component import clone_components_and_immediate_parent_of_first_component


def extend_cyclic(container, n = 1, total = 2):
   r'''.. versionadded:: 1.1.1

   Extend `container` with last `n` elements `total` times::

      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
      
   ::
      
      abjad> containertools.extend_cyclic(staff, n = 2, total = 3)
      Staff{8}

   ::

      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
         e'8 [
         f'8 ]
         e'8 [
         f'8 ]
      }

   Return `container`.

   .. todo:: harmonize name with ``containertools.contents_multiply( )``.
   '''

   # get start and stop indices
   stop = len(container)
   start = stop - n

   # for the total number of elements less one
   for x in range(total - 1):

      # copy last n elements of container
      addendum = clone_components_and_immediate_parent_of_first_component(container[start:stop])

      # extend container with addendum
      container.extend(addendum)

   return container
