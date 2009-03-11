from abjad.helpers.are_spannable_components import _are_spannable_components


def components_untie(spannable_components):
   '''Input parameter:

      spannable_components must be a list of spannable Abjad components.

      Description:

      Untie every component in spannable_components
      Return spannable_components.'''

   # check input
   if not _are_spannable_components(spannable_components):
      raise ContiguityError('input must be spannable components.')

   # untie components
   for component in spannable_components:
      component.tie.unspan( )

   # return components
   return spannable_components
