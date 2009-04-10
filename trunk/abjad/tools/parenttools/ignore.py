from abjad.helpers.assert_components import assert_components


def _ignore(components):
   '''No contiguity requirements.
      Use to temporarily 'lift' parent references.
      Return receipt of unordered set of (component, parent) pairs.
      Then do some other operation, probably copy.
      Then reapply parent references.
      Call _parenttools.restore(receipt).'''

   assert_components(components)

   receipt = set([ ])
   for component in components:
      parent = component.parentage.parent
      component.parentage._ignore( )
      receipt.add((component, parent))

   return receipt
