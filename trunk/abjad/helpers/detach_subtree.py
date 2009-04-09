from abjad.component.component import _Component
from abjad.receipt.detach import _DetachReceipt
from abjad.tools.spannertools.withdraw_from_contained import \
   _withdraw_from_contained


## TODO: Internalize detach_subtree( ) into _Container.__setitem__ ##

def detach_subtree(component):
   '''Detach component from parentage.
      Detach component from spanners.
      Detach children of component from spanners.
      Return receipt.

      This helper is a drop-in replacement for _Component.detach( ).
      This helper leaves all score trees always in tact.'''

   if not isinstance(component, _Component):
      raise TypeError('Must be Abjad component.')

   parentage = component.parentage._cut( )
   spanners = component.spanners._detach( )
   _withdraw_from_contained([component])

   receipt = _DetachReceipt(component, parentage, spanners)
   return receipt
