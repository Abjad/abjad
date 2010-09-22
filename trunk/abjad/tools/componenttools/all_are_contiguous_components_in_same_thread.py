from abjad.components._Component import _Component
from abjad.tools import threadtools
from abjad.tools.componenttools.component_is_orphan import component_is_orphan
import types


def all_are_contiguous_components_in_same_thread(expr, klasses = (_Component), 
   allow_orphans = True):
   '''True when expr is a Python list of Abjad components such that
         
         1. all components in list are strictly contiguous, and
         2. all components in list are in the same thread.

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
   #if not first.parentage.is_orphan:
   if not component_is_orphan(first):
      orphan_components = False

   same_thread = True
   strictly_contiguous = True

   #first_signature = first.thread.signature
   first_signature = threadtools.component_to_thread_signature(first)
   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, klasses):
         return False
      #if not cur.parentage.is_orphan:
      if not component_is_orphan(cur):
         orphan_components = False
      #cur_signature = cur.thread.signature
      cur_signature = threadtools.component_to_thread_signature(cur)
      if not cur_signature == first_signature:
         same_thread = False
      if not prev._navigator._is_immediate_temporal_successor_of(cur):
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_thread or not strictly_contiguous):
         return False
      prev = cur

   return True
