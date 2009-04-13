from abjad.component.component import _Component
from abjad.tools.spannertools.withdraw_from_contained import \
   _withdraw_from_contained


## TODO: Deprecate _DetachReceipt ##
## TODO: Deprecate all receipts. ##
## TODO: Extend componenttools.detach( ) to take a component list ##

def detach(component):
   '''Detach component from parentage.
      Detach component from spanners.
      Detach children of component from spanners.
      Return receipt.

      This helper leaves all score trees always in tact.'''

   if not isinstance(component, _Component):
      raise TypeError('Must be Abjad component.')

   parentage = component.parentage._cut( )
   spanners = component.spanners._detach( )
   _withdraw_from_contained([component])

   return component
