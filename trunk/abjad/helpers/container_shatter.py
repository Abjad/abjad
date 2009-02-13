from abjad.helpers.container_splinter import container_splinter


def container_shatter(container):
   '''Shatter container.'''

   right = container
   while len(right) > 1:
      left, right = container_splinter(right, 1)
