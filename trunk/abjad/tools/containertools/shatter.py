from abjad.tools.containertools.splinter import splinter


def shatter(container):
   '''Shatter container.'''

   right = container
   while 1 < len(right):
      left, right = splinter(right, 1)
