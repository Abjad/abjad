def is_beamable_component(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` is a beamable component.
   '''

   from abjad.components._Leaf import _Leaf
   from abjad.tools import durtools
   if isinstance(expr, _Leaf):
      if 0 < durtools.rational_to_flag_count(expr.duration.written):
         return True
   return False
