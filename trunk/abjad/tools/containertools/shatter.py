#from abjad.tools.containertools.split import split
from abjad.tools.containertools.split_fractured import split_fractured


def shatter(container):
   '''Shatter container.'''

   right = container
   while 1 < len(right):
      left, right = split_fractured(right, 1)
