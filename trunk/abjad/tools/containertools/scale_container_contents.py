from abjad.leaf import _Leaf
from abjad.measure import _Measure
from abjad.tools import iterate
from abjad.tools import tietools
from abjad.tools import tuplettools
from abjad.tuplet import FixedDurationTuplet


def scale_container_contents(container, multiplier):
   r'''.. versionadded:: 1.1.1

   Scale `container` contents by dot `multiplier`::

      abjad> staff = Staff(construct.scale(2))
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
      }
      
   ::
      
      abjad> containertools.scale_container_contents(staff, Rational(3, 2))
      Staff{2}

   ::

      abjad> f(staff)
      \new Staff {
         c'8. [
         d'8. ]
      }
   
   Scale `container` contents by tie `multiplier`::

      abjad> staff = Staff(construct.scale(2))
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
      }
      
   ::
      
      abjad> containertools.scale_container_contents(staff, Rational(5, 4))
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

      abjad> staff = Staff(construct.scale(2))
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
      }
      
   ::
      
      abjad> containertools.scale_container_contents(staff, Rational(4, 3))
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
      ``containertools.scale_container_contents( )``.
   '''

   for expr in iterate.chained_contents(container[:]):
      if tietools.is_chain(expr):
         tietools.duration_scale(expr, multiplier)
      elif isinstance(expr, FixedDurationTuplet):
         tuplettools.contents_scale(expr, multiplier)
      elif isinstance(expr, _Measure):
         ## TODO: Move import to higher level of scope? ##
         from abjad.tools import measuretools
         measuretools.scale_measure_contents_in(expr, multiplier)
      else:
         raise Exception(NotImplemented)

   return container
