from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_components import _are_components
from abjad.helpers.are_components_in_same_parent import \
   _are_components_in_same_parent
from abjad.helpers.are_components_in_same_score import \
   _are_components_in_same_score
from abjad.helpers.are_components_in_same_thread import \
   _are_components_in_same_thread
from abjad.helpers.are_strictly_contiguous_components import \
   _are_strictly_contiguous_components
from abjad.helpers.are_strictly_contiguous_components_in_same_parent import \
   _are_strictly_contiguous_components_in_same_parent
from abjad.helpers.are_strictly_contiguous_components_in_same_score import \
   _are_strictly_contiguous_components_in_same_score
from abjad.helpers.are_strictly_contiguous_components_in_same_thread import \
   _are_strictly_contiguous_components_in_same_thread
from abjad.helpers.are_thread_contiguous_components import \
   _are_thread_contiguous_components


def _test_components(expr, 
   contiguity = None, share = None, allow_orphans = True):
   '''Assert expr is a Python list of Abjad components.
      Set _contiguity_ to None, 'strict' or 'thread'.
      Set _share_ to None, 'parent', 'score' or 'thread'.

      The allow_orphans keyword works as a type of bypass.
      If allow_orphans is set to True (which it is by default),
      and if expr is a Python list of orphan components,
      then the helper will always evaluate to True, regardless
      of the checks specified by the other keywords.

      On the other hand, if the allow_orphans keyword is set
      to False, then expr must meet the checks specified by the
      other keywords in other for the helper to evaluate to True.

      Calls to this function appear at the beginning of many helpers.
      Calls to this function also iterate all elements in expr.
      For this reason, you can turn off all calls to this function.
      Set something in cfg.'''

   if contiguity is None:
      
      if share is None:
         _are_components(expr)

      elif share == 'parent':
         _are_components_in_same_parent(expr, allow_orphans)

      elif share == 'score':
         _are_components_in_same_score(expr, allow_orphans)

      elif share == 'thread':
         _are_components_in_same_thread(expr, allow_orphans)

      else:
         raise ValueError(
            "share must be 'parent', 'score', 'thread' or None.")

   elif contiguity == 'strict':
   
      if share is None:
         _are_strictly_contiguous_components(expr, allow_orphans)

      elif share == 'parent':
         _are_strictly_contiguous_components_in_same_parent(
            expr, allow_orphans)

      elif share == 'score':
         _are_strictly_contiguous_components_in_same_score(
            expr, allow_orphans)

      elif share == 'thread':
         _are_strictly_contiguous_components_in_same_thread(
            expr, allow_orphans)

      else:
         raise ValueError(
            "share must be 'parent', 'score', 'thread' or None.")

   elif contiguity == 'thread':

      if share is not None:
         raise ValueError('When checking for thread-contiguity,'
            " the 'share' keyword should not be set.")

      else:
         _are_thread_contiguous_components(expr, allow_orphans)

   else:
      raise ValueError("'contiguity' must be 'strict', 'thread' or None.")
