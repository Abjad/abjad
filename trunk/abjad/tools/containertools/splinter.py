from abjad.tools.containertools.hew import hew


def splinter(container, i):
   '''Like containertools.hew( );
      but fracture spanners across newly hewn parts.'''

   return hew(container, i, spanners = 'fracture')
