from abjad.tools.containertools.split import split


def shatter(container):
   '''Shatter container.'''

   right = container
   while 1 < len(right):
      left, right = split(right, 1)
