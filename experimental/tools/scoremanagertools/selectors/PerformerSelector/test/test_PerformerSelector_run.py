from abjad import *
from experimental import *


def test_PerformerSelector_run_01():

    selector = scoremanagertools.selectors.PerformerSelector()
    selector._session._underscore_delimited_current_score_name = 'example_score_1'
    result = selector.run(user_input='hornist')

    assert result == scoretools.Performer(name='hornist', instruments=[instrumenttools.FrenchHorn()])
