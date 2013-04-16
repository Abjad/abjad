from abjad.tools import instrumenttools
from abjad.tools import scoretools
from experimental import *


def test_PerformerSelector_run_01():

    selector = scoremanagementtools.selectors.PerformerSelector()
    selector.session._current_score_package_short_name = 'example_score_1'
    result = selector.run(user_input='1')

    assert result == scoretools.Performer(name='hornist', instruments=[instrumenttools.FrenchHorn()])
