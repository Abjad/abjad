from abjad.tools.split.container_fractured import container_fractured


def shatter(container):
   '''Shatter container.'''

   right = container
   while 1 < len(right):
      left, right = container_fractured(right, 1)
