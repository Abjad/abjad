from abjad.container.container import Container
from abjad.helpers.cyclic_extend import cyclic_extend


def contents_multiply(container, total = 2):
   '''Multiply the contents of container to total copies of contents;
      total = 1 leaves container unchanged;
      total = 2 doubles the contents of container, etc.

      Return multiplied container.'''

   assert isinstance(container, Container)
   assert isinstance(total, int)
   assert total >= 0

   if 0 < total:
      return cyclic_extend(container, n = len(container), total = total)
   else:
      container.clear( )
      return container
