from abjad.metricgrid.spanner import MetricGrid
from abjad.container.container import Container


## TODO: Change containertools.slice_by_duration( ) to accept durations ##

def slice_by_duration(container, meters):
   '''Slice leaves in given container at ponts delimited by meters.'''

   assert isinstance(container, Container)

   mg = MetricGrid(container, meters)
   mg.splitOnBar( )
   mg.clear( )
   
