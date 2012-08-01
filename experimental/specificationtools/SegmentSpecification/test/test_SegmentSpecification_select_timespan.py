from abjad.tools import *
from experimental import selectortools
from experimental import specificationtools
from experimental import timespantools
from experimental.specificationtools import ScoreSpecification


def test_SegmentSpecification_select_timespan_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])

    selection_1 = segment.select_timespan()
    selection_2 = selectortools.MultipleContextTimespanSelector(
        context_names=['Grouped Rhythmic Staves Score'],
        timespan=timespantools.SingleSourceTimespan(selector=selectortools.SegmentSelector(index='red')))

    assert selection_1 == selection_2
