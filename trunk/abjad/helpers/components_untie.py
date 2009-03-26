from abjad.helpers.assert_components import assert_components


def components_untie(spannable_components):
   '''Input parameter:

      spannable_components must be a list of spannable Abjad components.

      Description:

      Untie every component in spannable_components
      Return spannable_components.'''

   # check input
   assert_components(spannable_components, contiguity = 'thread')

   # untie components
   for component in spannable_components:
      component.tie.unspan( )

   # return components
   return spannable_components
