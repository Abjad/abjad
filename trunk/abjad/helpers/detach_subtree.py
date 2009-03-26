from abjad.component.component import _Component
from abjad.helpers.components_detach_spanners_deep import \
   _components_detach_spanners_deep
from abjad.receipt.detach import _DetachReceipt


def detach_subtree(component):
   '''Detach component from parentage.
      Detach component from spanners.
      Detach children of component from spanners.
      Return receipt.

      This helper is a drop-in replacement for _Component.detach( ).
      This helper leaves all score trees always in tact.'''

   if not isinstance(component, _Component):
      raise TypeError('Must be Abjad component.')

   parentage = component.parentage._detach( )
   spanners = component.spanners._detach( )
   _components_detach_spanners_deep([component])

   receipt = _DetachReceipt(component, parentage, spanners)
   return receipt
