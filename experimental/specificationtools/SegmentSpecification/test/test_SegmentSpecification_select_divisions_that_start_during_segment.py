from abjad.tools import *
from experimental import *
from experimental import helpertools
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification


def test_SegmentSpecification_select_divisions_that_start_during_segment_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    specification = ScoreSpecification(score_template)

    segment = specification.append_segment('red')
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    contexts = ['Voice 1', 'Voice 3']

    selector_1 = segment.select_divisions(contexts=contexts, stop=5)
    selector_2 = selectortools.MultipleContextDivisionSliceSelector(
        contexts=['Voice 1', 'Voice 3'],
        inequality=timespantools.TimespanInequality(
            timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
            timespantools.SingleSourceTimespan(
                selector=selectortools.SegmentSelector(
                    index='red'
                    )
                )
            ),
        stop=5
        )

    assert selector_1 == selector_2
