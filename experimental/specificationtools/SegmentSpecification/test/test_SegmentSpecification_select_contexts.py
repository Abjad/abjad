from abjad.tools import *
from experimental import selectortools
from experimental import specificationtools
from experimental import timespantools
from experimental.specificationtools import ScoreSpecification


def test_SegmentSpecification_select_contexts_01():

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=4))
    segment = score_specification.append_segment('red')
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    selection_1 = segment.select_contexts()
    selection_2 = selectortools.Selection(
        contexts=['Grouped Rhythmic Staves Score'],
        timespan=timespantools.Timespan(selector=selectortools.SegmentSelector(index='red')))

    assert selection_1 == selection_2
