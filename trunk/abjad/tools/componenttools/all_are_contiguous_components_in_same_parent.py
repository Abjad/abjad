from abjad._Component import _Component
import types


def all_are_contiguous_components_in_same_parent(expr, klasses = (_Component, ), 
   allow_orphans = True):
   '''True when expr is a Python list of Abjad components such that

         1. all components in list are strictly contiguous, and
         2. every component in list has the same parent.

      Otherwise False.
   '''

   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, klasses):
      return False

   first_parent = first.parentage.parent
   if first_parent is None:
      if allow_orphans:
         orphan_components = True
      else:
         return False
   
   same_parent = True
   strictly_contiguous = True

   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, klasses):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      if not cur.parentage.parent is first_parent:
         same_parent = False
      if not prev._navigator._is_immediate_temporal_successor_of(cur):
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_parent or not strictly_contiguous):
         return False
      prev = cur

   return True
