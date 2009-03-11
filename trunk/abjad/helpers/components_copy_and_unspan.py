from abjad.helpers.are_spannable_components import _are_spannable_components


def components_copy_and_unspan(spannable_components):
   '''Docs.'''

   if not _are_spannable_components(spannable_components):
      raise ValueError('input must be spannable components.')

   
