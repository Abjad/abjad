from abjad.exceptions import MissingSpannerError
from abjad.tools import check


def are_in_same_spanner(components):
   '''True if all components in list share same tie spanner,
      otherwise False.'''

   check.assert_components(components)
   
   try:
      first = components[0]
      try:
         first_tie_spanner = first.tie.spanner
         for component in components[1:]:
            if component.tie.spanner is not first_tie_spanner:
               return False
      except MissingSpannerError:
         return False
   except IndexError:
      return True

   return True
