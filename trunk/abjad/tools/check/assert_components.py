from abjad.component.component import _Component
from abjad.exceptions import ContiguityError
from abjad.tools.check.assess_components import assess_components

#visits = 0

def assert_components(expr, klasses = (_Component, ),
   contiguity = None, share = None, allow_orphans = True):
   '''Assert expr is a Python list of Abjad components.
      Set _contiguity_ to None, 'strict' or 'thread'.
      Set _share_ to None, 'parent', 'score' or 'thread'.

      The allow_orphans keyword works as a type of bypass.
      If allow_orphans is set to True (which it is by default),
      and if expr is a Python list of orphan components,
      then the function will always evaluate to True, regardless
      of the checks specified by the other keywords.

      On the other hand, if the allow_orphans keyword is set
      to False, then expr must meet the checks specified by the
      other keywords in other for the function to evaluate to True.

      Calls to this function appear at the beginning of many functions.
      Calls to this function also iterate all elements in expr.
      For this reason, you can turn off all calls to this function.
      Set something in cfg.'''

   #global visits
   #visits += 1
   #print 'debug: in assert_components %s ...' % visits

   if contiguity is None:
      
      if share is None:
         if not assess_components(expr, klasses = klasses):
            raise TypeError('Must be Python list'
               ' of Abjad %s.' % str(klasses))

      elif share == 'parent':
         if not assess_components(expr, klasses = klasses, share = 'parent', 
            allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of Abjad components'
               ' all in same parent.')

      elif share == 'score':
         if not assess_components(expr, klasses = klasses, share = 'score', 
            allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of Abjad components'
               ' all in same score.')

      elif share == 'thread':
         if not assess_components(expr, klasses = klasses, share = 'thread', 
            allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of Abjad components'
               ' all in same thread.')

      else:
         raise ValueError(
            "share must be 'parent', 'score', 'thread' or None.")

   elif contiguity == 'strict':
   
      if share is None:
         if not assess_components(expr, klasses = klasses, contiguity = 'strict', 
            allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of strictly contiguous Abjad components.')

      elif share == 'parent':
         if not assess_components(expr, klasses = klasses, contiguity = 'strict', 
            share = 'parent', allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of strictly contiguous Abjad components'
               ' all in same parent.')
   
      elif share == 'score':
         if not assess_components(expr, klasses = klasses, contiguity = 'strict', 
            share = 'score', allow_orphans = allow_orphans):
            raise ContiguityError('Must be Python list'
               ' of strictly contiguous Abjad components'
               ' all in same score.')
   
      elif share == 'thread':
         if not assess_components(expr, klasses = klasses, contiguity = 'strict', 
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
         if not assess_components(expr, klasses = klasses,
            contiguity = 'thread', allow_orphans = allow_orphans):
            raise ContiguityError('Must by Python list'
               ' of thread-contiguous Abjad components.')

   else:
      raise ValueError("'contiguity' must be 'strict', 'thread' or None.")
