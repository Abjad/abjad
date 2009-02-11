from abjad.container.container import Container
from abjad.helpers.cyclic_extend import cyclic_extend


def contents_multiply(container, n = 1):
   '''Multiply the contents of container n times.'''

   assert isinstance(container, Container)
   cyclic_extend(container, len(container), n)
   return container
