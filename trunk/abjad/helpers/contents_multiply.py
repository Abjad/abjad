from abjad.container.container import Container
from abjad.helpers.cyclic_extend import cyclic_extend


def contents_multiply(container, total = 2):
   '''Multiply the contents of container to total copies of contents;
      total = 1 leaves container unchanged;
      total = 2 doubles the contents of container, etc.'''

   assert isinstance(container, Container)
   assert isinstance(total, int)

   return cyclic_extend(container, n = len(container), total = total)
