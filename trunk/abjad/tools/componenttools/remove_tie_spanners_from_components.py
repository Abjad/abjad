from abjad.tools import check


def remove_tie_spanners_from_components(components):
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
      
      abjad> componenttools.remove_tie_spanners_from_components(staff[:])
      abjad> f(staff)
      \new Staff {
         c'4
         c'16
         d'4
         d'16
      }

   Return `components`.

   .. todo:: move to ``tietools``.

   .. versionchanged:: 1.1.2
      renamed ``componenttools.untie_shallow( )`` to
      ``componenttools.remove_tie_spanners_from_components( )``.
   '''

   check.assert_components(components, contiguity = 'thread')

   for component in components:
      component.tie.unspan( )

   return components
