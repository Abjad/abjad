from abjad.metricgrid.spanner import MetricGrid
from abjad.container.container import Container


def metric_slice(container, meters):
   '''Slice leaves in given container at ponts delimited by meters.'''

   assert isinstance(container, Container)

   mg = MetricGrid(container, meters)
   mg.splitOnBar( )
   mg.clear( )
   
