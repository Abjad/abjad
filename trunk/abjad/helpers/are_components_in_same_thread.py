from abjad.component.component import _Component


def _are_components_in_same_thread(expr):
   '''True when expr is a Python list of Abjad components such
      that all components in list carry the same thread signature.

      Otherwise False.'''

   if not isinstance(expr, list):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   signature = first.parentage._threadSignature
   for component in expr[1:]:
      if component.parentage._threadSignature != signature:
         return False

   return True
