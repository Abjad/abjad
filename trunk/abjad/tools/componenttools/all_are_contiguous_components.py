from abjad.components._Component import _Component
import types


def all_are_contiguous_components(expr, klasses = (_Component, ), allow_orphans = True):
   '''True expr is a Python list of strictly contiguous components.
      Otherwise False.
   '''

   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, klasses):
      return False

   orphan_components = True
   if not first.parentage.orphan:
      orphan_components = False

   strictly_contiguous = True

   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, klasses):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      if not prev._navigator._is_immediate_temporal_successor_of(cur):
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         not strictly_contiguous:
         return False
      prev = cur

   return True
