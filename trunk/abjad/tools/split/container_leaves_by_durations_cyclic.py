from abjad.metricgrid.spanner import MetricGrid
from abjad.container.container import Container


## TODO: Can this act on leaves outside of score? ##

def container_leaves_by_durations_cyclic(container, durations):
   '''Split leaves contained at any level of depth in container.
      Take split points cyclically from 'durations' list.'''

   assert isinstance(container, Container)

   mg = MetricGrid(container, durations)
   mg.splitOnBar( )
   mg.clear( )
   
