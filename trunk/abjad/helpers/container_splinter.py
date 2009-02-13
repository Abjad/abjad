from abjad.helpers.container_hew import container_hew


def container_splinter(container, i):
   '''Like container_hew( );
      but fracture spanners across newly hewn parts.'''

   return container_hew(container, i, spanners = 'fracture')
