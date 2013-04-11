from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental import *


def test_TempoMarkSelector_run_01():

    selector = scftools.selectors.TempoMarkSelector()
    selector.session._current_score_package_short_name = 'example_score_1'
    result = selector.run(user_input='1')

    assert result == contexttools.TempoMark(durationtools.Duration(1, 8), 72)
