from abjad import *
from experimental import *


def test_PerformerSelector_run_01():

    selector = scoremanagertools.selectors.PerformerSelector()
    selector.session._snake_case_current_score_name = 'red_example_score'
    result = selector._run(pending_user_input='hornist')

    assert result == scoretools.Performer(name='hornist', instruments=[instrumenttools.FrenchHorn()])
