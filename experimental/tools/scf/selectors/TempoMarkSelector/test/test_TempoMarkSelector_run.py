from abjad.tools import contexttools
from abjad.tools import durationtools
import scf


def test_TempoMarkSelector_run_01():

    selector = scf.selectors.TempoMarkSelector()
    selector.session._current_score_package_short_name = 'betoerung'
    result = selector.run(user_input='1')

    assert result == contexttools.TempoMark(durationtools.Duration(1, 8), 72)
