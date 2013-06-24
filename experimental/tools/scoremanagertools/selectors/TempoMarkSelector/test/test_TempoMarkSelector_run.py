from abjad import *
from experimental import *


def test_TempoMarkSelector_run_01():

    selector = scoremanagertools.selectors.TempoMarkSelector()
    selector._session._snake_case_current_score_name = 'red_example_score'
    result = selector._run(pending_user_input='8=72')

    assert result == contexttools.TempoMark(durationtools.Duration(1, 8), 72)
