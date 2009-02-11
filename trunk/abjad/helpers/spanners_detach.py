from abjad.helpers.iterate import iterate


def spanners_detach(expr):
   '''Detach spanners from every Abjad component in expr.'''

   for component in iterate(expr, '_Component'):
      component.spanners.detach( )
