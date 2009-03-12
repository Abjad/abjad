from abjad.helpers.are_spannable_components import _are_spannable_components


def components_copy_and_unspan(spannable_components):
   '''Deep copy each of the components in spannable_components.
      Remove all spanners attaching to any component.

      spannable_components must be a list of spannable components.

      Example:'''

   if not _are_spannable_components(spannable_components):
      raise ValueError('input must be spannable components.')

    
