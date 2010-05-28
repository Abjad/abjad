from abjad.tools import check


def untie_shallow(components):
   r'''Untie thread-contiguous `components`. ::

      abjad> staff = Staff(construct.scale(2, (5, 16)))
      abjad> f(staff)
      \new Staff {
         c'4 ~
         c'16
         d'4 ~
         d'16
      }
      
   ::
      
      abjad> componenttools.untie_shallow(staff[:])
      abjad> f(staff)
      \new Staff {
         c'4
         c'16
         d'4
         d'16
      }

   Return `components`.

   .. todo:: move to ``tietools``.
   '''

   check.assert_components(components, contiguity = 'thread')

   for component in components:
      component.tie.unspan( )

   return components
