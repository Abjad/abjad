from abjad import *
from experimental import *


def test_PerformerSelector_run_01():

    selector = scoremanagertools.selectors.PerformerSelector()
    selector.session._current_score_package_short_name = 'example_score_1'
    result = selector.run(user_input='hornist')

    assert result == scoretools.Performer(name='hornist', instruments=[instrumenttools.FrenchHorn()])
