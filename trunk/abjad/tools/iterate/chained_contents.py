from abjad.exceptions.exceptions import TieChainError


def chained_contents(expr):
   '''Iterate expr but return tie chains in place of leaves.
      Crossing ties raise TieChainError.'''
   from abjad.container.container import Container
   from abjad.leaf.leaf import _Leaf

   if isinstance(expr, _Leaf):
      if len(expr.tie.chain) == 1:
         yield expr.tie.chain
      else:
         raise TieChainError('can not only one leaf in tie chain.')
   elif isinstance(expr, (list, Container)):
      for component in expr:
         if isinstance(component, _Leaf):
            if not component.tie.spanned or component.tie.last:
               yield component.tie.chain
         elif isinstance(component, Container):
            yield component
   else:
      raise ValueError('input must be iterable.')
