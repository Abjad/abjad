from abjad.component import _Component
from abjad.exceptions import ContiguityError
from abjad.tools.check.assess_components import assess_components


def assert_components(expr, klasses = (_Component, ),
   contiguity = None, share = None, allow_orphans = True):
   r'''Assert `expr` meets the criteria specified by the keyword parameters.
   Raise nothing where `expr` meets criteria.
   Raise assertion error where `expr` fails criteria.
   Set `contiguity` to ``'strict'``, ``'thread'`` or ``None``.
   Set `share` to ``'parent'``, ``'score'``, ``'thread'`` or ``None``.
   The word 'assert' in the name of this function is meant to
   contrast with 'assess' in other functions defined in this package.
   This function either returns none or raises an exception
   but does not return true or false.
   Functions named with 'assess' return true or false
   but raise no exceptions.

   Examples all refer to the following score. ::

      abjad> first_voice = Voice(construct.scale(3))
      abjad> second_voice = Voice(construct.scale(2))
      abjad> pitchtools.diatonicize([first_voice, second_voice])
      abjad> staff = Staff([first_voice, second_voice])
      abjad> f(staff)
      \new Staff {
              \new Voice {
                      c'8
                      d'8
                      e'8
              }
              \new Voice {
                      f'8
                      g'8
              }
      }

   With ``contiguity == 'strict'`` and ``share == 'parent'``:

      Return none for strictly contiguous components that share the same parent::

         abjad> first_voice[1:]
         [Note(d', 8), Note(e', 8)]
         abjad> check.assert_components(first_voice[1:], contiguity = 'strict', share = 'parent')

      Raise contiguity error for noncontiguous components::

         abjad> (first_voice[0], first_voice[-1])
         (Note(c', 8), Note(e', 8))
         abjad> check.assert_components(first_voice[0], first_voice[-1]), contiguity = 'strict', share = 'parent')
         ContiguityError

      Raise contiguity error for components that do not share the same parent::

         abjad> staff.leaves   
         (Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8), Note(g', 8))
         abjad> check.assert_components(staff.leaves, contiguity = 'strict', share = 'parent')
         ContiguityError

   With ``contiguity == 'strict'`` and ``share == 'score'``:

      Return none for strictly contiguous components that share the same score::

         abjad> staff.leaves
         (Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8), Note(g', 8))
         abjad> check.assert_components(staff.leaves, contiguity = 'strict', share = 'score')

      Raise contiguity error for noncontiguous components::

         abjad> (first_voice[0], first_voice[-1])
         (Note(c', 8), Note(e', 8))
         abjad> check.assert_components(first_voice[0], first_voice[-1]), contiguity = 'strict', share = 'parent')
         ContiguityError

   The `allow_orphans` keyword works as a type of bypass.

   If `allow_orphans` is set to true 
   and if `expr` is a Python list of orphan components,
   then the function will always evaluate to true, regardless
   of the checks specified by the other keywords.

   On the other hand, if the `allow_orphans` keyword is set
   to false, then `expr` must meet the checks specified by the
   other keywords in order for the function to evaluate to true.

   Calls to this function appear at the beginning of many functions.  
   Calls to this function also iterate all elements in input.
   Initial performance testing indicates that this function is

   .. todo:: eliminate keywords and break this function into
      a family of nine related functions with longer names.
   '''

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
