from abjad.components._Component import _Component
from abjad.tools.componenttools.component_is_orphan import component_is_orphan
from abjad.tools.componenttools.component_to_score_root import component_to_score_root
import types


def all_are_contiguous_components_in_same_score(expr, klasses = None, allow_orphans = True):
   '''True when elements in `expr` are all contiguous components in same score.
   Otherwise false::

      abjad> score = Score([Staff(macros.scale(3))])
      abjad> componenttools.all_are_contiguous_components_in_same_score(score.leaves) 
      True

   True when elements in `expr` are all contiguous `klasses` in same score.
   Otherwise false::

      abjad> score = Score([Staff(macros.scale(3))])
      abjad> componenttools.all_are_contiguous_components_in_same_score(score.leaves, klasses = Note) 
      True

   Return boolean.
   '''

   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      #raise TypeError('Must be list of Abjad components.')
      return False

   if klasses is None:
      klasses = _Component

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, klasses):
      return False

   orphan_components = True   
   if not component_is_orphan(first):
      orphan_components = False

   same_score = True
   strictly_contiguous = True

   first_score = component_to_score_root(first)
   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, klasses):
         return False
      if not component_is_orphan(cur):
         orphan_components = False
      if not component_to_score_root(cur) is first_score:
         same_score = False
      if not prev._navigator._is_immediate_temporal_successor_of(cur):
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_score or not strictly_contiguous):
         return False
      prev = cur

   return True
