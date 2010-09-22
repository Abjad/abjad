from abjad.components._Component import _Component
from abjad.tools import threadtools
from abjad.tools.componenttools.component_is_orphan import component_is_orphan
import types


def all_are_components_in_same_thread(expr, klasses = (_Component, ), allow_orphans = True):
   '''True when expr is a Python list of Abjad components such
      that all components in list carry the same thread signature.

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

   #first_signature = first.thread.signature
   first_signature = threadtools.component_to_thread_signature(first)
   for component in expr[1:]:
      #if not component.parentage.is_orphan:
      if not component_is_orphan(component):
         orphan_components = False
      #if component.thread.signature != first_signature:
      if threadtools.component_to_thread_signature(component) != first_signature:
         same_thread = False
      if not allow_orphans and not same_thread:
         return False
      if allow_orphans and not orphan_components and not same_thread:
         return False

   return True
