def _restore(receipt):
   '''Use to restore parentage.
      Use after call to _ignore(components), from parenttools.
      Return None.'''

   for component, parent in receipt:
      assert component.parentage.parent is None
      component.parentage._switch(parent)
