def flip(expr):
   '''Flip expr one index to the right in parent.
      Flip expr one index to the right in spanners.

      Return None.'''

   # swap positions in parent
   if not expr.parentage.orphan:
      parent = expr.parentage.parent
      parent_index = parent.index(expr)
      try:
         next = parent[parent_index + 1]
      except IndexError:
         return
      parent._music[parent_index] = next
      parent._music[parent_index + 1] = expr

   # swap positions in spanners ... tricky!
   expr_spanners = { }
   for spanner in list(expr.spanners.attached):
      expr_spanners[spanner] = spanner.index(expr)
      spanner.remove(expr)
   next_spanners = { }
   for spanner in list(next.spanners.attached):
      next_spanners[spanner] = spanner.index(next)
      spanner.remove(next)
   for key, value in next_spanners.items( ):
      key.insert(value, expr)
   for key, value in expr_spanners.items( ):
      key.insert(value, next)
