from abjad.tools import check
from abjad.tools.spannertools.withdraw_from_contained import \
   _withdraw_from_contained


def detach(components):
   '''Detach component from parentage.
      Withdraw component and children of component from attached spanners.
      Return components.'''

   check.assert_components(components)
   for component in components:
      component.parentage._cut( )
      _withdraw_from_contained([component])
   return components
