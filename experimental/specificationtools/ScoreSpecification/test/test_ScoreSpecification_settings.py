from abjad.tools import *
from specificationtools.ScoreSpecification import ScoreSpecification


def test_ScoreSpecification_settings_01():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))
    assert not specification.settings

    segment = specification.append_segment()
    assert not specification.settings
    assert not segment.settings

    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    assert not specification.settings
    assert not segment.settings

    score = specification.interpret()
    assert len(specification.settings) == 1
    assert len(segment.settings) == 1
