from abjad import *


def test_MetricGridSpanner___init___01():
    '''Init empty metric grid spanner.
    '''

    metric_grid = spannertools.MetricGridSpanner()
    assert isinstance(metric_grid, spannertools.MetricGridSpanner)
