from abjad.components._Leaf import _Leaf
from abjad.components._Measure import _Measure
from abjad.tools import tietools
from abjad.tools import tuplettools
from abjad.tools.tuplettools import FixedDurationTuplet


def scale_contents_of_container(container, multiplier):
   r'''.. versionadded:: 1.1.1

   Scale `container` contents by dot `multiplier`::

      abjad> staff = Staff(macros.scale(2))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
      }
      
   ::
      
      abjad> containertools.scale_contents_of_container(staff, Rational(3, 2))
      Staff{2}

   ::

      abjad> f(staff)
      \new Staff {
         c'8. [
         d'8. ]
      }
   
   Scale `container` contents by tie `multiplier`::

      abjad> staff = Staff(macros.scale(2))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
      }
      
   ::
      
      abjad> containertools.scale_contents_of_container(staff, Rational(5, 4))
      Staff{4}

   ::

      abjad> f(staff)
      \new Staff {
         c'8 [ ~
         c'32
         d'8 ~
         d'32 ]
      }

   Scale `container` contents by nonbinary `multiplier`::

      abjad> staff = Staff(macros.scale(2))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
      }
      
   ::
      
      abjad> containertools.scale_contents_of_container(staff, Rational(4, 3))
      Staff{2}

   ::

      abjad> f(staff)
      \new Staff {
         \times 2/3 {
            c'4 [
         }
         \times 2/3 {
            d'4 ]
         }
      }

   Return `container`.

   .. todo:: Move to ``durtools``?

   .. versionchanged:: 1.1.2
      renamed ``containertools.contents_scale( )`` to
      ``containertools.scale_contents_of_container( )``.

   .. versionchanged:: 1.1.2
      renamed ``containertools.scale_container_contents( )`` to
      ``containertools.scale_contents_of_container( )``.
   '''

   for expr in tietools.iterate_topmost_tie_chains_and_components_forward_in_expr(container[:]):
      if tietools.is_tie_chain(expr):
         tietools.add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration(expr, multiplier)
      elif isinstance(expr, tuplettools.FixedDurationTuplet):
         tuplettools.scale_contents_of_tuplets_in_expr_by_multiplier(expr, multiplier)
      elif isinstance(expr, _Measure):
         ## TODO: Move import to higher level of scope? ##
         from abjad.tools import measuretools
         measuretools.scale_contents_of_measures_in_expr(expr, multiplier)
      else:
         raise Exception(NotImplemented)

   return container
