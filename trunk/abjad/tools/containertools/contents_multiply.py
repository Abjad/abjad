from abjad.container.container import Container
from abjad.tools.containertools.extend_cyclic import extend_cyclic


def contents_multiply(container, total = 2):
   '''Multiply the contents of container to total copies of contents;
      total = 1 leaves container unchanged;
      total = 2 doubles the contents of container, etc.

      Return multiplied container.'''

   assert isinstance(container, Container)
   assert isinstance(total, int)
   assert 0 <= total

   if 0 < total:
      return extend_cyclic(container, n = len(container), total = total)
   else:
      #container.clear( )
      del(container[:])
      return container
