from abjad.helpers.are_thread_contiguous_components import _are_thread_contiguous_components


def _are_spannable_components(expr):
   '''True when expr is a Python list of Abjad components
      and when any one spanner can apply to all components in list.
      Otherwise False.

      This function is a one-line wrapper around
      _are_thread_contiguous_components( ).'''

   return _are_thread_contiguous_components(expr)
