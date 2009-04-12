from abjad.exceptions.exceptions import ContiguityError
from abjad.tools import check


def assert_components(expr, 
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
         if not check.assess_components(expr):
            raise TypeError('Must be Python list'
               ' of Abjad components.')

      elif share == 'parent':
         if not check.assess_components(expr, share = 'parent', 
            allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of Abjad components'
               ' all in same parent.')

      elif share == 'score':
         if not check.assess_components(expr, share = 'score', 
            allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of Abjad components'
               ' all in same score.')

      elif share == 'thread':
         if not check.assess_components(expr, share = 'thread', 
            allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of Abjad components'
               ' all in same thread.')

      else:
         raise ValueError(
            "share must be 'parent', 'score', 'thread' or None.")

   elif contiguity == 'strict':
   
      if share is None:
         if not check.assess_components(expr, contiguity = 'strict', 
            allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of strictly contiguous Abjad components.')

      elif share == 'parent':
         if not check.assess_components(expr, contiguity = 'strict', 
            share = 'parent', allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of strictly contiguous Abjad components'
               ' all in same parent.')
   
      elif share == 'score':
         if not check.assess_components(expr, contiguity = 'strict', 
            share = 'score', allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of strictly contiguous Abjad components'
               ' all in same score.')
   
      elif share == 'thread':
         if not check.assess_components(expr, contiguity = 'strict', 
            share = 'thread', allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of strictly contiguous Abjad components'
               ' all in same thread.')
   
      else:
         raise ValueError(
            "share must be 'parent', 'score', 'thread' or None.")

   elif contiguity == 'thread':

      if share is not None:
         raise ValueError('When checking for thread-contiguity,'
            " the 'share' keyword should not be set.")

      else:
         if not check.assess_components(expr, 
            contiguity = 'thread', allow_orphans = allow_orphans):
            raise ContiguityError('Must by Python list'
               ' of thread-contiguous Abjad components.')

   else:
      raise ValueError("'contiguity' must be 'strict', 'thread' or None.")
