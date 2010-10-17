from abjad.tools.durtools.is_assignable_rational import is_assignable_rational


def all_are_components_scalable_by_multiplier(components, multiplier):
   '''True when `components` are all scalable by `multiplier`::

      abjad> components = [Note(0, (1, 8))]
      abjad> componenttools.all_are_components_scalable_by_multiplier(components, Fraction(3, 2))
      True
   
   Otherwise false::

      abjad> components = [Note(0, (1, 8))]
      abjad> componenttools.all_are_components_scalable_by_multiplier(components, Fraction(2, 3))
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``durtools.are_scalable( )`` to
      ``componenttools.all_are_components_scalable_by_multiplier( )``.
   '''

   from abjad.components._Leaf import _Leaf
   for component in components:
      if isinstance(component, _Leaf):
         candidate_duration = multiplier * component.duration.written 
         if not is_assignable_rational(candidate_duration):
            return False         

   return True
