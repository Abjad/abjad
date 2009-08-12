from abjad.tools import durtools
from abjad.leaf.leaf import _Leaf


def are_scalable(components, multiplier):
   '''``True`` when every component in `components` can
   rewrite according to `multiplier` with no ad hoc tuplets. ::

      abjad> t = [Note(0, (1, 8))]
      abjad> check.are_scalable(t, Rational(1, 2))
      True

   ::

      abjad> t = [Note(0, (1, 8))]
      abjad> check.are_scalable(t, Rational(3, 2))
      True
   
   ``False`` otherwise. ::

      abjad> t = [Note(0, (1, 8))]
      abjad> check.are_scalable(t, Rational(2, 3))
      False

   Note that `components` must be iterable.
   '''

   for component in components:
      if isinstance(component, _Leaf):
         candidate_duration = multiplier * component.duration.written 
         if not durtools.is_assignable(candidate_duration):
            return False         

   return True
