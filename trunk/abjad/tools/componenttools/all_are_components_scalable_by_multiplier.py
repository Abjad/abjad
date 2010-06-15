from abjad.tools.durtools.is_assignable_rational import is_assignable_rational


def all_are_components_scalable_by_multiplier(components, multiplier):
   '''True when every component in `components` can
   rewrite according to `multiplier` with no ad hoc tuplets. ::

      abjad> t = [Note(0, (1, 8))]
      abjad> componenttools.all_are_components_scalable_by_multiplier(t, Rational(1, 2))
      True

   ::

      abjad> t = [Note(0, (1, 8))]
      abjad> componenttools.all_are_components_scalable_by_multiplier(t, Rational(3, 2))
      True
   
   False otherwise. ::

      abjad> t = [Note(0, (1, 8))]
      abjad> componenttools.all_are_components_scalable_by_multiplier(t, Rational(2, 3))
      False

   Note that `components` must be iterable.

   .. versionchanged:: 1.1.2
      renamed ``durtools.are_scalable( )`` to
      ``componenttools.all_are_components_scalable_by_multiplier( )``.
   '''

   from abjad.leaf import _Leaf
   for component in components:
      if isinstance(component, _Leaf):
         candidate_duration = multiplier * component.duration.written 
         if not is_assignable_rational(candidate_duration):
            return False         

   return True
