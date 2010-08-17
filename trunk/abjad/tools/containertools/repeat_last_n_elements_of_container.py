from abjad.tools.componenttools.clone_components_and_immediate_parent_of_first_component import clone_components_and_immediate_parent_of_first_component


def repeat_last_n_elements_of_container(container, n = 1, total = 2):
   r'''.. versionadded:: 1.1.1

   Extend `container` with last `n` elements `total` times::

      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
      
   ::
      
      abjad> containertools.repeat_last_n_elements_of_container(staff, n = 2, total = 3)
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

   .. todo:: harmonize name with ``containertools.repeat_contents_of_container( )``.

   .. versionchanged:: 1.1.2
      renamed ``containertools.extend_cyclic( )`` to
      ``containertools.repeat_last_n_elements_of_container( )``.
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
