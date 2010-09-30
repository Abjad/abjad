def _restore(receipt):
   '''Use to restore parentage.
      Use after call to _ignore(components), from componenttools.
      Return None.'''

   for component, parent in receipt:
      assert component._parentage.parent is None
      component._parentage._switch(parent)
