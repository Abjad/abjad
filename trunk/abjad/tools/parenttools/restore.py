def restore(receipt):
   '''Use to restore parentage.
      Use after call to parenttools.ignore_parent(components).
      Return None.'''

   for component, parent in receipt:
      assert component.parentage.parent is None
      component.parentage._switch(parent)
