from abjad import *
from experimental import *


def test_TempoMarkSelector_run_01():

    selector = scoremanagertools.selectors.TempoMarkSelector()
    selector.session._current_score_package_name = 'example_score_1'
    result = selector.run(user_input='8=72')

    assert result == contexttools.TempoMark(durationtools.Duration(1, 8), 72)
