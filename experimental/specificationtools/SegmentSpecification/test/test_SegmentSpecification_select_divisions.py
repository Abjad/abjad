from abjad.tools import *
from experimental import *
from experimental import helpertools
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification


def test_SegmentSpecification_select_divisions_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])
    contexts = ['Voice 1', 'Voice 3']

    selector_1 = segment.select_divisions(contexts=contexts, stop=5)
    selector_2 = selectortools.MultipleContextDivisionSliceSelector(
        context_names=['Voice 1', 'Voice 3'],
        inequality=timespantools.TimespanInequality(
            timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
            timespantools.SingleSourceTimespan(
                selector=selectortools.SegmentItemSelector(
                    identifier='red'
                    )
                )
            ),
        stop=5
        )

    assert selector_1 == selector_2
