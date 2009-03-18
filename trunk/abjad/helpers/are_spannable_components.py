from abjad.helpers.are_strictly_contiguous_components_in_same_thread import _are_strictly_contiguous_components_in_same_thread


## TODO: Reimplement as wrapper around _are_thread_contiguous_components( ).
## TODO: Implement _are_thread_contiguous_components( ).

def _are_spannable_components(expr):
   '''True when expr is a Python list of Abjad components
      and when any one spanner can apply to all components in list.
      Otherwise False.

      NOTE that this function is currently merely a literal wrapper
      around _are_strictly_contiguous_components_in_same_thread( ).
      The real code for this helper will be written once we go back 
      and make the thread-identification stuff work perfectly.

      At this point _are_spannable_components( ) should be exactly
      the same thing as the (currently nonexistent)
      _are_thread_contiguous_components( ).

      NOTE that you should use this _are_spannable_components( )
      in any function that you want to EVENTUALLY use
      _are_spannable_components( ), as a type of structural to-do.'''

   return _are_strictly_contiguous_components_in_same_thread(expr)
