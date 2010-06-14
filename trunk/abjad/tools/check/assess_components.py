from abjad.component import _Component


def assess_components(expr, klasses = (_Component, ), 
   contiguity = None, share = None, allow_orphans = True):
   r'''Test `expr`. Return true or false depending on the
   combination of values of the four keyword parameters.
   Set `contiguity` to ``'strict'``, ``'thread'`` or ``None``.
   Set `share` to ``'parent'``, ``'score'``, ``'thread'`` or ``None``.
   The word 'assess' in the name of this function is meant to
   contrast with 'assert' in other functions defined in this package.
   This function returns true or false but raises no exceptions.
   Functions named with 'assert' raise exceptions instead of
   returning true or false.

   Examples all refer to the following score. ::

      abjad> first_voice = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
      abjad> second_voice = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
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

      True for strictly contiguous components that share the same parent::

         abjad> first_voice[1:]
         [Note(d', 8), Note(e', 8)]
         abjad> check.assess_components(first_voice[1:], contiguity = 'strict', share = 'parent')
         True

      False for noncontiguous components::

         abjad> (first_voice[0], first_voice[-1])
         (Note(c', 8), Note(e', 8))
         abjad> check.assess_components(first_voice[0], first_voice[-1]), contiguity = 'strict', share = 'parent')
         False

      False for components that do not share the same parent::

         abjad> staff.leaves   
         (Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8), Note(g', 8))
         abjad> check.assess_components(staff.leaves, contiguity = 'strict', share = 'parent')
         False

   With ``contiguity == 'strict'`` and ``share == 'score'``:

      True for strictly contiguous components that share the same score::

         abjad> staff.leaves
         (Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8), Note(g', 8))
         abjad> check.assess_components(staff.leaves, contiguity = 'strict', share = 'score')
         True

      False for noncontiguous components::

         abjad> (first_voice[0], first_voice[-1])
         (Note(c', 8), Note(e', 8))
         abjad> check.assess_components(first_voice[0], first_voice[-1]), contiguity = 'strict', share = 'parent')
         False

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
   from abjad.tools import componenttools

   if contiguity is None:
      
      if share is None:
         return componenttools.all_are_components(expr, klasses = klasses)

      elif share == 'parent':
         return componenttools.all_are_components_in_same_parent(expr, 
            klasses = klasses, allow_orphans = allow_orphans)

      elif share == 'score':
         return componenttools.all_are_components_in_same_score(expr, 
            klasses = klasses, allow_orphans = allow_orphans)

      elif share == 'thread':
         return componenttools.all_are_components_in_same_thread(expr, 
            klasses = klasses, allow_orphans = allow_orphans)

      else:
         raise ValueError(
            "share must be 'parent', 'score', 'thread' or None.")

   elif contiguity == 'strict':
   
      if share is None:
         return componenttools.all_are_contiguous_components(
            expr, klasses = klasses, allow_orphans = allow_orphans)

      elif share == 'parent':
         return componenttools.all_are_contiguous_components_in_same_parent(
            expr, klasses = klasses, allow_orphans = allow_orphans)

      elif share == 'score':
         return componenttools.all_are_contiguous_components_in_same_score(
            expr, klasses = klasses, allow_orphans = allow_orphans)

      elif share == 'thread':
         return componenttools.all_are_contiguous_components_in_same_thread(
            expr, klasses = klasses, allow_orphans = allow_orphans)

      else:
         raise ValueError(
            "share must be 'parent', 'score', 'thread' or None.")

   elif contiguity == 'thread':

      if share is not None:
         raise ValueError('When checking for thread-contiguity,'
            " the 'share' keyword should not be set.")

      else:
         return componenttools.all_are_thread_contiguous_components(
            expr, klasses = klasses, allow_orphans = allow_orphans)

   else:
      raise ValueError("'contiguity' must be 'strict', 'thread' or None.")
